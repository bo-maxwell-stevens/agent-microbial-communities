# Six-Pair Release Readiness

- Generated (UTC): 2026-06-05T12:23:26Z
- Recommendation: **ready to commit**

## Validation gates
- py_compile_exit: PASS (exit=0)
- targeted_pytest_exit: PASS (exit=0)
- full_pytest_exit: PASS (exit=0)
- git_diff_check_exit: PASS (exit=0)

## Canonical row counts
- phase4_mantel_inference.csv: 12
- phase4_summary.csv: 12
- phase5_bac_mantel_inference.csv: 12
- phase5b_dbRDA_summary.csv: 24
- phase5b_predictor_ranking.csv: 144
- phase5c_model_comparison.csv: 168
- phase5c_predictor_effects.csv: 864
- phase5c_pair_rankings.csv: 108

## Pair coverage by phase
- Phase 4: AMF↔EUK, AMF↔ITS, BAC↔AMF, BAC↔EUK, BAC↔ITS, EUK↔ITS
- Phase 5A: AMF↔EUK, AMF↔ITS, BAC↔AMF, BAC↔EUK, BAC↔ITS, EUK↔ITS
- Phase 5B: AMF↔EUK, AMF↔ITS, BAC↔AMF, BAC↔EUK, BAC↔ITS, EUK↔ITS
- Phase 5C: AMF↔EUK, AMF↔ITS, BAC↔AMF, BAC↔EUK, BAC↔ITS, EUK↔ITS
- Phase 5D: AMF↔EUK, AMF↔ITS, BAC↔AMF, BAC↔EUK, BAC↔ITS, EUK↔ITS
- Six-pair coverage complete across all phases: True

## Remaining blockers
- None
