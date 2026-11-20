# IBM Bob working log

A running record of how our team worked with **IBM Bob**, our core development tool. Each row shows what we
asked, what Bob produced, and how we judged and changed it.

Add a row with `scripts/log_bob.sh` or let Bob append it (rule in `.bob/rules/02-bob-log-and-commits.md`).

**How we ran Bob:** most sessions ran through **IBM Bob Shell** (`bob run`) on Roshan's laptop, using the
team's custom modes. Prompts were drafted with help from an AI coordinator (Claude Code), which also reviewed
and tested Bob's output. **All application code was written by IBM Bob**; the review notes in the last column
record what we checked or changed.

**Bob setup used:** `AGENTS.md` (auto-loaded project context), `.bob/rules/` (engineering and logging rules),
`.bob/custom_modes.yaml` (📊 Data Analyst, 🏆 Impact Writer, 🔁 Pilot Feedback), plus Bob's built-in
Plan / Agent / Ask modes.

| Time | Phase | Member | Bob mode | What we asked | What Bob produced | What we kept / changed and why |
|------|-------|--------|----------|---------------|-------------------|--------------------------------|
| 15:11 | 1 | Roshan | Plan | Asked Bob to read CASE.md and produce PERSONA.md, USER_STORIES.md, and BUILD_PLAN.md for Case 2 — Alternative-Format Study Tool | Created docs/PERSONA.md (fictional persona Lena Trujillo, framing, metrics), replaced docs/USER_STORIES.md (5 stories with Given/When/Then, MVP vs Next), created docs/BUILD_PLAN.md (mobile-first design decisions, study.py contract, Home.py wireframe, 4-member team split, 6-test test plan, Part 2 checklist) | Kept all three files as produced; no changes needed — content matched case requirements and was sufficiently specific for agent-mode implementation |
