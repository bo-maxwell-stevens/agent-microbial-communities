# Manuscript V18 Review Notes

## Verification completed before edits
I read the full current manuscript (`manuscript_v17.md`) before making edits and verified Methods/Results quantitative anchors against committed repository outputs.

Primary files checked:
- `results/phase5d_synthesis/final_coupling_rankings.csv`
- `results/phase5_bac_integration/phase5_bac_mantel_inference.csv`
- `results/phase5d_synthesis/final_environment_driver_summary.csv`
- `results/phase5d_synthesis/final_plant_diversity_summary.csv`
- `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`
- `results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv`
- `results/manuscript_preparation/methods_parameter_inventory.csv`
- `results/phase2_confirmatory_coupling/sample_cohort_used.csv`

Machine-readable verification snapshot:
- `/tmp/v18_verification.json`

## Key numerical anchors confirmed
- Cohort size: `n = 84`
- Highest coupling: BAC↔ITS presence/absence `0.5740768828` (reported as `0.574`)
- Mantel top BAC↔ITS: `ρ = 0.5842070605`, `p = 0.002` (reported as `0.584`, `0.002`)
- EUK↔ITS coupling values: `0.5378532210`, `0.5352122895` (reported as `0.538`, `0.535`)
- Coupling range: `0.3190034192–0.5740768828` (reported as `0.319–0.574`)
- BAC↔ITS prevalence stability: `ρ = 0.5972515497` at 0.05 and `0.5711625713` at 0.10
- BAC↔EUK at conservative threshold: `ρ = 0.1425007227`, `p = 0.018` (reported as `ρ = 0.143`, `p = 0.018`)
- Environmental adjusted R² integrated range: `0.1881364249–0.2776637106` (mean `0.2227137059`)
- Geography sensitivity delta: `0.0079546440–0.0218934528`
- pH contribution range: `0.0919503027–0.1509953841`
- Top plant-diversity deltas: `0.0189834474`, `0.0171597305`, `0.0165046833`

## Consistency audit (Abstract/Methods/Results)
Checked and confirmed consistency for:
- sample size (`n = 84`)
- pair counts and integrated-pair framing
- prevalence thresholds (`0.05`, `0.10`)
- permutation counts (`999`)
- environmental predictor framing (`pH_KCl`, `N_pct`, `bio12`, geography sensitivity)
- plant-diversity hypothesis set (A–G vs abiotic baseline)

Consistency issues discovered: **none**.

## Scope-control verification
- Modified sections: **Methods**, **Results**.
- Unchanged sections: **Abstract**, **Introduction**, **Discussion**, **Conclusions**, **Figure legends**, **References**.
- No scientific outputs modified.
- No analyses/HPC reruns.

## Requested counts
- Numerical precision changes: **1**
- Wording improvements: **5**

Word counts:
- Methods: **978 → 990**
- Results: **481 → 475**
- Total manuscript: **2689 → 2695**
