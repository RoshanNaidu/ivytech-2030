# AGENTS.md: project context for IBM Bob

IBM Bob loads this file automatically into every conversation. Keep it short and current.

## What this project is
Ivy Tech Community College **IT Challenge 2026: "The Future of Ivy Tech: Build the 2030 Experience with IBM Bob."**
We are an Innovation Squad building a working prototype for **one pillar** of Ivy Tech's Strategic Plan 2030
("The Future of College") and **one person** it serves. Problem framing lives in `app/lib/config.py`.

Judges score: technical execution, innovation, challenge fit, feasibility, real-world impact, documentation,
every member's contribution, professionalism. They read our **commit history**.

## Stack
- Python 3.12, managed by `uv`. Run: `uv run streamlit run app/Home.py`. Test: `uv run pytest -q`. Lint: `uv run ruff check app tests`.
- Streamlit multipage app: `app/Home.py` + `app/pages/N_Name.py`. Shared code in `app/lib/`:
  - `config.py`: persona, problem, pillar, outcome metric (single source of truth)
  - `data.py`: load/clean/profile any CSV/XLSX in `data/`; `describe_for_llm()` for prompts
  - `ml.py`: `train(df, target)` explainable baseline model with permutation importance
  - `charts.py`: Plotly helpers with consistent styling (`auto_chart`, `importance_bar`, `gauge`, `trajectory`)
  - `ai.py`: `ask(prompt, system, history)` with backends claude | granite (Ollama) | offline; never crashes
  - `ui.py`: `page(title)` sidebar + dataset picker; `get_df()` returns the active dataframe
- Data provided on challenge day goes in `data/` (git-ignored except `data/README.md`).

## How to work in this repo
- Smallest change that works end-to-end; keep the app runnable after every commit.
- New screen = new file in `app/pages/`, using `page()` and `get_df()`. Put reusable logic in `app/lib/`.
- Never hard-code secrets; read from `.env` (see `.env.example`).
- Plain-language UI copy for students and college leaders; no jargon on screen.
- After meaningful work, append a row to `docs/BOB_LOG.md` (see `.bob/rules/`).
