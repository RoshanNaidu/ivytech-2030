"""study.py — passage splitting, AI summarisation/questions, verification, offline fallbacks.

Public API
----------
split_passages(text)       -> dict[str, str]           {P1: ..., P2: ...}
summarise(passages, ask_fn)-> list[dict]               [{text, passage_id}]
make_questions(passages, ask_fn) -> list[dict]         [{stem, options, correct_index, passage_id, proof_text}]
offline_summary(passages)  -> list[dict]
offline_questions(passages)-> list[dict]
study(text, ask_fn)        -> dict  (all-in-one, cached by text hash)
"""

from __future__ import annotations

import hashlib
import json
import re
import textwrap
from collections.abc import Callable
from difflib import SequenceMatcher
from functools import lru_cache

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


def _verify_bullet(item: dict, passages: dict[str, str]) -> bool:
    """Return True if item["proof_text"] or item["text"] can be found in the named passage."""
    pid = item.get("passage_id", "")
    passage = passages.get(pid, "")
    if not passage:
        return False
    probe = item.get("proof_text") or item.get("text", "")
    return _fuzzy_match(probe, passage)


def _verify_question(item: dict, passages: dict[str, str]) -> bool:
    """Return True if item["proof_text"] can be found in the named passage."""
    pid = item.get("passage_id", "")
    passage = passages.get(pid, "")
    if not passage:
        return False
    proof = item.get("proof_text", "")
    return _fuzzy_match(proof, passage)


# ---------------------------------------------------------------------------
# AI summarisation
# ---------------------------------------------------------------------------

_SUMMARISE_SYSTEM = (
    "You are a plain-language tutor helping adult students who are English-language learners. "
    "Use ONLY the passages provided. Write in simple, clear English (aim for 8th-grade level). "
    "For every bullet, cite the passage id (e.g. P1) where the idea comes from. "
    "Copy the proof sentence WORD-FOR-WORD from that passage. "
    "Return ONLY valid JSON: "
    '{"bullets": [{"text": "...", "passage_id": "P1", "proof_text": "...exact sentence..."}, ...]}'
)

_QUESTIONS_SYSTEM = (
    "You are a plain-language tutor creating multiple-choice practice questions for adult students "
    "who are English-language learners. "
    "Use ONLY the passages provided. Write in simple, clear English. "
    "For every question, cite the passage id and copy the proof sentence WORD-FOR-WORD from that passage. "
    "Return ONLY valid JSON: "
    '{"questions": [{"stem": "...", "options": ["A", "B", "C", "D"], "correct_index": 0, '
    '"passage_id": "P1", "proof_text": "...exact sentence..."}, ...]}'
)


def _passages_prompt(passages: dict[str, str]) -> str:
    parts = [f"[{pid}] {text}" for pid, text in passages.items()]
    return "\n\n".join(parts)


def summarise(passages: dict[str, str], ask_fn: Callable) -> dict:
    """Return verified summary bullets + metadata.

    Returns:
        {
          "bullets": [{"text": str, "passage_id": str, "proof_text": str}],
          "dropped": int,
          "backend": str,
        }
    """
    prompt = (
        "Summarise the following reading in 3–5 bullet points. "
        "Plain English only. Each bullet must end with the passage id it came from.\n\n"
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
        if _verify_bullet(item, passages):
            verified.append(item)
        else:
            dropped += 1

    # Top up from offline if fewer than 3 verified bullets
    if len(verified) < 3:
        fallback = offline_summary(passages)
        existing_pids = {b["passage_id"] for b in verified}
        for b in fallback:
            if b["passage_id"] not in existing_pids:
                verified.append(b)
            if len(verified) >= 3:
                break

    return {"bullets": verified, "dropped": dropped, "backend": backend}


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
        "Create 3 multiple-choice questions from the following reading. "
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
        if _verify_question(item, passages):
            verified.append(item)
        else:
            dropped += 1

    # Top up from offline if fewer than 3 verified questions
    if len(verified) < 3:
        fallback = offline_questions(passages)
        for q in fallback:
            if len(verified) >= 3:
                break
            verified.append(q)

    return {"questions": verified[:5], "dropped": dropped, "backend": backend}


# ---------------------------------------------------------------------------
# Offline / deterministic fallbacks
# ---------------------------------------------------------------------------


def offline_summary(passages: dict[str, str]) -> list[dict]:
    """Deterministic fallback — works with no AI model.

    Builds one bullet per passage from the first full sentence of that passage.
    """
    bullets: list[dict] = []
    for pid, text in passages.items():
        sents = _sentences(text)
        if not sents:
            continue
        proof = sents[0]
        # Simple plain-English paraphrase: just use the first sentence as the bullet
        bullets.append({"text": proof, "passage_id": pid, "proof_text": proof})
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
# All-in-one cached entry point
# ---------------------------------------------------------------------------


def _text_hash(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


@lru_cache(maxsize=32)
def _cached_study(text_hash: str, text: str, provider_name: str) -> dict:  # noqa: ARG001 (hash is the cache key)
    from lib.ai import ask

    passages = split_passages(text)
    summary = summarise(passages, ask)
    questions = make_questions(passages, ask)
    return {
        "passages": passages,
        "summary": summary,
        "questions": questions,
    }


def study(text: str) -> dict:
    """All-in-one entry point.  Results are cached per (text, AI_PROVIDER)."""
    import os

    provider_name = os.getenv("AI_PROVIDER", "offline")
    return _cached_study(_text_hash(text), text, provider_name)


# ---------------------------------------------------------------------------
# Convenience re-export for quick description
# ---------------------------------------------------------------------------

__all__ = [
    "split_passages",
    "summarise",
    "make_questions",
    "offline_summary",
    "offline_questions",
    "study",
    "textwrap",  # re-exported for tests
]
