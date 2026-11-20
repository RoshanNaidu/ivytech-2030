# Ivy Tech 2030: <Product name>

> **IT Challenge 2026: Data Analytics, Applied AI & Informatics.** *The Future of Ivy Tech: Build the 2030
> Experience with IBM Bob.* An Innovation Squad prototype for one pillar of Ivy Tech's Strategic Plan 2030.

**Pillar:** <pillar> · **For:** <persona> · **2030 outcome:** <metric> from <baseline> to <target>

<!-- Screenshot or GIF of the core flow goes here: docs/img/demo.png -->

## Problem
<Who is struggling, with what, and the number from the data that proves it. 3-4 sentences.>

## Solution
<What the prototype does for the persona, end to end, in 3 bullets. What changed after pilot feedback.>

## Technical approach
- **App:** Python 3.12 + Streamlit multipage app (`app/`), Plotly charts, pandas.
- **Analytics / AI:** <model or AI feature: e.g. explainable risk model (scikit-learn, permutation importance);
  plain-English Q&A over a dataset summary via `lib/ai.py` (Claude, IBM Granite via Ollama, or offline fallback)>.
- **Data:** <dataset(s) provided on the day, cleaning, privacy safeguards>.
- **Quality:** smoke tests (`pytest`), lint (`ruff`), GitHub Actions CI on every push.

## Strategic Plan 2030 pillar
<Which pillar and exactly how this advances it. Link: https://www.ivytech.edu/strategicplan>

## How we used IBM Bob
IBM Bob was our core development tool for every phase. Full log: [`docs/BOB_LOG.md`](docs/BOB_LOG.md).
- **Project context for Bob:** [`AGENTS.md`](AGENTS.md) + rules in [`.bob/rules/`](.bob/rules/).
- **Custom modes we built** ([`.bob/custom_modes.yaml`](.bob/custom_modes.yaml)): 📊 Data Analyst, 🏆 Impact Writer, 🔁 Pilot Feedback.
- <3 highlights: where Bob saved the most time, where we corrected it, what we learned.>

## Impact
See the one-page [2030 Impact Statement](docs/IMPACT_STATEMENT.md) and [pilot feedback](docs/PILOT_FEEDBACK.md).

## Run it
```bash
./scripts/setup.sh                      # installs uv + Python 3.12 + dependencies
uv run streamlit run app/Home.py        # http://localhost:8501
uv run pytest -q                        # tests
```
Optional AI: copy `.env.example` to `.env` and set `AI_PROVIDER` (`claude` + key, `granite` with Ollama, or `offline`).

## Team
| Member | Role | Main contributions |
|--------|------|--------------------|
| <name> | Lead / PM |  |
| <name> | Data |  |
| <name> | App |  |
| <name> | Story |  |

## Repository map
```
app/Home.py, app/pages/   Streamlit screens
app/lib/                  config (problem framing), data, ml, charts, ai, ui helpers
data/                     challenge data (git-ignored)
docs/                     Impact Statement, Bob log, user stories, pilot feedback, demo script, playbook
.bob/, AGENTS.md          IBM Bob rules, custom modes and project context
```

## Preparation disclosure
Before the event we prepared only reusable tooling: this generic Streamlit starter (data loading, charts,
baseline model, AI wrapper), documentation templates and IBM Bob configuration. The problem, analysis and
prototype were defined and built during the challenge with IBM Bob; see the commit history and Bob log.
