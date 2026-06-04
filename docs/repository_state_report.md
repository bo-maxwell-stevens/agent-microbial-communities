# Repository state report

Generated (UTC): 2026-06-04T15:23:31.478055+00:00

## Canonical direct-Aitchison status
- Phase 4 CLR distance_metric values: ['euclidean']
- Phase 5A CLR distance_metric values: ['euclidean']
- Phase 5C clr_distance_strategy values: ['direct_aitchison']
- Phase 5B script default CLR strategy is direct_aitchison: True
- Canonical outputs direct-Aitchison consistent: True

## Canonical 999-permutation status
- Phase4 Mantel: `results/phase4_coupling_inference/phase4_mantel_inference.csv` `n_permutations` unique=[999]
- Phase5A Mantel: `results/phase5_bac_integration/phase5_bac_mantel_inference.csv` `n_permutations` unique=[999]
- Phase5B dbRDA: `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv` `permutations` unique=[999]
- Phase5B predictor: `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv` `permutations` unique=[999]
- Phase5C model: `results/phase5c_plant_diversity/phase5c_model_comparison.csv` `permutations` unique=[999]
- Phase5C predictor: `results/phase5c_plant_diversity/phase5c_predictor_effects.csv` `permutations` unique=[999]
- All canonical permutation fields expected to be 999 are 999: True

## p-value floor checks (999 permutations)
- Phase4: min p-value in `results/phase4_coupling_inference/phase4_mantel_inference.csv` = 0.001000
- Phase5A: min p-value in `results/phase5_bac_integration/phase5_bac_mantel_inference.csv` = 0.001000
- Phase5B: min p-value in `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv` = 0.001000
- Phase5C: min p-value in `results/phase5c_plant_diversity/phase5c_model_comparison.csv` = 0.001000
- p-value floor consistent with 999 permutations (>=0.001): True

## Pair-scope and manuscript reference checks
- Phase 5B pairs: ['AMF↔EUK', 'AMF↔ITS', 'BAC↔ITS', 'EUK↔ITS']
- Phase 5C pairs: ['AMF↔EUK', 'AMF↔ITS', 'BAC↔ITS', 'EUK↔ITS']
- Phase 5D pairs: ['AMF↔EUK', 'AMF↔ITS', 'BAC↔ITS', 'EUK↔ITS']
- Pair scope consistent across canonical outputs: True
- Manuscript references temporary/noncanonical outputs: none

## Backup preservation
- Pre-999 backup root exists: True
- Number of archived snapshots under results/archive_pre_999_sync/: 5
  - 20260603T171330Z
  - 20260604T090054Z
  - 20260604T094703Z
  - 20260604T132755Z
  - 20260604T133238Z

## Verdict
- Repository internally consistent canonical baseline: yes