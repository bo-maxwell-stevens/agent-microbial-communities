# Environmental Confounding Assessment (Phase 1 Robustness)

## Objective
Assess whether reduced-space coupling signals persist, weaken, or behave erratically after conservative adjustment for measured environmental covariates.

This is a sensitivity analysis only; no causal claims are made.

## Covariates considered
When present in metadata:
- `pH_KCl`
- `N_pct`
- `C_pct`
- `P_Mehlich3_mg_100g`
- `K_Mehlich3_mg_100g`
- `hfp.300`
- `bio1now.100`
- `bio12now.100`
- `region` (one-hot encoded)
- `PC1-4` (if present)

## Method
For each prevalence-threshold × PCA-dimension scenario and each kingdom pair:
1. Compute raw coupling metrics in embedding space.
2. Build covariate matrix (numeric + one-hot categorical).
3. Residualize embeddings against covariates via linear least squares.
4. Recompute coupling metrics on residualized embeddings.
5. Summarize attenuation/amplification:
   - `delta = adjusted - raw`
   - `attenuation_abs_ratio = |adjusted| / |raw|`

Source file: `results/phase1_robustness/environmental_adjustment_summary.csv`

## Key observations
1. **Adjustment did not uniformly attenuate effects.**
   In multiple pair/metric combinations, adjusted values increased substantially relative to raw values.

2. **Large post-adjustment magnitudes occurred frequently.**
   Several adjusted distance-correlation values approached very high magnitudes (near ~0.9), which is atypical and suggests sensitivity to specification / residualization geometry rather than clean confound removal.

3. **Direction flips and large deltas occurred.**
   Some association and coupling summaries changed sign after adjustment, indicating that effect direction is not consistently robust to covariate handling.

## Interpretation constraints
- These patterns are *not* evidence of strong environmentally corrected biological effects.
- They are more consistent with **high adjustment sensitivity** under modest sample size and high-dimensional embeddings.
- Therefore, adjusted outputs should be treated as a stress test result, not a primary inferential basis.

## Defensibility assessment
### What is defensible
- Reporting that coupling signals were tested under broad environmental adjustment and that conclusions are sensitive to adjustment choices.
- Using adjustment outputs as cautionary context for reviewer transparency.

### What is not defensible
- Framing inflated post-adjustment correlations as stronger biological truth.
- Treating residualization as causal identification.
- Overstating adjustment-stable conclusions when sign/magnitude instability is present.

## Reviewer-facing risk statement
The strongest reviewer concern is likely **over-adjustment / model-instability artifacts** (including magnitude inflation after residualization), compounded by limited blocked-permutation structure and compositional/high-dimensional constraints.

## Recommendation
For confirmatory next-phase analyses:
- Keep one minimal adjustment set (pre-specified) + unadjusted primary analysis.
- Prefer robustness criteria based on consistency across preprocessing and metrics, not maximal adjusted magnitude.
- Require directional consistency between raw and adjusted estimates before elevating confidence.
