# Engineering rules (all modes)

1. Keep the app runnable. Before finishing a code task, run `uv run pytest -q` and `uv run ruff check app tests`
   and fix anything you broke.
2. Reuse `app/lib/` helpers (`get_df`, `auto_chart`, `train`, `ask`, `describe_for_llm`) instead of re-implementing them.
3. Prefer editing existing files over creating parallel versions. No `*_v2.py`, no dead code.
4. Data arrives on challenge day: never invent numbers in the UI or docs. Compute them from `data/` or label them as assumptions.
5. Treat any student data as sensitive: no names or IDs in charts, logs, prompts sent to an AI backend, or screenshots.
6. Show uncertainty honestly (model metrics vs. baseline, sample sizes) so judges trust the numbers.
7. Every user-facing screen answers: who is this for, what should they do next.
