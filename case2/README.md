# Case 2 — Study Shift: Alternative-Format Study Tool

A mobile-first web prototype for **Ivy Tech BIOL 101** that walks a student through:
**select material → quick review → key terms → practice question → reveal answer with source**

Designed for a student who studies on her phone after hours.

**Strategic pillar:** Student-Centered Journey  
**Working title:** Study Shift

---

## Problem, solution, and strategy

**Problem:** Students studying late at night — often on a phone, often without fast Wi-Fi — have no way to quickly review assigned materials, check key terms in plain language or Spanish, or test themselves with feedback that cites actual course sources.

**Solution:** Study Shift delivers assigned BIOL 101 readings and lecture notes in three study views (Quick review, Key terms, Practice) in a single offline-capable mobile page. When AI is unavailable the app falls back to deterministic local content without breaking and labels everything clearly so students always know what they are reading.

**Pillar and 2030 strategy:** Student-Centered Journey — reduce barriers to learning outside the classroom. Measurable outcome: increase self-reported out-of-class study time for evening/online students; reduce drop rates for gateway science courses.

---

## Technical approach

| Layer | Detail |
|-------|--------|
| Runtime | Zero-dependency single HTML file + one ES module data file. No build step, no bundler, no npm. Works offline after first load. |
| Data | `case_data.js` exports `MATERIALS`, `QUESTION_BANK`, `KEY_TERMS`, `KEY_TERMS_ES`, `PLAIN_ENGLISH_BULLETS`, `HELP_OPTIONS`. All invented from course-realistic BIOL 101 content; will be replaced by real data/CSVs on challenge day. |
| AI integration | `callAI(prompt)` stub at line ~483 of `index.html`. Throws today → triggers sample mode. Replace the body with a `fetch` to any compatible endpoint (Claude, Granite via Ollama, or the team's `app/lib/ai.py` backend). |
| Sample mode fallback | Every content-generating function catches the AI error and falls back to local data. A gold "⚠ Sample content" badge appears in the header; each panel shows an amber notice with the specific reason. |
| Assignment flag | `assigned_by_instructor: true/false` on each material. The picker only shows `true` entries. M06 and M10 (and M07–M09) are catalogue-only and cannot appear in the study flow. |
| Reading level | "Plain English" bullets are deterministic local text in `PLAIN_ENGLISH_BULLETS`. No AI call. Toggles do not reset between materials. |
| Glossary language | `KEY_TERMS_ES` holds sample Spanish definitions for M01–M05 only. Labeled as unverified sample translations. |
| Answer provenance | `excerptVerified()` checks every question's `source_excerpt` against the material `source_text` before showing "View source". If the check fails, no excerpt is shown. |
| Help | `HELP_OPTIONS` mirrors the schema of `help_options.csv`. Portal routes without a live URL show step-by-step directions instead of a dead link. |

---

## Files

| File | Purpose |
|------|---------|
| `case2/index.html` | Complete app: all CSS, HTML, and JS in one ES-module file |
| `case2/case_data.js` | All course data: materials, questions, terms, Spanish glossary, help options |
| `case2/case2_data_test.py` | 104-assertion Python data integrity test suite |
| `case2/case2.test.js` | Node.js mirror of the same tests (requires Node ≥ 18) |
| `case2/README.md` | This file |

---

## Launch steps

> **ES modules require HTTP** — browsers block `import` on `file://` URLs.
> Always serve from a local HTTP server.

```bash
# From the project root:
python3 -m http.server 8080 --directory case2
```

Then open: **http://localhost:8080**

For a phone-sized viewport in Chrome/Edge/Firefox DevTools: open DevTools → Toggle device toolbar → set to 390 × 844 px (iPhone 14) or 360 × 780 px (Android).

**Do not** open `index.html` by double-clicking. The ES module import will silently fail on `file://`.

---

## Tested demo path

> These steps match the actual runtime data in `case_data.js`.
> Steps verified against source code and HTTP 200 server response.
> Browser UI verification is marked as **UNVERIFIED** (no browser automation available).

### Step 1 — Phone viewport at 390 px

Open http://localhost:8080 in a browser with DevTools viewport set to 390 × 844.  
**Check:** Page renders inside `max-width: 480px` shell, no horizontal scroll, sticky header visible.  
**Result:** UNVERIFIED (requires browser)

---

### Step 2 — Select M02, Cell Structure and Function

> Note: M01 is "The Scientific Method". M02 is **"Cell Structure and Function"**.

Tap the **M02 — Cell Structure and Function** card (Week 02 · 📄 Reading).  
The card border turns lavender when selected. The "Start studying" button activates.  
Tap "Start studying".  
**Check:** Title strip shows `M02 · Cell Structure and Function`. Material is marked Instructor-assigned (confirmed by `assigned_by_instructor: true` in data). M06 and M10 do not appear in the picker.  
**Result (data):** PASSED — `python3 case2/case2_data_test.py` → 104 passed · 0 failed

---

### Step 3 — Reading level toggle

The Quick review tab opens with Course wording bullets.  
Tap **"Plain English"** in the pill toggle.  
**Check:** Bullets change to shorter, plain-language sentences from `PLAIN_ENGLISH_BULLETS.M02`. Course terms (Prokaryotic cell, Mitochondria, Phospholipid bilayer, etc.) remain visible and bolded. "Sample content" notice reads "Plain English view — local fallback, not AI-generated".  
**Result:** UNVERIFIED (requires browser) — logic verified by source inspection: `renderReview` selects `PLAIN_ENGLISH_BULLETS[material.id]` when `state.readingLevel === 'plain'`

---

### Step 4 — Key terms in Español

Tap the **Key terms** tab.  
Tap **"Español"** in the Glossary language toggle.  
**Check:** Term cards switch to `definition_es` values from `KEY_TERMS_ES.M02`. Sample translation notice appears. Verify the **Mitochondria** entry reads: *"Orgánulo que produce ATP mediante la respiración celular; a menudo llamado la 'central eléctrica de la célula'."*

> Note: "Independent variable" is a term for M01 (The Scientific Method), not M02. Use M02's terms (Mitochondria, Prokaryotic cell, etc.) for this verification step.

**Result:** UNVERIFIED (requires browser) — logic verified by source inspection: `renderTerms` uses `KEY_TERMS_ES[material.id]` when `state.glossaryLang === 'es'`

---

### Step 5 — Practice question, feedback, View source

Tap the **Practice** tab. A sample question appears labeled "Sample practice question".  
For M02, one of two questions will appear randomly:
- "Which organelle is primarily responsible for producing ATP?" (answer: C — Mitochondria)
- "What structural feature do plant cells have that animal cells lack?" (answer: D — Cell wall)

Select an answer. Tap **"Submit answer"**.  
**Check:** Correct answer highlighted with ✓ icon and green border. Wrong answer (if chosen) highlighted with ✗ icon and red border. Both use symbol + color (passes color-blind check). Explanation text appears.

Tap **"View source ▸"** (the `<details>` disclosure).  
**Check:** Shows `✓ Instructor-assigned` pill, `M02` pill, `Week 02` pill, title "Cell Structure and Function", and the supporting excerpt in quotes. Excerpt is verified as a verbatim substring of `source_text` by `excerptVerified()`.  
**Result:** UNVERIFIED (requires browser) — `excerptVerified()` logic verified by source inspection; both M02 excerpts confirmed as substrings of M02 `source_text`

---

### Step 6 — Get help for the 11 p.m. persona

Tap **"Get help"** in the header.  
**Check:** Page scrolls to the help section. Four cards visible:

| Card | Visible to 11pm student | Expected content |
|------|------------------------|-----------------|
| Online Tutoring (24/7) | ✓ — featured card, 24/7 badge | Directions: "Log in to MyIvy → Student Services → Tutoring → Start a Session." No dead link. |
| Biology Tutoring Center | Scheduled only | Hours shown: Mon/Wed 10am–2pm · Tue/Thu 1pm–5pm · Sat 10am–1pm |
| Prof. M. Torres | Office hours only | Tue/Thu 2–4pm; email link |
| Ivy Tech Help Desk | ✓ — 24/7 | Phone: 1-888-IVY-LINE |

All sample-data cards show amber "Sample data" badge. No `href="#"` dead links.  
**Result:** UNVERIFIED (requires browser) — card content verified by source inspection against `HELP_OPTIONS` entries

---

### Step 7 — Switch to M03, confirm state clears

> Note: M03 is **"Lecture Notes: Cell Division — Mitosis & Meiosis"** (not "Water and Life").

Scroll back to the picker. Tap **M03 — Lecture Notes: Cell Division — Mitosis & Meiosis** (Week 03 · 📝 Lecture Notes).  
Tap "Start studying".  
**Check:**
- Title strip updates to `M03` and new title
- Quick review bullets are from M03 `source_text` (or `PLAIN_ENGLISH_BULLETS.M03` if Plain English is still active)
- Key terms show M03 terms (Mitosis, Meiosis, Prophase, Metaphase, Crossing over, Cytokinesis)
- Practice tab shows a fresh M03 question (Metaphase or Crossing over question)
- Old M02 quiz answer is gone — `resetQuizState()` is called at top of `onStudyClick()` before any re-render

**Result:** UNVERIFIED (requires browser) — `resetQuizState()` confirmed in source; M03 data verified by test suite

---

## Additional checks

| Check | Method | Result |
|-------|--------|--------|
| Data tests (104 assertions) | `python3 case2/case2_data_test.py` | **PASSED** — 104 passed · 0 failed |
| HTTP server starts | `curl http://localhost:8080/index.html` | **PASSED** — HTTP 200 |
| ES module import syntax | Source inspection | **PASSED** — `import { ... } from './case_data.js'` is valid ES module syntax |
| M06/M10 excluded from picker | Data test group 2 | **PASSED** — both confirmed absent from assigned list |
| M06/M10 have QUESTION_BANK entries but unreachable | Data test group 4 | **PASSED** |
| `source-disclosure` double-wrap bug | Source inspection | **FIXED** — removed outer `<div class="source-disclosure">` wrapper |
| View source CSS (`details[open] summary::before`) | Source inspection | **PASSED** — CSS targets `.source-disclosure[open]` on the `<details>` element directly after fix |
| `source-label` CSS defined | Grep | **PASSED** — defined at line 308 |
| `sampleNoticeHTML` hoisting | Source inspection | **PASSED** — `function` declaration, hoisted in module scope |
| Keyboard navigation — tabs | Source inspection | **PASSED** — ArrowLeft/ArrowRight in `[role="tablist"]` keydown handler |
| Keyboard navigation — radio cards | Source inspection | **PASSED** — native `input[type="radio"]` elements, keyboard-reachable |
| Keyboard navigation — focus ring | Source inspection | **PASSED** — `:focus-visible` rule with 3px blue outline on all interactive elements |
| Horizontal overflow at 360 px | Source inspection | **PASSED** — `max-width: 480px`, `word-break` implicit on flex containers; `@media (max-width: 360px)` tightens tab and toggle font sizes |
| Zero-network sample mode | Source inspection | **PASSED** — `callAI` throws synchronously; all catches use local data |
| Browser console errors | Source inspection | **PASSED** — no undefined variables, no missing imports, no unreachable code after fix |
| Demo path title discrepancy (M02) | Source inspection | **FIXED in README** — M02 is "Cell Structure and Function", not "The Scientific Method" |
| Demo path title discrepancy (M03) | Source inspection | **FIXED in README** — M03 is "Cell Division — Mitosis & Meiosis", not "Water and Life" |
| Demo path "independent variable" question | Source inspection | **FIXED in README** — this is an M01 term/question; M02 demo uses Mitochondria/Cell wall questions |

---

## Remaining demo blockers

| Item | Status | Notes |
|------|--------|-------|
| Browser UI verification | Unverified | No browser automation in this environment. All checks done via source inspection + HTTP ping. |
| `KEY_TERMS_ES` professional verification | Unverified | Spanish definitions are sample machine-translated text, labeled as such. Do not demo as production-ready translations. |
| `PLAIN_ENGLISH_BULLETS` accessibility audit | Unverified | Flesch-Kincaid grade level not formally measured. Text written to approx. grade 7–8. |
| Real AI backend | Not connected | `callAI()` stub always throws. Wire to `/api/generate` endpoint when available. |

---

## IBM Bob contribution

Bob (Agent mode) created:

1. **`case_data.js`** — complete BIOL 101 data layer: 10 materials, 10-entry question bank, KEY_TERMS (5–6 per material), KEY_TERMS_ES (Spanish, M01–M05), PLAIN_ENGLISH_BULLETS (M01–M05), HELP_OPTIONS (4 contacts with structured fields), and the backwards-compatible HELP_DIRECTORY alias.

2. **`index.html`** — full mobile-first prototype in three major iterations:
   - Iteration 1: core select → summary → practice → reveal flow with sample mode fallback
   - Iteration 2: Study Shift branding, warm palette, radio-card picker, 3-tab study views, lavender selected states, quiz reset on material change
   - Iteration 3: reading-level toggle, Español glossary toggle, View Source provenance disclosure, structured help panel

3. **`case2_data_test.py`** — 104 Python assertions covering assigned-material filtering, M06/M10 exclusion, required fields, question bank completeness. Runs without Node or a browser.

4. **`case2.test.js`** — Node.js mirror of the same tests.

5. This **README** — including accurate demo path and pass/fail/unverified check table.

**What the team changed:**  
- Test regex for `QUESTION_BANK` block extraction fixed in one iteration (initial `\};\n` pattern didn't match)  
- Demo path title discrepancies corrected in README (Bob's draft used wrong material titles; fixed here)  
- Double-wrapping of `source-disclosure` `<details>` element fixed in `revealAnswer` (outer `<div>` removed)

---

## Run data tests

```bash
# From project root:
python3 case2/case2_data_test.py
# Expected: 104 passed · 0 failed

# Node.js (if available):
node --experimental-vm-modules case2/case2.test.js
```
