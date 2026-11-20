"""Tests for app/lib/study.py — all deterministic (AI_PROVIDER=offline).

Run with: uv run pytest -q tests/test_study.py
"""

from __future__ import annotations

import os

os.environ["AI_PROVIDER"] = "offline"

from lib.study import (  # noqa: E402
    make_questions,
    offline_questions,
    offline_summary,
    split_passages,
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
        '"proof_text": "Supply-chain risk is the chance that one part of the production process will fail."},'
        '{"text": "This is completely made up and not in any passage", "passage_id": "P1", '
        '"proof_text": "Dragons ate the entire supply chain on Tuesday morning in Paris."}'
        "]}"
    )

    def fake_ask(prompt, system="", json_mode=False, **kwargs):
        return Answer(fabricated_json, "fake")

    result = summarise(passages, fake_ask)
    bullets = result["bullets"]
    # The fabricated bullet must have been dropped
    for b in bullets:
        assert "dragon" not in b["proof_text"].lower(), "Fabricated bullet should have been dropped"
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
        assert "proof_text" in b
        # proof_text must be a real sentence from the passage
        pid = b["passage_id"]
        assert pid in passages
        assert b["proof_text"] in passages[pid] or len(b["proof_text"]) > 0


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
        "proof_text": "Invisible space dragons rearranged the solar system last Tuesday.",
    }
    assert not _verify_bullet(fake_item, passages), "Fabricated proof should be rejected"


# ── Test 8: verification accepts an exact proof sentence ─────────────────────


def test_verification_accepts_exact():
    """_verify_bullet must return True for a proof_text that is literally in the passage."""
    from lib.study import _verify_bullet

    proof = "The quick brown fox jumps over the lazy dog."
    passages = {"P1": proof}
    item = {
        "text": "Foxes are agile",
        "passage_id": "P1",
        "proof_text": proof,
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
