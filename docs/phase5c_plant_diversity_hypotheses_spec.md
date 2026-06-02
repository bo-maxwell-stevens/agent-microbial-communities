# Phase 5C plant diversity hypotheses specification

## Scientific objective
Evaluate whether DarkDivNet biodiversity metrics explain additional variation in cross-domain microbial coupling beyond the Phase 5B abiotic baseline.

## Conceptual constraint
This is **hypothesis testing**, not generic feature selection.

Do not place `alpha`, `dark`, `pool`, and `compl` together in a single primary model due to structural dependence (`alpha ≈ pool - dark`).

## Predictor policy
### Abiotic base (fixed)
- `pH_KCl`
- `N_pct`
- `bio12now.100`

### Primary hypothesis models
- **A**: abiotic base
- **B**: abiotic base + `alpha`
- **C**: abiotic base + `dark`
- **D**: abiotic base + `pool`
- **E**: abiotic base + `compl`
- **F**: abiotic base + `alpha` + `dark`
- **G**: abiotic base + `pool` + `compl`

### Geography sensitivity-only
- add `latitude`, `longitude` to each model as a sensitivity scope

### Explicit exclusions
- `PC1`, `PC2`, `PC3`, `PC4`
- `beta`, `beta.perc`, `compl.perc`, `gamma`

## Response and stratification
- Microbial pairs: `BAC↔ITS`, `AMF↔ITS`, `EUK↔ITS`, `AMF↔EUK`
- Branches: `presence/absence`, `CLR`
- Coupling response identical to Phase 5B methodology

## Reported statistics per model
- R²
- adjusted R²
- Δ adjusted R² vs abiotic base
- permutation p-value

## Required outputs
`results/phase5c_plant_diversity/`:
- `phase5c_model_comparison.csv`
- `phase5c_predictor_effects.csv`
- `phase5c_pair_rankings.csv`
- `phase5c_hypothesis_summary.csv`
- `phase5c_model_delta_adj_r2.png`
- `phase5c_hypothesis_rankings.png`
- `phase5c_pair_comparisons.png`
