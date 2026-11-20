"""Smoke test for F1: level=Simple, language=Spanish on bam101_week3.txt.

Usage:
    uv run python scripts/smoke_f1.py
"""

from __future__ import annotations

import os
import pathlib
import sys

# Make app/lib importable
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "app"))

from lib.ai import ask  # noqa: E402
from lib.study import (  # noqa: E402
    flesch_kincaid_grade,
    make_questions,
    split_passages,
    strip_metadata,
    summarise,
)

SAMPLE = pathlib.Path(__file__).parent.parent / "samples" / "bam101_week3.txt"

raw = SAMPLE.read_text(encoding="utf-8")
body = strip_metadata(raw)
passages = split_passages(body)

print(f"\nAI_PROVIDER: {os.getenv('AI_PROVIDER', '(auto)')}")
print(f"Passages: {list(passages.keys())}\n")

# FK grade of original
grade_before = flesch_kincaid_grade(body)
print(f"FK grade BEFORE (original body): {grade_before}")

# Run Simple/Spanish summary
print("\nRunning summarise(level=Simple, language=Spanish)…")
sum_result = summarise(passages, ask, level="Simple", language="Spanish")
bullets = sum_result["bullets"]
backend = sum_result["backend"]
dropped = sum_result["dropped"]

en_summary = " ".join(b.get("text_en") or b.get("text", "") for b in bullets)
grade_after = flesch_kincaid_grade(en_summary)

print(f"FK grade AFTER  (English summary): {grade_after}")
print(f"Grade reduction: {grade_before} → {grade_after}")

# Run questions to check verified counts
print("\nRunning make_questions(level=Simple, language=Spanish)…")
q_result = make_questions(passages, ask, level="Simple", language="Spanish")
questions = q_result["questions"]
q_dropped = q_result["dropped"]
verified_count = len(questions)
with_proof = sum(1 for q in questions if q.get("proof_text", "").strip())

print(f"Questions verified: {verified_count} of {verified_count + q_dropped} (dropped {q_dropped})")
print(f"With proof_text: {with_proof} of {verified_count}")
print(f"Backend: {backend}")

print("\n── 2 example bullets (ES + EN) ──────────────────────────────────")
for b in bullets[:2]:
    print(f"  ES: {b.get('text', '')}")
    print(f"  EN: {b.get('text_en', b.get('text', ''))}")
    print(f"  proof: {b.get('proof', '')[:80]}…")
    print()
