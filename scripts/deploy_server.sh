#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_SERVICE="${BACKEND_SERVICE:-}"
FRONTEND_SERVICE="${FRONTEND_SERVICE:-}"
PIP_INSTALL_COMMAND="${PIP_INSTALL_COMMAND:-install -r requirements.txt}"
NPM_INSTALL_COMMAND="${NPM_INSTALL_COMMAND:-ci}"
NPM_BUILD_COMMAND="${NPM_BUILD_COMMAND:-build}"

cd "$ROOT_DIR"
git pull --ff-only

cd "$BACKEND_DIR"
if [ ! -x ".venv/bin/python" ]; then
  echo "Python virtual environment not found: backend/.venv" >&2
  exit 1
fi

# Always run Alembic during deploy. If there is no new migration, this is a no-op.
".venv/bin/python" -m pip $PIP_INSTALL_COMMAND
".venv/bin/python" -m alembic upgrade head

cd "$FRONTEND_DIR"
npm $NPM_INSTALL_COMMAND
npm run "$NPM_BUILD_COMMAND"

if [ -n "$BACKEND_SERVICE" ]; then
  sudo systemctl restart "$BACKEND_SERVICE"
fi

if [ -n "$FRONTEND_SERVICE" ]; then
  sudo systemctl restart "$FRONTEND_SERVICE"
fi

echo "CampusTree deploy complete."
