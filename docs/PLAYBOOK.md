# Challenge-day playbook

> The brief: *"prepare your skills, not a solution."* This repo is our **toolkit**. The idea, analysis
> and prototype are created on the day with IBM Bob, and the commit history will show it.

## Roles (everyone commits from their own GitHub account; contribution is scored)
| Role | Owns | Primary Bob mode |
|------|------|------------------|
| **Lead / PM** | problem framing, `config.py`, user stories, timeboxes, final README | Plan → 🏆 Impact Writer |
| **Data** | dataset profiling, baseline numbers, model, evidence charts | 📊 Data Analyst |
| **App** | screens in `app/pages/`, the end-to-end user flow, demo stability | Agent |
| **Story** | Bob log hygiene, pilot interviews, Impact Statement, demo script | 🔁 Pilot Feedback → 🏆 Impact Writer |
With 3 people, Lead also takes Story. With 5, split App into front-end flow and AI feature.

## Before the event (do now)
- [ ] Everyone: Bob trial active, Bob installed, **logged in**, Bobcoins saved. GitHub account ready.
- [ ] Everyone: accepted repo invite, `git clone`, `./scripts/setup.sh`, app runs at http://localhost:8501.
- [ ] Everyone: open the repo folder in Bob and check Settings → Modes shows the 3 custom modes.
- [ ] Skim `docs/PILLARS.md` and pick a favourite idea per pillar, so Phase 1 is a choice, not a blank page.
- [ ] Charge laptops; bring chargers; phone hotspot as backup Wi-Fi.

## Phase 1: Define and plan with Bob
**Done means:** persona + problem + measurable 2030 outcome agreed, MVP stories written, plan committed.
1. Read the brief and data dictionary together. Drop data into `data/` (git-ignored).
2. 📊 Data Analyst: profile the data (prompt P1-1). Find the 1-2 facts that make the problem real.
3. Choose: **pillar → one person → one problem → one metric**. Use the selection test below.
4. Plan mode: generate user stories + MVP plan (prompt P1-3). Edit, don't accept blindly.
5. Fill `app/lib/config.py`, `docs/USER_STORIES.md`, first `docs/BOB_LOG.md` rows. **Commit + push.**

**Selection test (score 1-3 each, pick the highest):** visible in the data? · demoable end-to-end in phase 2?
· a metric leaders already track (retention, completion, wages, transfer)? · one clear person? · AI adds real value?

## Phase 2: Smallest working prototype
**Done means:** a persona can complete the core task end-to-end on real data, live, without errors.
- Build ONE flow first; reuse the Explore / Predict / Assistant / Impact pages; delete or hide what doesn't fit.
- Commit every 20-30 minutes, each member on their own files to avoid conflicts (`git pull --rebase` often).
- Freeze 15 minutes before the end of the phase: run it fresh, fix only blockers.

## Phase 3: Improve with pilot feedback (don't restart)
**Done means:** feedback captured, 2-3 targeted changes shipped, before → after documented.
- Run the 4 questions in `docs/PILOT_FEEDBACK.md` with each pilot user; watch silently.
- 🔁 Pilot Feedback mode: cluster and rank (prompt P3-1). Ship the top 2-3 small changes.
- Record the before → after in `docs/PILOT_FEEDBACK.md` and link the commits.

## Phase 4: Document and prove impact
**Done means:** README complete, Impact Statement one page, Bob log complete, demo rehearsed twice.
- 🏆 Impact Writer drafts README + Impact Statement from our real numbers (prompts P4-1, P4-2); humans edit.
- Rehearse `docs/DEMO_SCRIPT.md`; every member speaks. Final commit + push; confirm the repo is **public**.

## How the judges score, and where we earn it
| Criterion | Where we earn it |
|-----------|------------------|
| Technical execution | Runs live without errors; tests + CI green; clean commits |
| Innovation | AI that does something a spreadsheet can't (risk ranking, plain-English Q&A, personalised next step) |
| Challenge fit | Explicit pillar + persona + 2030 metric on screen and in the README |
| Feasibility | Uses data Ivy Tech already has; rollout plan across 19 campuses; honest risks |
| Real-world impact | Baseline → target → number of students, from real data |
| Documentation | README, Impact Statement, Bob log, pilot feedback, all complete |
| Contribution | Commits from every member; every member speaks in the demo |
| Professionalism | Plain language, consistent design, on time |
