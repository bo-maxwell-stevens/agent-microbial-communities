# Phase 2 Confirmatory Coupling Report

## Cohort

The primary Phase 2 cohort was the strict full-overlap cohort:

- AMF
- EUK
- ITS
- sample-level metadata

The final aligned cohort contained 84 samples. Sample IDs were preserved in canonical form, for example `D009.N1`, and sample order was verified to be identical across all analyzed matrices.

## Analysis Scope

Phase 2 was restricted to the three predefined cross-kingdom pairs:

- EUK ↔ ITS
- AMF ↔ ITS
- AMF ↔ EUK

BAC was intentionally excluded from the primary Phase 2 analysis because of its very high dimensionality and should be handled separately in Phase 2b.

## Preprocessing

The analysis compared:

- 5% prevalence threshold
- 10% prevalence threshold
- presence/absence branch
- CLR branch

Feature filtering was column-only. The 84-sample cohort was fixed and preserved throughout all preprocessing, embedding, and metric-computation steps.

## Coupling Metrics

The Phase 2 workflow computed:

- Procrustes Fit
- Mantel Spearman

All 12 pair × threshold × branch combinations produced populated metric values.

## Main Findings

The most robust coupling by Mantel Spearman was:

- EUK ↔ ITS, presence/absence branch, 10% threshold
- Mantel Spearman = 0.607268

The strongest Procrustes Fit was:

- AMF ↔ EUK, CLR branch, 10% threshold
- Procrustes Fit = 0.182380

## Interpretation

EUK ↔ ITS appears to be the strongest and most stable cross-kingdom coupling signal in this confirmatory analysis.

AMF-linked couplings were detectable but more sensitive to preprocessing choices, especially prevalence threshold and transformation branch. This is consistent with the lower richness, lower depth, and greater sparsity previously observed for AMF.

These results support continued investigation of cross-kingdom ecological coordination, but they should not yet be interpreted as mechanistic or causal evidence.

## Cautions

- No causal claims should be made from this analysis.
- AMF-linked coupling should be treated as biologically interesting but preprocessing-sensitive.
- Environmental adjustment and BAC integration remain future steps.
- BAC should be analyzed separately because its high dimensionality may dominate integrated analyses.

## Recommended Next Step

Proceed to Phase 2b: bacterial coupling sensitivity.

Phase 2b should test:

- BAC ↔ EUK
- BAC ↔ ITS
- BAC ↔ AMF

using stronger dimensionality controls and conservative prevalence filtering.
