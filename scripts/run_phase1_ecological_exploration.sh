#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

exec python3 "$REPO_ROOT/scripts/run_phase1_ecological_exploration.py" \
  --repo-root "$REPO_ROOT" \
  --data-dir data \
  --results-dir results/phase1_ecological_exploration
