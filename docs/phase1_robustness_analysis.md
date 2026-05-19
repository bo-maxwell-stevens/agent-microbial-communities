# Phase 1 Robustness Analysis (Reduced-Space Multi-Kingdom Coupling)

## Scope and guardrails
This phase is a *validation/stability* exercise, not a manuscript-claim phase.

- No causal claims.
- No taxon-level interaction networks.
- No definitive assembly-mechanism claims.
- Focus: whether reduced-space coupling signals are stable across preprocessing choices and conservative adjustments.

## Inputs and overlap
- Metadata: `data/Final_data_with_diversity_prefixed.csv`
- Kingdom tables: `AMF`, `BAC`, `EUK`, `ITS`
- Full overlap used in this phase: **84 samples**

## Methods tested
Implemented in `scripts/analysis/phase1_robustness_analysis.py`.

### 1) Prevalence sensitivity
Thresholds tested: `0.01`, `0.05`, `0.10`, `0.20`.

Tracked:
- retained taxa (`features_after`)
- retained taxa fraction
- retained variance fraction proxy

Output: `results/phase1_robustness/prevalence_threshold_sensitivity.csv`

### 2) Dimensionality sensitivity
PCA dimensions tested: `5`, `10`, `20`.

Output: reflected in scenario rows of:
- `robustness_summary.csv`
- `coupling_metric_stability.csv`

### 3) Coupling metric sensitivity
For each kingdom pair and scenario:
- Procrustes correlation
- Mantel-like Spearman correlation on distance vectors
- RV coefficient
- Distance-vector Pearson correlation (embedding-space correlation summary)

Output: `coupling_metric_stability.csv`

### 4) Environmental confounding checks (conservative)
Covariates (if present):
- `pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`, `hfp.300`, `bio1now.100`, `bio12now.100`, `region`, `PC1-4`

Approach:
- one-hot encoding for categorical covariates
- residualized embeddings before recomputing coupling metrics
- reporting attenuation/delta rather than causal interpretation

Output: `environmental_adjustment_summary.csv`

### 5) Null-model checks
Per pair/metric/scenario:
- shuffled-sample-label null
- random alignment (orthonormal rotation) null
- null mean/sd/quantiles and permutation p-values

Output: `null_model_results.csv`

### 6) Association stability (auxiliary)
Plant-side metrics where available (e.g., `compl`, `dark`) were tested against reduced microbial summaries (`*_PC1`, cross-kingdom dispersion), with and without covariate residualization.

Output: `association_stability.csv` (lightweight helper)

## Robustness findings (what appears stable)
Across threshold × PCA scenarios:

- **Most stable pairwise coupling pattern:** `EUK-ITS` (consistently positive and relatively low variability across all four metric families).
- `AMF-ITS` and `AMF-EUK` were generally positive and directionally stable, but less stable than `EUK-ITS`.
- Scenario-level mean coupling was weakest at threshold `0.01` and stronger from `0.05` to `0.20`, suggesting very-lenient prevalence filtering can dilute signal.

## Findings that were sensitive/unstable
- Pairings involving **BAC with EUK/ITS** showed higher variability and occasional weak/negative values in distance-correlation metrics.
- Several association signs/magnitudes changed across preprocessing scenarios.
- Covariate-adjusted association/coupling values were sometimes *much larger* than raw values (see confounding doc), indicating potential over-adjustment artifacts and inferential fragility.

## Reviewer-risk assessment
### Main vulnerabilities
1. **Pseudoreplication / permutation structure limitations**
   - Sample structure provides limited robust blocking options; independence assumptions remain a concern.
2. **High-dimensional compositional data risks**
   - CLR+PCA reduces dimension but does not fully eliminate compositional artifacts.
3. **Adjustment instability**
   - Large residualization-induced shifts (including sign flips/amplification) suggest model sensitivity to covariate specification.
4. **Sample size constraints (n=84 overlap)**
   - Adequate for exploratory reduced-space screening, but limited for strong multivariable claims.

### What is safest to carry forward
- Directional statement that **some reduced-space cross-kingdom coupling signals (especially EUK-ITS) are reproducible across multiple preprocessing settings**.
- Explicitly frame as *exploratory but comparatively robust within this framework*.

### What likely should be avoided/abandoned at this stage
- Strong claims relying on BAC-linked pair effects alone.
- Any claim that survives only after aggressive covariate residualization with large magnitude inflation.
- Causal ecological mechanism claims.

## Feasibility status after robustness phase
- The project remains **manuscript-feasible** *if* claims are narrowed to robust reduced-space reproducibility findings and framed conservatively.
- The current framework is defensible for an exploratory/stability-focused manuscript section, but not for strong mechanistic inference.

## Suggested next step
Run a **pre-registered confirmatory reduced-space subset**:
- restrict to top stable pair(s) and stable metric family
- predefine one prevalence threshold window (e.g., `0.05-0.10`) and PCA dimension rule
- keep conservative permutation inference and report uncertainty intervals
- treat environmental adjustment as sensitivity analysis, not causal correction
