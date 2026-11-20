# Build Plan — Part 2: Alternative-Format Study Tool

**Case:** Case 2 · **Pillar:** Academic & Instructional Quality  
**Persona:** Lena — online working adult, ESL, phone-only, 11 pm–1 am study window  
**Stack:** Python 3.12, Streamlit, uv · AI: `app/lib/ai.py` (granite / claude / offline)

---

## Overview

Rebuild `app/Home.py` into a mobile-first, single-scroll study screen. The app accepts a course
reading, splits it into numbered passages, generates a plain-language summary and practice
questions whose every bullet and answer is verified against the source text, and shows a
leading-indicator dashboard. No data leaves the device (Granite runs locally via Ollama).
The existing `app/pages/4_Impact.py` is kept untouched for the metric visualisation.

---

## Key design decisions

### 1. Mobile-first, dark-themed single screen
- One vertical page — no tabs, no sidebar navigation to click through.
- Dark background (`#0e1117`), body font ≥ 16 px, full-width layout to avoid horizontal scroll
  on a 390 px phone viewport.
- Sparse copy; every label is in plain language (no jargon).
- Rationale: Lena studies on a phone after 11 pm; brightness and scrolling friction matter.

### 2. Passage splitting and citation
- The reading is split into numbered passages **P1 … Pn** (one paragraph or ~150 words each).
- Every summary bullet and every practice question must end with a `[Px]` citation tag.
- **Verification rule:** before displaying a bullet or question, `app/lib/study.py` checks
  that a key phrase from the generated text actually appears (case-insensitive substring match)
  in the named passage. Items that fail this check are silently dropped.
- This is the technical implementation of the A-Ivy requirement: "Ground answers in approved sources."
- Rationale: prevents hallucinated bullets from reaching the student; the judge can see the
  citation and verify it live during the demo.

### 3. Offline fallback that always works
- When `AI_PROVIDER=offline` or the Granite server is unreachable, `study.py` returns a
  hardcoded deterministic summary and question set for each sample reading.
- The demo never crashes; the fallback is clearly labelled as offline mode.

### 4. Privacy
- Sample readings only — made-up content in `samples/`; no real course materials, no student data.
- Nothing is written to disk or a database; all state lives in Streamlit `session_state`.
- Granite runs locally (Ollama); nothing is sent to any external server unless `AI_PROVIDER=claude`.
- No names, IDs, or identifiers in any AI prompt.

### 5. Designed for small later additions
Each planned extension is a contained change:
| Future feature | Where the change goes |
|---|---|
| Reading-level / plain-English toggle | Add `simplify(text, level)` to `study.py`; add one radio button to `Home.py` |
| Spanish language toggle | Add `translate(bullets, lang)` to `study.py`; add one toggle to `Home.py` |
| "Get help from a person" path | Add a modal / expander to `Home.py`; no library changes needed |
| Visible source-proof panel | Render passage text inline when user clicks a `[Px]` label; already available via `passages` dict |
| Session metrics persistence | Replace `session_state` accumulator with an append-only local JSON in `data/` |

---

## Repository layout after Part 2

```
app/
  Home.py                  ← rebuilt as the study screen (replaces the data-dashboard landing page)
  lib/
    ai.py                  ← unchanged (granite / claude / offline backends)
    study.py               ← NEW: passages, summarise, questions, verify, offline fallback
    config.py              ← update PRODUCT_NAME, PERSONA, PILLAR, OUTCOME_METRIC, TAGLINE
    charts.py              ← unchanged
    data.py                ← unchanged
    ml.py                  ← unchanged
    ui.py                  ← unchanged (page() helper reused)
  pages/
    4_Impact.py            ← unchanged (metric visualisation)
    1_Explore.py           ← unchanged (kept for judges)
    2_Predict.py           ← unchanged
    3_Assistant.py         ← unchanged
samples/
  bam101_week3.txt         ← NEW: made-up Business Admin reading (supply-chain risk, ~400 words)
  cit110_week1.txt         ← NEW: made-up IT Foundations reading (networking basics, ~400 words)
  samples_index.json       ← NEW: metadata {course, week, title, assigned_by} for each sample
```

---

## `app/lib/study.py` — module contract

```python
# Public API — implementation in Part 2 by agent mode

def split_passages(text: str) -> dict[str, str]:
    """Split raw text into {P1: ..., P2: ..., ...} dict. ~150 words per passage."""

def summarise(passages: dict[str, str], ask_fn) -> list[dict]:
    """Return verified summary bullets: [{text: str, passage_id: str}].
    Drops bullets whose key phrase is not found in the named passage."""

def make_questions(passages: dict[str, str], ask_fn) -> list[dict]:
    """Return verified MCQ list: [{stem, options[4], correct_index, passage_id, proof_text}].
    Drops questions whose proof_text is not found in the named passage."""

def offline_summary(passages: dict[str, str]) -> list[dict]:
    """Deterministic fallback — works with no AI model."""

def offline_questions(passages: dict[str, str]) -> list[dict]:
    """Deterministic fallback — works with no AI model."""
```

---

## `app/Home.py` — screen layout (wireframe)

```
┌─────────────────────────────────────┐
│  📖  StudyBuddy                     │
│  Plain-language study, any hour     │
├─────────────────────────────────────┤
│  Course: [dropdown ▾]  Week: [1 ▾] │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  Paste your reading here …   │  │
│  └───────────────────────────────┘  │
│          [ Summarise ]              │
├─────────────────────────────────────┤
│  Summary                            │
│  • Key idea one [P1]                │
│  • Key idea two [P2]                │
│  • Key idea three [P3]              │
│          [ Practice ]               │
├─────────────────────────────────────┤
│  Practice questions                 │
│  Q1. … [P1]                         │
│    ○ A   ○ B   ○ C   ○ D            │
│  [Check answer]  → Proof: "…" [P1] │
├─────────────────────────────────────┤
│  Tonight's stats  |  🕐 Late-night  │
│  Accuracy: 2/3    |  sets: 1        │
│  [Ask a person →]                   │
└─────────────────────────────────────┘
```

---

## Sample readings (`samples/`)

Each `.txt` file is entirely made-up content written for the prototype. The
`samples_index.json` carries metadata so the UI can populate the course/week pickers without
any real course data.

**bam101_week3.txt** — "Supply-Chain Risk Management" (~400 words, 3 passages P1–P3)  
**cit110_week1.txt** — "Introduction to Networking" (~400 words, 3 passages P1–P3)

---

## Team split (4 members, no file conflicts)

| Member | Files owned | Deliverable |
|---|---|---|
| **A — Roshan** | `app/lib/study.py` (new), `samples/` (new) | Core library: `split_passages`, `summarise`, `make_questions`, verification logic, offline fallbacks; write 2 sample readings and `samples_index.json` |
| **B — Member 2** | `app/Home.py` | Study screen UI: dark theme, text area, dropdowns, summary render with [Px] labels, practice Q render with proof reveal, stats row |
| **C — Member 3** | `app/lib/config.py` | Update `PRODUCT_NAME`, `TAGLINE`, `PERSONA`, `PILLAR`, `OUTCOME_METRIC`, `OUTCOME_BASELINE`, `OUTCOME_TARGET` to match our case |
| **D — Member 4** | `tests/test_study.py` (new), `docs/BOB_LOG.md`, `README.md` | Write tests for `split_passages` and the verification rule; keep BOB_LOG current; draft README sections |

> Member A starts first (study.py is a dependency of Home.py). B can begin on the UI scaffold
> against a stub import while A finishes. C and D are independent and can run in parallel.

---

## Test plan

| Test | What it checks | File |
|---|---|---|
| `test_split_passages_basic` | 400-word text produces ≥ 2 passages keyed P1, P2, … | `tests/test_study.py` |
| `test_split_passages_single` | Text < 150 words produces exactly P1 | `tests/test_study.py` |
| `test_summarise_verification` | Bullet whose phrase is absent from its passage is dropped | `tests/test_study.py` |
| `test_questions_verification` | Question whose proof_text is absent is dropped | `tests/test_study.py` |
| `test_offline_summary_no_model` | `offline_summary()` returns ≥ 1 bullet with no AI call | `tests/test_study.py` |
| `test_offline_questions_no_model` | `offline_questions()` returns ≥ 1 question with no AI call | `tests/test_study.py` |
| **Manual smoke test** | Open on iPhone / Android Chrome at 390 px width; confirm dark bg, no h-scroll, all buttons reachable | Demo checklist |
| **Offline demo test** | Set `AI_PROVIDER=offline`; confirm full flow completes without error | Demo checklist |

Run with: `uv run pytest -q tests/test_study.py`  
Lint with: `uv run ruff check app tests`

---

## Part 2 task checklist

- [x] **A** Create `app/lib/study.py` with `split_passages`, `summarise`, `make_questions`, verification logic, `offline_summary`, `offline_questions`
- [x] **A** Create `samples/bam101_week3.txt` (made-up supply-chain reading, ~400 words)
- [x] **A** Create `samples/cit110_week1.txt` (made-up networking reading, ~400 words)
- [x] **A** Create `samples/samples_index.json` with course/week/title/assigned_by for each sample
- [x] **C** Update `app/lib/config.py`: PRODUCT_NAME="StudyBuddy", TAGLINE, PERSONA, PILLAR, OUTCOME_METRIC, OUTCOME_BASELINE=62.0, OUTCOME_TARGET=70.0
- [x] **B** Rewrite `app/Home.py` as the study screen: dark theme CSS, course/week pickers, text area, Summarise button, summary render, Practice button, question render with proof reveal, stats row, "Ask a person" placeholder
- [x] **D** Create `tests/test_study.py` with all six unit tests from the test plan (extended to 10 tests)
- [x] **D** Confirm `uv run pytest -q` and `uv run ruff check app tests` pass with no errors
- [x] **D** Append BOB_LOG row for Part 2 work
- [ ] **Any** Manual smoke test on mobile viewport; offline demo test with `AI_PROVIDER=offline`
