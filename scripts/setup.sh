#!/usr/bin/env bash
# One-command setup for teammates: installs uv (if missing), Python 3.12 and all dependencies.
set -euo pipefail
cd "$(dirname "$0")/.."
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv (Astral's Python manager)…"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
uv sync
[ -f .env ] || cp .env.example .env
uv run pytest -q
echo
echo "Ready. Start the app with:  uv run streamlit run app/Home.py"
