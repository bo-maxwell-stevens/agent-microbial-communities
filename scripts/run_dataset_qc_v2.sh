#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$REPO_ROOT/scripts/dataset_qc_v2.py" \
  --repo-root "$REPO_ROOT" \
  --data-dir data \
  --results-dir results/dataset_qc_v2 \
  --docs-dir docs
