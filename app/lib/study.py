"""study.py — passage splitting, AI summarisation/questions, verification, offline fallbacks.

Public API
----------
strip_metadata(text)       -> str                       body text with header lines removed
split_passages(text)       -> dict[str, str]           {P1: ..., P2: ...}
summarise(passages, ask_fn)-> dict                     {bullets: [{text, passage_id, proof}], dropped, backend}
make_questions(passages, ask_fn) -> dict
                                   {questions: [{stem, options, correct_index, passage_id, proof_text}], ...}
offline_summary(passages)  -> list[dict]
offline_questions(passages)-> list[dict]
study(text, ask_fn)        -> dict  (all-in-one, cached by text hash)
fingerprint_check(body_text, expected_fp) -> bool   sha256(body_text[:200]) == expected_fp
highlight_proof(passage, proof_sentence) -> str     passage with proof_sentence wrapped in <mark>
"""

from __future__ import annotations

import hashlib
import json
import re
import textwrap
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from functools import lru_cache

# ---------------------------------------------------------------------------
# Metadata / header stripping  (Fix #1)
# ---------------------------------------------------------------------------

# Lines that are part of the sample file preamble rather than the reading body:
#   • The title line (matches a known pattern or heuristic)
#   • "Fictional course reading…" disclaimer
#   • "All companies, people…" disclaimer
#   • Blank lines
# We strip them before splitting into passages so they don't pollute P1 or the summary.

_HEADER_PATTERNS: list[re.Pattern] = [
    # Passage markers like "[P1]", "[P2]" — stripped; we do our own splitting
    re.compile(r"^\s*\[P\d+\]\s*$"),
    # "Fictional … created for …" disclaimer
    re.compile(r"^\s*Fictional\b", re.IGNORECASE),
    # "All companies … invented." disclaimer
    re.compile(r"^\s*All companies\b", re.IGNORECASE),
    # Title lines: typically "Title — Course, Week N" (contains " — " and no sentence-ending punctuation)
    re.compile(r"^[^.!?]*—[^.!?]*$"),
]


def strip_metadata(text: str) -> str:
    """Remove header / metadata lines from a sample reading.

    Strips:
    - [Pn] passage-marker lines (we re-split ourselves)
    - "Fictional course reading …" disclaimer lines
    - "All companies … invented." disclaimer lines
    - Title lines that look like "Title — Course, Week N" (no sentence punctuation)

    Returns the cleaned body text as a single string with normalised whitespace.
    """
    lines = text.splitlines()
    body_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(pat.match(stripped) for pat in _HEADER_PATTERNS):
            continue
        body_lines.append(stripped)
    return " ".join(body_lines)


# ---------------------------------------------------------------------------
# Passage splitting
# ---------------------------------------------------------------------------

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def _sentences(text: str) -> list[str]:
    """Split text into individual sentences."""
    parts = _SENTENCE_RE.split(text.strip())
    return [p.strip() for p in parts if p.strip()]


def split_passages(text: str) -> dict[str, str]:
    """Split raw text into {P1: ..., P2: ...}.

    Target: 2–4 sentences / up to ~120 words per passage.
    Original text is preserved; no summarisation here.
    """
    sentences = _sentences(text)
    if not sentences:
        return {"P1": text.strip()}

    passages: dict[str, str] = {}
    idx = 1
    current: list[str] = []
    word_count = 0

    for sent in sentences:
        words_in_sent = len(sent.split())
        # Start a new passage if adding this sentence would exceed ~120 words
        # AND we already have at least 2 sentences.
        if word_count + words_in_sent > 120 and len(current) >= 2:
            passages[f"P{idx}"] = " ".join(current)
            idx += 1
            current = []
            word_count = 0
        current.append(sent)
        word_count += words_in_sent

    if current:
        passages[f"P{idx}"] = " ".join(current)

    return passages


# ---------------------------------------------------------------------------
# JSON parsing (defensive)
# ---------------------------------------------------------------------------


def _parse_json(raw: str) -> object:
    """Strip markdown code fences and parse JSON.  Returns None on failure."""
    # Remove ```json ... ``` or ``` ... ```
    cleaned = re.sub(r"```(?:json)?\s*", "", raw)
    cleaned = cleaned.replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find the first JSON object or array in the text
        for start_char, end_char in [("[", "]"), ("{", "}")]:
            start = cleaned.find(start_char)
            end = cleaned.rfind(end_char)
            if start != -1 and end != -1 and end > start:
                try:
                    return json.loads(cleaned[start : end + 1])
                except json.JSONDecodeError:
                    pass
    return None


# ---------------------------------------------------------------------------
# Verification helpers
# ---------------------------------------------------------------------------


def _normalise(s: str) -> str:
    """Lower-case, collapse whitespace, strip punctuation for fuzzy compare."""
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _fuzzy_match(needle: str, haystack: str, threshold: float = 0.85) -> bool:
    """Return True if needle is found (or close to found) in haystack.

    Checks:
    1. Exact normalised substring.
    2. SequenceMatcher ratio against each sentence in haystack >= threshold.
    """
    n_needle = _normalise(needle)
    n_hay = _normalise(haystack)
    if n_needle in n_hay:
        return True
    for sent in _sentences(haystack):
        ratio = SequenceMatcher(None, n_needle, _normalise(sent)).ratio()
        if ratio >= threshold:
            return True
    return False


def _find_proof_passage(proof: str, passages: dict[str, str]) -> str | None:
    """Search all passages for proof; return the passage_id where it is found, or None.

    Fix #3: searches ALL passages so that a wrong cited id can be corrected.
    """
    for pid, text in passages.items():
        if _fuzzy_match(proof, text):
            return pid
    return None


def _verify_bullet(item: dict, passages: dict[str, str]) -> bool:
    """Return True if item["proof"] or item["proof_text"] or item["text"] can be found in the named passage."""
    pid = item.get("passage_id", "")
    passage = passages.get(pid, "")
    if not passage:
        return False
    probe = item.get("proof") or item.get("proof_text") or item.get("text", "")
    return _fuzzy_match(probe, passage)


def _verify_question(item: dict, passages: dict[str, str]) -> bool:
    """Return True if item["proof_text"] can be found in the named passage."""
    pid = item.get("passage_id", "")
    passage = passages.get(pid, "")
    if not passage:
        return False
    proof = item.get("proof_text", "")
    return _fuzzy_match(proof, passage)


def _correct_or_drop_question(item: dict, passages: dict[str, str]) -> dict | None:
    """Fix #3: If proof_text is not in the cited passage, search all passages.

    Returns the item (possibly with corrected passage_id) if found anywhere,
    or None if not found in any passage.
    """
    proof = item.get("proof_text", "")
    if not proof:
        return None
    # First check the cited passage
    if _verify_question(item, passages):
        return item
    # Search all passages for a correct home
    found_pid = _find_proof_passage(proof, passages)
    if found_pid is not None:
        corrected = dict(item)
        corrected["passage_id"] = found_pid
        return corrected
    return None


def _correct_or_drop_bullet(item: dict, passages: dict[str, str]) -> dict | None:
    """Fix #3 applied to summary bullets.

    Returns the item (possibly with corrected passage_id) if found anywhere,
    or None if not found in any passage.
    """
    probe = item.get("proof") or item.get("proof_text") or item.get("text", "")
    if not probe:
        return None
    # First check the cited passage
    if _verify_bullet(item, passages):
        return item
    # Search all passages for a correct home
    found_pid = _find_proof_passage(probe, passages)
    if found_pid is not None:
        corrected = dict(item)
        corrected["passage_id"] = found_pid
        return corrected
    return None


# ---------------------------------------------------------------------------
# AI summarisation
# ---------------------------------------------------------------------------

_SUMMARISE_SYSTEM = (
    "You are a plain-language tutor helping adult students who are English-language learners. "
    "Use ONLY the passages provided. Write in simple, clear English (aim for 8th-grade level). "
    "For every bullet:\n"
    "  - 'text' is a SHORT plain-language paraphrase (1–2 sentences, NOT copied word-for-word)\n"
    "  - 'passage_id' is the passage id (e.g. P1) where the idea comes from\n"
    "  - 'proof' is the EXACT supporting sentence copied WORD-FOR-WORD from that passage\n"
    "Return ONLY valid JSON: "
    '{"bullets": [{"text": "plain paraphrase", "passage_id": "P1", "proof": "exact copied sentence"}, ...]}'
    " Aim for 5 bullets."
)

_QUESTIONS_SYSTEM = (
    "You are a plain-language tutor creating multiple-choice practice questions for adult students "
    "who are English-language learners. "
    "Use ONLY the passages provided. Write in simple, clear English. "
    "For every question, cite the passage id and copy the proof sentence WORD-FOR-WORD from that passage. "
    "Return ONLY valid JSON: "
    '{"questions": [{"stem": "...", "options": ["A", "B", "C", "D"], "correct_index": 0, '
    '"passage_id": "P1", "proof_text": "...exact sentence..."}, ...]}'
    " Aim for 5 questions."
)


def _passages_prompt(passages: dict[str, str]) -> str:
    parts = [f"[{pid}] {text}" for pid, text in passages.items()]
    return "\n\n".join(parts)


def summarise(passages: dict[str, str], ask_fn: Callable) -> dict:
    """Return verified summary bullets + metadata.

    Returns:
        {
          "bullets": [{"text": str, "passage_id": str, "proof": str}],
          "dropped": int,
          "backend": str,
        }
    """
    prompt = (
        "Summarise the following reading in 5 bullet points for an English-language learner. "
        "Plain English only. Each bullet must have a short paraphrase (text), the passage id, "
        "and the exact proof sentence copied word-for-word.\n\n"
        + _passages_prompt(passages)
    )
    answer = ask_fn(prompt, system=_SUMMARISE_SYSTEM, json_mode=True)
    backend = answer.backend

    parsed = _parse_json(answer.text)
    raw_bullets: list[dict] = []
    if isinstance(parsed, dict):
        raw_bullets = parsed.get("bullets", [])
    elif isinstance(parsed, list):
        raw_bullets = parsed  # tolerate top-level list

    verified: list[dict] = []
    dropped = 0
    for item in raw_bullets:
        if not isinstance(item, dict):
            dropped += 1
            continue
        # Normalise field: accept both "proof" and legacy "proof_text"
        if "proof_text" in item and "proof" not in item:
            item["proof"] = item.pop("proof_text")
        # Also strip the [P3] ... [P3] pattern from text (Fix #2)
        if "text" in item:
            item["text"] = re.sub(r"\s*\[P\d+\]\s*", " ", item["text"]).strip()

        result = _correct_or_drop_bullet(item, passages)
        if result is not None:
            verified.append(result)
        else:
            dropped += 1

    # Top up from offline if fewer than 3 verified bullets
    if len(verified) < 3:
        fallback = offline_summary(passages)
        existing_pids = {b["passage_id"] for b in verified}
        for b in fallback:
            if b["passage_id"] not in existing_pids:
                verified.append(b)
            if len(verified) >= 5:
                break

    return {"bullets": verified[:5], "dropped": dropped, "backend": backend}


def make_questions(passages: dict[str, str], ask_fn: Callable) -> dict:
    """Return verified MCQ list + metadata.

    Returns:
        {
          "questions": [{"stem", "options", "correct_index", "passage_id", "proof_text"}],
          "dropped": int,
          "backend": str,
        }
    """
    prompt = (
        "Create 5 multiple-choice questions from the following reading. "
        "Each question must have exactly 4 options (A, B, C, D) and one correct answer. "
        "Plain English only.\n\n"
        + _passages_prompt(passages)
    )
    answer = ask_fn(prompt, system=_QUESTIONS_SYSTEM, json_mode=True)
    backend = answer.backend

    parsed = _parse_json(answer.text)
    raw_questions: list[dict] = []
    if isinstance(parsed, dict):
        raw_questions = parsed.get("questions", [])
    elif isinstance(parsed, list):
        raw_questions = parsed

    verified: list[dict] = []
    dropped = 0
    for item in raw_questions:
        if not isinstance(item, dict):
            dropped += 1
            continue
        # Normalise correct_index
        ci = item.get("correct_index", 0)
        if isinstance(ci, str):
            try:
                ci = int(ci)
            except ValueError:
                ci = 0
        item["correct_index"] = ci
        # Fix #3: correct or drop based on all-passage search
        result = _correct_or_drop_question(item, passages)
        if result is not None:
            verified.append(result)
        else:
            dropped += 1

    # Top up from offline if fewer than 3 verified questions (Fix #6)
    if len(verified) < 3:
        fallback = offline_questions(passages)
        for q in fallback:
            if len(verified) >= 5:
                break
            verified.append(q)

    return {"questions": verified[:5], "dropped": dropped, "backend": backend}


# ---------------------------------------------------------------------------
# Offline / deterministic fallbacks
# ---------------------------------------------------------------------------


def offline_summary(passages: dict[str, str]) -> list[dict]:
    """Deterministic fallback — works with no AI model.

    Builds one bullet per passage from the first full sentence of that passage.
    Uses the new {text, passage_id, proof} shape (Fix #2).
    """
    bullets: list[dict] = []
    for pid, text in passages.items():
        sents = _sentences(text)
        if not sents:
            continue
        proof = sents[0]
        # Simple plain-English paraphrase: just use the first sentence as the bullet
        bullets.append({"text": proof, "passage_id": pid, "proof": proof})
    return bullets


def offline_questions(passages: dict[str, str]) -> list[dict]:
    """Deterministic fallback — multiple-choice built from key sentences.

    Blanks out an important term from a sentence and uses other key terms
    as distractors.  correct_index and proof_text are always exact.
    """
    questions: list[dict] = []
    all_key_terms: list[str] = []

    # Collect candidate key terms (capitalised words / noun-like tokens) from all passages
    for text in passages.values():
        for word in text.split():
            clean_w = re.sub(r"[^\w]", "", word)
            if len(clean_w) >= 4 and clean_w[0].isupper() and clean_w not in all_key_terms:
                all_key_terms.append(clean_w)

    for pid, text in passages.items():
        sents = _sentences(text)
        if not sents:
            continue
        # Pick the sentence with the most capitalised words as the "key" sentence
        key_sent = max(sents, key=lambda s: sum(1 for w in s.split() if w and w[0].isupper()))
        words = key_sent.split()

        # Find first 4+-letter capitalised word to blank out
        blank_word = ""
        for w in words:
            cw = re.sub(r"[^\w]", "", w)
            if len(cw) >= 4 and cw[0].isupper():
                blank_word = cw
                break

        if not blank_word:
            # fallback: use first long word
            for w in words:
                if len(re.sub(r"[^\w]", "", w)) >= 4:
                    blank_word = re.sub(r"[^\w]", "", w)
                    break

        if not blank_word:
            continue

        stem_text = key_sent.replace(blank_word, "______", 1)
        stem = f'Fill in the blank: \u201c{stem_text}\u201d'

        # Build distractors from all_key_terms excluding the correct answer
        distractors = [t for t in all_key_terms if t != blank_word][:3]
        # Pad if needed
        while len(distractors) < 3:
            distractors.append("None of the above")

        options = [blank_word, distractors[0], distractors[1], distractors[2]]
        questions.append(
            {
                "stem": stem,
                "options": options,
                "correct_index": 0,
                "passage_id": pid,
                "proof_text": key_sent,
            }
        )

    return questions


# ---------------------------------------------------------------------------
# All-in-one cached entry point  (Fix #5: concurrent AI calls)
# ---------------------------------------------------------------------------


def _text_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


@lru_cache(maxsize=32)
def _cached_study(text_hash: str, text: str, provider_name: str) -> dict:  # noqa: ARG001 (hash is the cache key)
    from lib.ai import ask

    passages = split_passages(text)

    # Run summarise and make_questions concurrently (Fix #5)
    with ThreadPoolExecutor(max_workers=2) as pool:
        f_summary = pool.submit(summarise, passages, ask)
        f_questions = pool.submit(make_questions, passages, ask)
        summary = f_summary.result()
        questions = f_questions.result()

    return {
        "passages": passages,
        "summary": summary,
        "questions": questions,
    }


def study(text: str) -> dict:
    """All-in-one entry point.  Results are cached per (text, AI_PROVIDER).

    Accepts the BODY text (after strip_metadata has been called).
    """
    import os

    provider_name = os.getenv("AI_PROVIDER", "offline")
    return _cached_study(_text_hash(text), text, provider_name)


# ---------------------------------------------------------------------------
# F2: Fingerprint check and proof-sentence highlight helper
# ---------------------------------------------------------------------------


def fingerprint_check(body_text: str, expected_fp: str) -> bool:
    """Return True if sha256(body_text[:200]) matches expected_fp.

    Args:
        body_text: The stripped body text of the loaded sample (after strip_metadata).
        expected_fp: The hex-digest string stored in samples_index.json.

    This lets the UI warn if the file on disk has been modified since the
    fingerprint was recorded.
    """
    actual = hashlib.sha256(body_text[:200].encode("utf-8")).hexdigest()
    return actual == expected_fp


def highlight_proof(passage: str, proof_sentence: str) -> str:
    """Return passage HTML with proof_sentence wrapped in <mark> for highlighting.

    If proof_sentence is not found (exact or case-insensitive), returns the
    passage with proof_sentence appended as a fallback so the UI always has
    something to show.

    Args:
        passage: The full passage text.
        proof_sentence: The exact sentence to highlight.

    Returns:
        HTML string safe for st.markdown(..., unsafe_allow_html=True).
    """
    if not proof_sentence or not passage:
        return passage or ""

    # Try exact match first
    if proof_sentence in passage:
        highlighted = passage.replace(proof_sentence, f"<mark>{proof_sentence}</mark>", 1)
        return highlighted

    # Try case-insensitive
    lower_passage = passage.lower()
    lower_proof = proof_sentence.lower()
    idx = lower_passage.find(lower_proof)
    if idx != -1:
        end = idx + len(proof_sentence)
        highlighted = passage[:idx] + f"<mark>{passage[idx:end]}</mark>" + passage[end:]
        return highlighted

    # Proof not found verbatim — return passage with proof appended
    return passage + f"\n\n*(Proof sentence: {proof_sentence})*"


# ---------------------------------------------------------------------------
# Convenience re-export for quick description
# ---------------------------------------------------------------------------

__all__ = [
    "strip_metadata",
    "split_passages",
    "summarise",
    "make_questions",
    "offline_summary",
    "offline_questions",
    "study",
    "fingerprint_check",
    "highlight_proof",
    "textwrap",  # re-exported for tests
]
