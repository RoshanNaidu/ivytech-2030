# Case 2 — Mobile Study Prototype

A mobile-first web prototype for **Ivy Tech BIOL 101** that walks a student
through: **select material → read summary → answer a practice question → reveal the answer**.

Designed for a student who studies on her phone after hours.

---

## Files

| File | Purpose |
|------|---------|
| `case_data.js` | All course data: `MATERIALS`, `QUESTION_BANK`, `HELP_DIRECTORY` |
| `index.html` | Single-file prototype (HTML + CSS + JS ES module) |
| `case2.test.js` | Node.js data integrity tests (run when Node is available) |
| `case2_data_test.py` | Python data integrity tests (run with `python3`) |

---

## Run the prototype

Open `case2/index.html` directly in any modern browser — no build step required.

```bash
# From the project root, any of these work:
open case2/index.html                      # macOS
xdg-open case2/index.html                  # Linux
start case2/index.html                     # Windows

# Or serve with Python for ES module support (recommended):
python3 -m http.server 8080 --directory case2
# then visit http://localhost:8080
```

> **Note:** Because `index.html` loads `case_data.js` as an ES module
> (`<script type="module">`), browsers block the import when opened as a
> `file://` URL. Use the Python server (or any static server) for local testing.

---

## Run the data tests

```bash
# From the project root:
python3 case2/case2_data_test.py
```

Expected output: **104 passed · 0 failed**

If Node ≥ 18 is available, the equivalent JS test can also be run:

```bash
node --experimental-vm-modules case2/case2.test.js
```

---

## What the tests verify

| # | Test group | Key checks |
|---|------------|-----------|
| 1 | M02 and M03 in assigned study | Both IDs appear in `assigned_by_instructor: true` list |
| 2 | M06 and M10 excluded from assigned | Neither appears in assigned list |
| 3 | M06 and M10 in full catalogue | Both IDs exist in MATERIALS |
| 4 | M06/M10 questions unreachable | QUESTION_BANK entries exist but assigned list never includes them |
| 5 | Required fields on all assigned materials | id, title, type, source_text, excerpt |
| 6 | Both material types in assigned study | "reading" and "lecture_notes" both present |
| 7 | Each assigned material has ≥1 question | QUESTION_BANK keyed by material ID |
| 8 | Question fields complete | question, options (4), answer (A–D), explanation, source_excerpt |
| 9 | Both types defined in source file | type "reading" and "lecture_notes" found in case_data.js |

---

## Architecture

The UI has five clearly separated components so each can be extended independently:

```
COMPONENT 1 — Selector        (initSelector)
COMPONENT 2 — Summary         (renderSummary / generateSummary)
COMPONENT 3 — Practice        (renderPractice / generatePractice)
COMPONENT 4 — Answer reveal   (revealAnswer)
COMPONENT 5 — Human help      (renderHelp)
```

**AI integration point:** replace the `callAI(prompt)` stub in `index.html`
with a real fetch to any compatible endpoint. When unavailable, the app
automatically falls back to sample mode and labels all generated content
with a gold "⚠ Sample Mode" banner and "Sample practice question" badges.

**Planned extensions (roadblock iteration):**
- Reading-level switch (swap summary component)
- Visible answer sources (toggle source excerpt in answer reveal)
- Smarter help routing (match material topic to tutor specialty)

---

## Design decisions

- **Narrow-first layout:** max-width 600 px, single column, `100dvh` for phone chrome.
- **Keyboard navigation:** `select`, radio buttons, and all buttons are native
  focusable elements; `:focus-visible` adds a 3 px blue outline.
- **Material ID provenance:** every summary and answer includes the material ID,
  title, and a source excerpt so the student can find the original text.
- **No student PII in prompts:** `callAI` sends only the material source text,
  never any student identifier.
