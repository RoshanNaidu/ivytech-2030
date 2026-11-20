# Team workflow

Speed beats ceremony, but judges read the commit history, so keep it clean and make sure everyone shows up in it.

## First time
```bash
git clone https://github.com/<owner>/ivytech-2030.git && cd ivytech-2030
./scripts/setup.sh
uv run streamlit run app/Home.py
```
Use **your own** GitHub account so your commits count as your contribution
(`git config user.name` / `user.email` must match your GitHub account).

## The loop (work directly on `main`, in small steps)
```bash
git pull --rebase                 # before you start, and before every push
# … work with IBM Bob …
uv run pytest -q && uv run ruff check app tests
git add -A && git commit -m "P2: add at-risk ranking to Predict page"
git pull --rebase && git push
```
- **Own your files.** Agree who edits which page or doc each phase, so you rarely conflict.
- `app/lib/config.py` and `README.md` have one owner (Lead) to avoid merge pain.
- Commit message: `P<phase>: <what changed>`. Commit every 20-30 minutes.
- Merge conflict? `git status`, fix the marked lines, `git add`, `git rebase --continue`. Ask for help early.
- Log your Bob sessions: `./scripts/log_bob.sh` (or let Bob append to `docs/BOB_LOG.md`).
