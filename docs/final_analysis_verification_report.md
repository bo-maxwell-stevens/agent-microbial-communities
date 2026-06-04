# Final Analysis Verification Report

- Generated: 2026-06-04T09:54:44.111854+00:00
- Repository: `/srv/hermes_projects/agent_microbial_communities`
- Branch: `main`
- HEAD at report generation: `1a662ab`
- Workflow: strict 999-permutation remediation + verification

## Phase permutation status

- Phase 4: 999-consistent **yes**
- Phase 5A: 999-consistent **yes**
- Phase 5B: 999-consistent **yes**
- Phase 5C: 999-consistent **yes**

## Phase 5A remediation details

- Cancelled stale laptop serial run (PID `49359`).
- Re-ran Phase 5A on Rocket via SLURM array at 999 permutations.
  - Job ID: `66369837`
  - Run ID: `phase5a_perm999_20260604T093653Z`
  - 24/24 array tasks completed (`ExitCode 0:0`).
- Combined checkpoints into final outputs and regenerated figures.
- Canonical Phase 5A outputs were backed up then replaced from validated 999 run.

## Backup preservation

- Pre-sync backups preserved under:
  - `results/archive_pre_999_sync/20260604T090054Z/` (prior Phase 5B/5C sync)
  - `results/archive_pre_999_sync/20260604T094703Z/phase5_bac_integration/` (Phase 5A pre-999 canonical backup)

## Validation suite

- `py_compile` (in-scope scripts + verification tests): **pass**
- `pytest -q tests/test_analysis_verification_data_integrity.py tests/test_analysis_verification_regression.py`: **pass** (`16 passed`)
- `pytest -q` (full suite): **pass** (`21 passed`)
- `git diff --check`: **pass**

## Manuscript-output consistency

- Canonical permutation fields expected to be 999 are now all 999 (see `perm999_completeness_check.json`).
- No stale 499 values remain in the canonical permutation fields for Phases 4/5A/5B/5C.
- P-value floors for 999-permutation outputs satisfy `>= 0.001` in checked canonical files.

## Numerical-claim audit status

- Numerical claims audited: 100
- Verified: 67
- Mismatches remaining: 0
- Not found: 23
- Needs human review: 10

## Manuscript readiness assessment

- Manuscript permutation language vs canonical outputs: **aligned to 999 for Phases 4/5A/5B/5C**.
- Unresolved risks:
  1. `23` claims remain `not_found` in numeric-claim audit.
  2. `10` claims remain `needs_human_review`.
- Recommendation: **ready for expert coauthor review on permutation consistency**, with the above unresolved claim-audit rows flagged for adjudication.


## 2026-06-04 strict 999 remediation re-verification (continuation)

- Generated (UTC): 2026-06-04T14:57:42.129026+00:00
- Phase 4 999-consistent: yes
- Phase 5A 999-consistent: yes
- Phase 5B 999-consistent: yes
- Phase 5C 999-consistent: yes
- Canonical stale 499 permutation fields: 0
- p-value floor checks pass: yes
- Numeric claims audited: 100
- Numeric claim status counts: {'verified': 67, 'not_found': 23, 'mismatch': 8, 'needs_human_review': 2}
- Mismatches remaining: 8
- P-value mismatches remaining: 1
- Pre-999 archive snapshots preserved: 5
- Validation suite: py_compile PASS; targeted pytest PASS (16); full pytest PASS (21); git diff --check PASS.
- Commit/tag decision: BLOCKED (mismatches remain; do not commit/tag until manuscript numeric mismatches are fully resolved).
