#!/usr/bin/env bash
# Run the SmartHaus test suite. Any extra args are passed through to pytest,
# e.g.  ./run_tests.sh -k health -v
set -euo pipefail

cd "$(dirname "$0")"

# Prefer the project venv if present, otherwise fall back to the active python.
if [[ -x "venv/bin/python" ]]; then
    PY="venv/bin/python"
else
    PY="python3"
fi

exec "$PY" -m pytest "$@"
