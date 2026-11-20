# IBM Bob working log

A running record of how our team worked with **IBM Bob**, our core development tool. Each row shows what we
asked, what Bob produced, and how we judged and changed it.

Add a row with `scripts/log_bob.sh` or let Bob append it (rule in `.bob/rules/02-bob-log-and-commits.md`).

**Bob setup used:** `AGENTS.md` (auto-loaded project context), `.bob/rules/` (engineering and logging rules),
`.bob/custom_modes.yaml` (📊 Data Analyst, 🏆 Impact Writer, 🔁 Pilot Feedback), plus Bob's built-in
Plan / Agent / Ask modes.

| Time | Phase | Member | Bob mode | What we asked | What Bob produced | What we kept / changed and why |
|------|-------|--------|----------|---------------|-------------------|--------------------------------|
| 15:04 | 2 | Madeline | Agent | Scaffold mobile-first Case 2 study prototype with case_data.js, select→summary→practice→reveal flow, sample mode fallback, human-help directory, M06/M10 exclusion, and 104-assertion Python test suite | Created `case2/case_data.js` (10 BIOL 101 materials, 10-entry question bank, help directory), `case2/index.html` (5-component mobile-first ES-module prototype), `case2/case2.test.js` (Node test), `case2/case2_data_test.py` (Python test), `case2/README.md` (run steps) | Kept all generated files; test regex for QUESTION_BANK block extraction was fixed in one iteration (initial `\};\n` pattern didn't match trailing newline, fixed to `\n\};`). All 104 tests pass. |
| 15:25 | 2 | Madeline | Agent | Implement core Study Shift UI: warm palette, 3-tab study views (Quick review / Key terms / Practice), radio-card material picker, quiz reset on material change, KEY_TERMS glossary, color-independent answer feedback | Rewrote `case2/index.html` (Study Shift branding, lavender selected state, evergreen primary, radio-card picker with week/type pills, 3 ARIA tab panels, term highlighting in bullets, `✓`/`✗` icons for color-blind feedback, quiz reset on material change). Added `KEY_TERMS` to `case2/case_data.js` (5–6 terms per material, all 10 IDs). 104 data tests still pass. | Kept all existing component function names; extended renderSummary→renderReview, added renderTerms. Sample-content notices added per-panel. M06/M10 exclusion verified. |
| 15:30 | 2 | Madeline | Agent | Roadblock iteration: (1) reading-level toggle + Español glossary, (2) View Source provenance disclosure, (3) structured help panel from HELP_OPTIONS | Added `KEY_TERMS_ES`, `PLAIN_ENGLISH_BULLETS`, `HELP_OPTIONS` to `case_data.js`. Rewrote `index.html`: pill-group level toggle (Course wording / Plain English) in Quick Review; lang toggle (English / Español) in Key Terms with sample-translation notice; `<details>` View Source in answer feedback with Instructor-assigned pill, week, title, verified excerpt; structured help cards with 24/7 badge, best_for text, portal directions instead of dead links. 104 data tests pass. | Kept all existing component function signatures. `excerptVerified()` checks every excerpt before showing it. Quiz reset preserved. M02/M03 tested in assigned list; M06/M10 confirmed absent. |
