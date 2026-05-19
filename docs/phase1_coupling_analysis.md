# Phase 1 Coupling Analysis

## Methods
- Cohort: full-overlap across metadata + AMF/BAC/EUK/ITS sample IDs.
- Preprocessing per kingdom: prevalence filtering -> relative abundance -> pseudocount CLR -> PCA reduced space.
- Coupling metrics: Procrustes correlation, Mantel-like Spearman over reduced-space distance vectors, and RV coefficient; all with permutation p-values.
- Associations: Spearman + permutation p-values between microbial summaries (kingdom PC1 and cross-kingdom dispersion) and plant metrics (`alpha`, `gamma`, `dark`, `compl`, `pool`, `compl.perc`, `beta`, `beta.perc`).
- Covariate-aware partial analysis: residualization using available numeric environmental covariates (`pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`, `hfp.300`, `bio1now.100`, `bio12now.100`).
- Blocking strategy: attempts `site.id` then `region`; falls back to unblocked permutations when repeated groups are unavailable.

## Operational robustness additions
- Checkpoint logging to `results/phase1_coupling/checkpoints.log`.
- Intermediate pre-expensive-step snapshot in `results/phase1_coupling/intermediate_summary.json`.
- Deduplicated/timestamped warning emission in `results/phase1_coupling/warnings.log`.
- Lightweight exponential retry/backoff for transient failures in long-running steps.
- Runtime metadata (`runtime_seconds`, environment, input hashes/sizes) in `run_metadata.json`.

## Sample cohort
- META: 99
- AMF: 120
- BAC: 140
- EUK: 135
- ITS: 139
- **Full overlap used for analysis: 84**

## Preprocessing
- Primary prevalence threshold: 0.05
- Sensitivity thresholds: 0.05, 0.10
- PCA components per kingdom: 5
- Permutations per primary test: 99

See:
- `results/phase1_coupling/filtering_summary.csv`
- `results/phase1_coupling/pca_variance_explained.csv`
- `results/phase1_coupling/prevalence_sensitivity.csv`

## Statistical assumptions
- Reduced-space analyses are used to control p>>n instability.
- Permutation tests provide conservative calibration; if blocking is unavailable, residual confounding risk remains.
- Metrics quantify global structure/coupling and are not taxon-level interaction claims.

## Results summary
- Strongest reduced-space kingdom coupling (Procrustes): **EUK–ITS**, corr=0.586, perm-p=0.010.
- Coupling sensitivity summary:
  - Threshold 0.05: mean Procrustes 0.423, mean Mantel 0.345, mean RV 0.538
  - Threshold 0.10: mean Procrustes 0.441, mean Mantel 0.376, mean RV 0.551
- Top exploratory microbial–plant signal (unadjusted): `AMF_PC1` vs `alpha` with Spearman r=-0.320 and perm-p=0.010.
- Covariate-adjusted (partial) associations were weaker in most top unadjusted pairs.

Detailed outputs:
- `results/phase1_coupling/kingdom_coupling_metrics.csv`
- `results/phase1_coupling/plant_associations.csv`

## Interpretation cautions
- This is a phase-1 defensibility pass, not final inference.
- Blocking was not possible with current overlap structure (`warnings.log` records fallback).
- Signals should be prioritized by threshold stability and covariate robustness, not single p-values.

## Next-step recommendations
1. Carry forward only associations stable across prevalence thresholds.
2. Keep reduced-space architecture for phase 2 and continue to avoid taxon-level co-occurrence networks.
3. Use strict validation/sensitivity workflows before manuscript-level claims.
