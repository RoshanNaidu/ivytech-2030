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
