# Release readiness report (v2.4 direct-Aitchison baseline)

Generated (UTC): 2026-06-04T15:24:00+00:00

## Required readiness answers

- Is the manuscript numerically consistent? **Yes.**
  - `results/manuscript_verification/manuscript_final_consistency_report.md` reports `mismatches = 0` and `needs_human_review = 0`.
  - Reconciled numeric statements in `manuscript/manuscript_v24.md` match canonical synthesis ranges/values.

- Is the repository internally consistent? **Yes.**
  - `docs/repository_state_report.md` confirms direct-Aitchison evidence, canonical 999 permutation fields, p-value floor consistency, pair-scope consistency, and preserved backups.

- Are the canonical outputs reproducible? **Yes (operationally reproducible baseline).**
  - Canonical outputs are complete and internally coherent under the current committed analysis pipeline.
  - Validation gates passed (py_compile for in-scope scripts, targeted pytest, full pytest, `git diff --check`).

- Are there any remaining blockers to coauthor review? **No blocking technical inconsistencies remain.**
  - Remaining work is editorial/coauthor interpretation, not repository or numeric-consistency remediation.

## Validation results

- `py_compile` (in-scope Phase 4/5 analysis + verification tests): **PASS**
- Targeted verification tests:
  - `.venv/bin/pytest -q tests/test_analysis_verification_data_integrity.py tests/test_analysis_verification_regression.py`
  - Result: **16 passed**
- Full test suite:
  - `.venv/bin/pytest -q`
  - Result: **21 passed**
- `git diff --check`: **PASS**

## Release decision

- Direct-Aitchison canonical baseline is ready for release tagging as `v2.4-direct-aitchison`.
- Safe to proceed to coauthor review before any new sensitivity-analysis branches.
