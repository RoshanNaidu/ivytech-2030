#!/usr/bin/env bash
# Append a row to docs/BOB_LOG.md.
# Usage: scripts/log_bob.sh <phase> <member> <mode> "<what we asked>" "<what Bob produced>" "<kept/changed + why>"
set -euo pipefail
cd "$(dirname "$0")/.."
if [ $# -ne 6 ]; then
  sed -n '3p' "$0"; exit 1
fi
clean() { printf '%s' "$1" | tr '\n' ' ' | sed 's/|/\\|/g'; }
printf '| %s | %s | %s | %s | %s | %s | %s |\n' "$(date +%H:%M)" "$(clean "$1")" "$(clean "$2")" \
  "$(clean "$3")" "$(clean "$4")" "$(clean "$5")" "$(clean "$6")" >> docs/BOB_LOG.md
echo "Logged. Commit it with your next change."
