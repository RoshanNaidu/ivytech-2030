# IBM Bob prompt library

Paste, then fill in the `<…>`. Bob already knows the repo from `AGENTS.md`. Log what happened in `docs/BOB_LOG.md`.

## Phase 1: Define and plan
**P1-1 · 📊 Data Analyst · profile the data**
> Profile every file in `data/`. For each: rows, columns, types, missing %, likely keys, and how files join.
> Then list 5 patterns relevant to Ivy Tech student outcomes (retention, completion, wages, transfer), each
> with the number behind it and the sample size. Write the code as a reusable function in `app/lib/data.py`.

**P1-2 · Ask · pressure-test the problem**
> We're considering: persona = <…>, problem = <…>, pillar = <…>, 2030 metric = <…>. Act as an Ivy Tech
> vice-chancellor. What's weak about this framing? What would make it measurable from our data? Suggest 2 sharper versions.

**P1-3 · Plan · stories and MVP plan**
> Write 5 user stories (As a / I want / so that + Given-When-Then acceptance criteria) for <persona> solving
> <problem>. Mark the 2 that form the smallest end-to-end MVP. Then give a build plan of 30-minute tasks for
> 4 people that reuses `app/lib/` and avoids two people editing the same file. Save stories to `docs/USER_STORIES.md`.

## Phase 2: Build
**P2-1 · Agent · core screen**
> Create `app/pages/<N>_<Name>.py` so <persona> can <core task>. Use `page()`, `get_df()`, and helpers in
> `app/lib/`. Keep it to one screen with a clear next action. Add a smoke test in `tests/`. Run tests and lint.

**P2-2 · Agent · AI feature**
> Using `lib.ai.ask`, add <AI capability> to <page>. Build the system prompt from `config.py` and
> `describe_for_llm(df)`. Never send row-level personal data. It must still work when `AI_PROVIDER=offline`.

**P2-3 · Ask · code review**
> Review the diff of the last commit for bugs, edge cases with missing or odd data, and anything that could
> crash during a live demo. List issues by severity with exact fixes.

## Phase 3: Improve
**P3-1 · 🔁 Pilot Feedback · prioritise**
> Here is our raw pilot feedback in `docs/PILOT_FEEDBACK.md`. Cluster it into themes, rank by user impact vs.
> effort, and propose the 3 smallest changes that fix the top themes without restructuring the app.

## Phase 4: Document and prove impact
**P4-1 · 🏆 Impact Writer · README**
> Complete README.md sections Problem, Solution, Technical approach, Pillar, Use of IBM Bob, using
> `config.py`, `docs/USER_STORIES.md`, `docs/BOB_LOG.md` and our real numbers. Concise, judge-friendly.

**P4-2 · 🏆 Impact Writer · Impact Statement**
> Fill `docs/IMPACT_STATEMENT.md` on one page: who benefits, metric baseline → 2030 target (show the maths
> from our data, e.g. +N pts × population × reach), what a 19-campus rollout needs, and the top risk + mitigation.

**P4-3 · Ask · judge rehearsal**
> Act as a judge scoring technical execution, innovation, challenge fit, feasibility and real-world impact.
> Ask our team the 5 hardest questions about this prototype, then tell us the weakest criterion and how to fix it in 15 minutes.
