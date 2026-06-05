# Prevalence Filtering Checkpoint

## Threshold decision
- Canonical threshold: **prevalence ≥ 0.05**.
- Sensitivity thresholds retained: **none** and **prevalence ≥ 0.10**.

## Taxa retained by domain (none / 0.05 / 0.10)
- BAC: none=291699, 0.05=16561, 0.10=7786
- ITS: none=26285, 0.05=1286, 0.10=518
- EUK: none=58205, 0.05=4126, 0.10=1651
- AMF: none=386, 0.05=148, 0.10=106

## Robustness summary
- Major conclusions were stable across thresholds.
- pH_KCl remained top environmental predictor (Phase 5B).
- abiotic_plus_alpha remained top plant-diversity model (Phase 5C).
- AMF↔ITS remained most plant-responsive.
- No Phase 5B/5C significance calls were gained or lost.

## Reason for canonical 0.05
- prevalence ≥ 0.05 reduces extreme rare-taxon noise while retaining more community information than prevalence ≥ 0.10.

## Canonical output status (no overwrite)
- Canonical outputs do **not** currently correspond to prevalence ≥ 0.05 (SHA-256 mismatch).
  - `results/phase4_coupling_inference/phase4_mantel_inference.csv` vs `results/filter_sensitivity/prevalence_005/phase4_coupling_inference/phase4_mantel_inference.csv`
  - `results/phase5_bac_integration/phase5_bac_mantel_inference.csv` vs `results/filter_sensitivity/prevalence_005/phase5_bac_integration/phase5_bac_mantel_inference.csv`
  - `results/phase5_bac_integration/phase5_bac_rank_summary.csv` vs `results/filter_sensitivity/prevalence_005/phase5_bac_integration/phase5_bac_rank_summary.csv`
  - `results/phase5b_environmental_drivers/phase5b_pair_rankings.csv` vs `results/filter_sensitivity/prevalence_005/phase5b_environmental_drivers/phase5b_pair_rankings.csv`
  - `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv` vs `results/filter_sensitivity/prevalence_005/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`
  - `results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv` vs `results/filter_sensitivity/prevalence_005/phase5c_plant_diversity/phase5c_hypothesis_summary.csv`
  - `results/phase5c_plant_diversity/phase5c_pair_rankings.csv` vs `results/filter_sensitivity/prevalence_005/phase5c_plant_diversity/phase5c_pair_rankings.csv`
  - `results/phase5d_synthesis/final_coupling_rankings.csv` vs `results/filter_sensitivity/prevalence_005/phase5d_synthesis/final_coupling_rankings.csv`
  - `results/phase5d_synthesis/final_pair_synthesis.csv` vs `results/filter_sensitivity/prevalence_005/phase5d_synthesis/final_pair_synthesis.csv`
- Per instruction, canonical outputs were not overwritten.

## Transparency
- All threshold outputs are preserved under `results/filter_sensitivity/prevalence_none`, `prevalence_005`, and `prevalence_010`.
