#!/usr/bin/env bash
# Invite teammates with push access. Usage: scripts/add_collaborators.sh user1 user2 …
set -euo pipefail
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
for u in "$@"; do
  gh api -X PUT "repos/$REPO/collaborators/$u" -f permission=push >/dev/null && echo "Invited $u to $REPO"
done
echo "They must accept the invite: https://github.com/$REPO/invitations"
