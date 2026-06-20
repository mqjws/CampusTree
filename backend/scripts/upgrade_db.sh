#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$BACKEND_DIR"

if [ ! -x ".venv/bin/python" ]; then
  echo "Python virtual environment not found: backend/.venv" >&2
  exit 1
fi

".venv/bin/python" -m alembic upgrade head
