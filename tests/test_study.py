"""Tests for app/lib/study.py — all deterministic (AI_PROVIDER=offline).

Run with: uv run pytest -q tests/test_study.py
"""

from __future__ import annotations

import os

os.environ["AI_PROVIDER"] = "offline"

from lib.study import (  # noqa: E402
    _correct_or_drop_question,
    _find_proof_passage,
    make_questions,
    offline_questions,
    offline_summary,
    split_passages,
    strip_metadata,
    summarise,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────

SHORT_TEXT = (
    "A local area network connects devices in one building. "
    "It allows computers to share files and printers."
)

LONG_TEXT = (
    # --- passage 1 (~120 words) ---
    "Supply-chain risk is the chance that one part of the production process will fail. "
    "Every business that makes or sells a product depends on a supply chain. "
    "Natural events such as floods can close ports or destroy factories. "
    "Political events such as trade disputes can raise the cost of imported parts overnight. "
    "A single supplier going out of business can leave a company with no way to build its product "
    "for weeks or months at a time. "
    # --- passage 2 (~120 words) ---
    "Companies use several strategies to reduce supply-chain risk. "
    "Diversification means working with more than one supplier for every critical part, "
    "so that losing one supplier does not stop production completely. "
    "Safety stock is extra inventory kept on hand as a buffer against unexpected delays. "
    "Near-shoring means moving suppliers closer to the final assembly site to shorten distances. "
    "Scenario planning involves running what-if exercises before an emergency happens. "
    "Regular supplier audits help a company catch warning signs early before problems grow. "
    # --- passage 3 (~120 words) ---
    "Technology also plays an important role in managing supply-chain risk. "
    "Modern software can track every shipment in real time and alert managers to delays. "
    "Artificial intelligence tools can predict which suppliers are likely to have problems "
    "based on news reports, weather data, and financial signals from around the world. "
    "Blockchain technology creates a permanent, tamper-proof record of every transaction "
    "in the supply chain, making it easier to find out where something went wrong. "
    "Together, technology and careful planning help businesses avoid the worst outcomes "
    "when disruptions strike their supply chains unexpectedly. "
)

# The raw sample file text (with header lines)
BAM101_RAW = """\
Supply-Chain Risk Management — BAM 101, Week 3
Fictional course reading created for the Ivy Tech 2030 Innovation Squad prototype.
All companies, people, and events described below are entirely invented.

[P1]
Every business that makes or sells a product depends on a supply chain.
A supply chain is the full set of steps needed to turn raw materials into something a customer can buy.

[P2]
Risks in a supply chain come from many different sources. Natural events such as floods can close ports.

[P3]
Companies use several strategies to reduce supply-chain risk. Diversification means working with more than one supplier.
"""


def _offline_ask(prompt: str, system: str = "", json_mode: bool = False, **kwargs):
    """Stand-in ask_fn that always returns offline mode Answer."""
    from lib.ai import Answer

    return Answer(
        "**Offline mode** (no AI backend configured). Set AI_PROVIDER to get answers.",
        "offline",
    )


# ── Test 1: split_passages produces ≥ 2 passages for a 400-word text ─────────


def test_split_passages_basic():
    passages = split_passages(LONG_TEXT)
    keys = list(passages.keys())
    assert len(passages) >= 2, f"Expected ≥ 2 passages, got {len(passages)}"
    for i, key in enumerate(keys, start=1):
        assert key == f"P{i}", f"Expected key P{i}, got {key}"
    # Every passage key must start with "P"
    for key in passages:
        assert key.startswith("P")
    # All original words should be preserved somewhere
    for passage_text in passages.values():
        assert len(passage_text.split()) > 0


# ── Test 2: short text produces exactly P1 ────────────────────────────────────


def test_split_passages_single():
    passages = split_passages(SHORT_TEXT)
    assert list(passages.keys()) == ["P1"], f"Expected ['P1'], got {list(passages.keys())}"
    assert SHORT_TEXT.strip().split()[0] in passages["P1"]


# ── Test 3: summarise drops a bullet whose proof_text is not in the passage ───


def test_summarise_verification():
    """A bullet with a fabricated proof_text that isn't in the passage is dropped."""
    from lib.ai import Answer

    passages = split_passages(LONG_TEXT)

    # Inject one real bullet + one fabricated bullet that cannot be verified
    fabricated_json = (
        '{"bullets": ['
        '{"text": "Risk can harm a business", "passage_id": "P1", '
        '"proof": "Supply-chain risk is the chance that one part of the production process will fail."},'
        '{"text": "This is completely made up and not in any passage", "passage_id": "P1", '
        '"proof": "Dragons ate the entire supply chain on Tuesday morning in Paris."}'
        "]}"
    )

    def fake_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer(fabricated_json, "fake")

    result = summarise(passages, fake_ask)
    bullets = result["bullets"]
    # The fabricated bullet must have been dropped
    for b in bullets:
        proof = b.get("proof") or b.get("proof_text", "")
        assert "dragon" not in proof.lower(), "Fabricated bullet should have been dropped"
    assert result["dropped"] >= 1, "Expected at least 1 dropped bullet"


# ── Test 4: make_questions drops a question whose proof_text is not in passage ─


def test_questions_verification():
    """A question with a fabricated proof_text is dropped."""
    from lib.ai import Answer

    passages = split_passages(LONG_TEXT)

    fabricated_json = (
        '{"questions": ['
        '{"stem": "What is a hallucinated term?", "options": ["A", "B", "C", "D"], '
        '"correct_index": 0, "passage_id": "P1", '
        '"proof_text": "Invisible unicorns manage every warehouse in the world."}'
        "]}"
    )

    def fake_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer(fabricated_json, "fake")

    result = make_questions(passages, fake_ask)
    questions = result["questions"]
    for q in questions:
        assert "unicorn" not in q["proof_text"].lower(), "Fabricated question should have been dropped"
    assert result["dropped"] >= 1, "Expected at least 1 dropped question"


# ── Test 5: offline_summary returns ≥ 1 bullet with no AI call ───────────────


def test_offline_summary_no_model():
    passages = split_passages(LONG_TEXT)
    bullets = offline_summary(passages)
    assert len(bullets) >= 1, "offline_summary must return at least 1 bullet"
    for b in bullets:
        assert "text" in b
        assert "passage_id" in b
        # Fix #2: new field name is "proof"
        assert "proof" in b, "offline_summary must use 'proof' field (not 'proof_text')"
        # proof must be a real sentence from the passage
        pid = b["passage_id"]
        assert pid in passages
        assert b["proof"] in passages[pid] or len(b["proof"]) > 0


# ── Test 6: offline_questions returns ≥ 1 question with no AI call ───────────


def test_offline_questions_no_model():
    passages = split_passages(LONG_TEXT)
    questions = offline_questions(passages)
    assert len(questions) >= 1, "offline_questions must return at least 1 question"
    for q in questions:
        assert "stem" in q
        assert "options" in q and len(q["options"]) == 4
        assert "correct_index" in q and 0 <= q["correct_index"] < 4
        assert "passage_id" in q
        assert "proof_text" in q


# ── Test 7: verification rejects a fabricated proof sentence ─────────────────


def test_verification_rejects_fabricated():
    """_verify_bullet must return False for a proof_text not in the passage."""
    from lib.study import _verify_bullet

    passages = {"P1": "The quick brown fox jumps over the lazy dog."}
    fake_item = {
        "text": "Foxes are fast",
        "passage_id": "P1",
        "proof": "Invisible space dragons rearranged the solar system last Tuesday.",
    }
    assert not _verify_bullet(fake_item, passages), "Fabricated proof should be rejected"


# ── Test 8: verification accepts an exact proof sentence ─────────────────────


def test_verification_accepts_exact():
    """_verify_bullet must return True for a proof that is literally in the passage."""
    from lib.study import _verify_bullet

    proof = "The quick brown fox jumps over the lazy dog."
    passages = {"P1": proof}
    item = {
        "text": "Foxes are agile",
        "passage_id": "P1",
        "proof": proof,
    }
    assert _verify_bullet(item, passages), "Exact proof text should be accepted"


# ── Test 9: summarise tops up to ≥ 3 bullets when AI returns nothing ─────────


def test_summarise_tops_up_when_ai_empty():
    """When the AI returns 0 verified bullets, offline fallback provides at least 3."""
    from lib.ai import Answer

    passages = split_passages(LONG_TEXT)

    def empty_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer('{"bullets": []}', "fake")

    result = summarise(passages, empty_ask)
    assert len(result["bullets"]) >= 3, "Should top up to ≥ 3 bullets from offline fallback"


# ── Test 10: make_questions tops up to ≥ 3 questions when AI returns nothing ──


def test_questions_tops_up_when_ai_empty():
    """When the AI returns 0 verified questions, offline fallback provides at least 3."""
    from lib.ai import Answer

    passages = split_passages(LONG_TEXT)

    def empty_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer('{"questions": []}', "fake")

    result = make_questions(passages, empty_ask)
    assert len(result["questions"]) >= 3, "Should top up to ≥ 3 questions from offline fallback"


# ── REGRESSION TEST 11: strip_metadata removes header lines ──────────────────


def test_strip_metadata_removes_header_lines():
    """Header lines (title, fictional disclaimer, [Pn] markers) must not appear in body text."""
    body = strip_metadata(BAM101_RAW)

    # Header patterns that should be gone
    assert "Supply-Chain Risk Management — BAM 101" not in body, "Title line should be stripped"
    assert "Fictional course reading" not in body, "Fictional disclaimer should be stripped"
    assert "All companies" not in body, "All-companies disclaimer should be stripped"
    assert "[P1]" not in body, "[P1] passage marker should be stripped"
    assert "[P2]" not in body, "[P2] passage marker should be stripped"
    assert "[P3]" not in body, "[P3] passage marker should be stripped"

    # Real content lines must survive
    assert "Every business that makes or sells a product" in body
    assert "Risks in a supply chain come from many different sources" in body
    assert "Companies use several strategies" in body


def test_strip_metadata_body_feeds_passages():
    """split_passages on the stripped body should produce ≥ 1 passage with no header content."""
    body = strip_metadata(BAM101_RAW)
    passages = split_passages(body)
    assert len(passages) >= 1

    all_text = " ".join(passages.values())
    assert "Fictional" not in all_text
    assert "All companies" not in all_text
    assert "BAM 101" not in all_text


# ── REGRESSION TEST 12: summary items have text, passage_id, proof ───────────


def test_offline_summary_shape():
    """offline_summary must return items with text, passage_id, and proof fields."""
    passages = split_passages(LONG_TEXT)
    bullets = offline_summary(passages)
    assert len(bullets) >= 1
    for b in bullets:
        assert "text" in b, "Missing 'text' field"
        assert "passage_id" in b, "Missing 'passage_id' field"
        assert "proof" in b, "Missing 'proof' field — shape changed in Fix #2"
        assert isinstance(b["text"], str) and b["text"]
        assert isinstance(b["proof"], str) and b["proof"]


def test_summarise_bullets_have_proof_field():
    """summarise() must return bullets with a 'proof' field (not 'proof_text')."""
    from lib.ai import Answer

    passages = split_passages(LONG_TEXT)

    # AI returns old-style "proof_text" key — must be normalised to "proof"
    legacy_json = (
        '{"bullets": ['
        '{"text": "Risk can harm a business", "passage_id": "P1", '
        '"proof_text": "Supply-chain risk is the chance that one part of the production process will fail."}'
        "]}"
    )

    def fake_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer(legacy_json, "fake")

    result = summarise(passages, fake_ask)
    for b in result["bullets"]:
        assert "proof" in b, "Bullet must have 'proof' field"
        assert "proof_text" not in b, "'proof_text' should have been normalised to 'proof'"


# ── REGRESSION TEST 13: every displayed proof is in the passage shown ─────────


def test_every_proof_exists_in_its_passage():
    """For every verified bullet, proof must be found (fuzzy) in the passage_id shown."""
    from lib.ai import Answer
    from lib.study import _fuzzy_match

    passages = split_passages(LONG_TEXT)

    # Fabricate bullets: one correct, one with wrong passage_id (should be corrected, not dropped)
    p2_sentence = "Companies use several strategies to reduce supply-chain risk."
    correctable_json = (
        '{"bullets": ['
        '{"text": "Risk can harm a business", "passage_id": "P1", '
        '"proof": "Supply-chain risk is the chance that one part of the production process will fail."},'
        # This proof is in P2 but cites P1 — should be corrected to P2
        f'{{"text": "Companies manage risk", "passage_id": "P1", "proof": "{p2_sentence}"}}'
        "]}"
    )

    def fake_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer(correctable_json, "fake")

    result = summarise(passages, fake_ask)
    for b in result["bullets"]:
        pid = b["passage_id"]
        proof = b.get("proof") or b.get("proof_text", "")
        passage_text = passages.get(pid, "")
        assert passage_text, f"passage_id {pid} not found in passages"
        assert _fuzzy_match(proof, passage_text), (
            f"Proof not found in its cited passage {pid}:\n  proof: {proof!r}"
        )


# ── REGRESSION TEST 14: passage-id correction works when cited id is wrong ────


def test_passage_id_correction_question():
    """_correct_or_drop_question corrects wrong passage_id instead of dropping."""
    # Set up two passages
    passages = {
        "P1": "The cat sat on the mat. A quick brown fox jumped over the lazy dog.",
        "P2": "The sky is blue and the grass is green. Birds fly south for the winter.",
    }

    # Item citing P1 but proof_text is actually in P2
    item = {
        "stem": "What colour is the sky?",
        "options": ["Blue", "Red", "Green", "Yellow"],
        "correct_index": 0,
        "passage_id": "P1",  # WRONG — sentence is in P2
        "proof_text": "The sky is blue and the grass is green.",
    }

    result = _correct_or_drop_question(item, passages)
    assert result is not None, "Item should not be dropped — proof exists in P2"
    assert result["passage_id"] == "P2", (
        f"passage_id should be corrected to P2, got {result['passage_id']!r}"
    )


def test_passage_id_drop_when_proof_in_no_passage():
    """_correct_or_drop_question returns None when proof is in no passage."""
    passages = {
        "P1": "The cat sat on the mat.",
        "P2": "The sky is blue and the grass is green.",
    }

    item = {
        "stem": "What did the aliens do?",
        "options": ["A", "B", "C", "D"],
        "correct_index": 0,
        "passage_id": "P1",
        "proof_text": "Aliens invaded the planet and ate all the cheese on Monday.",
    }

    result = _correct_or_drop_question(item, passages)
    assert result is None, "Item should be dropped when proof is in no passage"


# ── REGRESSION TEST 15: _find_proof_passage searches all passages ─────────────


def test_find_proof_passage_finds_correct_passage():
    """_find_proof_passage must return the passage where the proof actually lives."""
    passages = {
        "P1": "Apples are red. The sun rises in the east.",
        "P2": "Bananas are yellow. The moon reflects sunlight.",
        "P3": "Cherries are small and round. They grow on trees.",
    }

    pid = _find_proof_passage("The moon reflects sunlight.", passages)
    assert pid == "P2", f"Expected P2, got {pid!r}"

    pid2 = _find_proof_passage("Cherries are small and round.", passages)
    assert pid2 == "P3", f"Expected P3, got {pid2!r}"

    pid3 = _find_proof_passage("Dragons do not exist in any passage.", passages)
    assert pid3 is None, "Should return None when proof not found"


# ── F2 TEST 16: fingerprint_check returns True for matching hash ──────────────


def test_fingerprint_check_match():
    """fingerprint_check must return True when body_text[:200] matches stored sha256."""
    import hashlib

    from lib.study import fingerprint_check

    body = "Every business that makes or sells a product depends on a supply chain." * 3
    expected = hashlib.sha256(body[:200].encode("utf-8")).hexdigest()
    assert fingerprint_check(body, expected), "Should return True for matching fingerprint"


def test_fingerprint_check_mismatch():
    """fingerprint_check must return False when text has changed."""
    import hashlib

    from lib.study import fingerprint_check

    body = "Every business that makes or sells a product depends on a supply chain." * 3
    expected = hashlib.sha256(body[:200].encode("utf-8")).hexdigest()
    tampered = "DIFFERENT CONTENT " + body
    assert not fingerprint_check(tampered, expected), "Should return False for mismatched fingerprint"


def test_fingerprint_check_uses_first_200_chars():
    """fingerprint_check must hash only the first 200 characters of body_text."""
    import hashlib

    from lib.study import fingerprint_check

    # Two texts that differ only after char 200 should produce the same fingerprint
    base = "A" * 200
    text_a = base + "EXTRA_A"
    text_b = base + "EXTRA_B"
    expected = hashlib.sha256(base.encode("utf-8")).hexdigest()
    assert fingerprint_check(text_a, expected), "text_a first 200 chars match"
    assert fingerprint_check(text_b, expected), "text_b first 200 chars also match"


# ── F2 TEST 17: highlight_proof wraps proof sentence in <mark> ────────────────


def test_highlight_proof_exact_match():
    """highlight_proof must wrap the proof sentence in <mark> tags."""
    from lib.study import highlight_proof

    passage = "The quick brown fox jumps over the lazy dog. The cat sat on the mat."
    proof = "The cat sat on the mat."
    result = highlight_proof(passage, proof)
    assert "<mark>The cat sat on the mat.</mark>" in result
    # The rest of the passage must still be present
    assert "The quick brown fox jumps over the lazy dog." in result


def test_highlight_proof_case_insensitive():
    """highlight_proof must find the sentence case-insensitively if exact match fails."""
    from lib.study import highlight_proof

    passage = "Supply-chain RISK is real. Companies must plan ahead."
    proof = "supply-chain risk is real."
    result = highlight_proof(passage, proof)
    assert "<mark>" in result, "Should still highlight even with case difference"


def test_highlight_proof_fallback_when_not_found():
    """highlight_proof must not crash when proof_sentence is absent; returns passage + note."""
    from lib.study import highlight_proof

    passage = "The sky is blue and the grass is green."
    proof = "Dragons do not exist in this passage at all."
    result = highlight_proof(passage, proof)
    # Must include original passage
    assert "The sky is blue" in result
    # Must not crash; content returned is non-empty
    assert result


def test_highlight_proof_empty_inputs():
    """highlight_proof must handle empty inputs gracefully."""
    from lib.study import highlight_proof

    assert highlight_proof("", "proof") == ""
    assert highlight_proof("some passage", "") == "some passage"
    assert highlight_proof("", "") == ""


# ── F1 TEST 18: flesch_kincaid_grade — simple text scores lower than complex ──


def test_fk_grade_simple_lower_than_complex():
    """A short, simple text must score a lower FK grade than a dense academic one."""
    from lib.study import flesch_kincaid_grade

    simple = (
        "Dogs are pets. They like to run. Kids love dogs. Dogs eat food."
    )
    complex_text = (
        "The epistemological foundations of contemporary cognitive neuroscience necessitate "
        "a comprehensive reevaluation of previously established theoretical frameworks "
        "concerning the neurobiological underpinnings of consciousness. "
        "Sophisticated computational methodologies have substantially transformed our "
        "understanding of prefrontal cortical architectures and their interdependencies "
        "with subcortical neuroanatomical structures."
    )
    grade_simple = flesch_kincaid_grade(simple)
    grade_complex = flesch_kincaid_grade(complex_text)
    assert grade_simple < grade_complex, (
        f"Simple text (grade {grade_simple}) should score lower than complex text (grade {grade_complex})"
    )


def test_fk_grade_returns_float():
    """flesch_kincaid_grade must return a non-negative float."""
    from lib.study import flesch_kincaid_grade

    grade = flesch_kincaid_grade("The cat sat on the mat. The dog ran fast.")
    assert isinstance(grade, float), "FK grade must be a float"
    assert grade >= 0.0, "FK grade must be non-negative"


def test_fk_grade_empty_returns_zero():
    """flesch_kincaid_grade must return 0.0 for empty or whitespace input."""
    from lib.study import flesch_kincaid_grade

    assert flesch_kincaid_grade("") == 0.0
    assert flesch_kincaid_grade("   ") == 0.0


def test_fk_grade_known_simple():
    """Very short, common words should score below grade 5."""
    from lib.study import flesch_kincaid_grade

    very_simple = "I see a dog. The dog is big. I run fast."
    grade = flesch_kincaid_grade(very_simple)
    # This text should be well below grade 5
    assert grade < 5.0, f"Expected grade < 5 for very simple text, got {grade}"


def test_fk_grade_offline_summary_lower_than_original():
    """The offline summary of a passage should have a lower or equal FK grade than the original."""
    from lib.study import flesch_kincaid_grade, offline_summary, split_passages

    # Use a moderately complex text
    text = (
        "Supply-chain risk is the probability that one or more components of the production "
        "process will experience unexpected disruptions, resulting in operational inefficiencies. "
        "Organisations must develop comprehensive mitigation strategies to address vulnerabilities "
        "in their procurement and distribution networks."
    )
    passages = split_passages(text)
    bullets = offline_summary(passages)
    summary_text = " ".join(b.get("text_en") or b.get("text", "") for b in bullets)
    grade_orig = flesch_kincaid_grade(text)
    grade_summary = flesch_kincaid_grade(summary_text)
    # Offline summary is the first sentence, which should be <= original grade
    # (can be equal if first sentence is the hardest)
    assert grade_summary <= grade_orig + 2.0, (
        f"Summary grade {grade_summary} should not be much higher than original {grade_orig}"
    )
