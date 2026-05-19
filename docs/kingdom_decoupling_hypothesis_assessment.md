# Kingdom-Decoupling Threshold Hypothesis Assessment

Generated: 2026-05-19T13:22:43.626749+00:00  
Git commit: `eb784829b2b24d988d2b07e12a30765935b6fdcc`

## Hypothesis under review
As plant communities become less complete higher dark diversity and lower completeness, cross-kingdom microbial coupling weakens and assembly becomes more decoupled or stochastic.

## Ecological plausibility
- Plausible because plant composition and completeness can alter litter chemistry, root exudation, microhabitat filtering, and trophic scaffolding that influence microbial community covariance.
- Plausible directional expectation: lower completeness may weaken deterministic host or environment filtering and increase heterogeneity in microbial composition.

## Novelty and literature alignment
- Conceptually novel in this specific plant dark-diversity framing.
- Aligns with broad literature on plant-soil feedbacks and host filtering, but direct dark-diversity to multi-kingdom coupling tests are limited.

## Testability with current data
- Full integrated cohort n=84.
- This supports moderate-complexity distance-based tests of coupling gradients.
- It does not strongly support high-parameter threshold discovery at taxon level without heavy regularization.

## Alternative explanations and confounders
- Regional structure and unmeasured site processes.
- Soil chemistry and climate covariation with completeness metrics.
- Differential sequencing depth and sparsity artifacts across kingdoms.
- Technical effects if present.

## What evidence would support the hypothesis
1. Coupling metric for kingdom spaces shows reproducible monotonic decline across completeness gradient bins.
2. Signal persists after controlling for region, soil, and climate covariates with blocked permutation.
3. Pattern replicates in sensitivity analyses pairwise kingdom subsets and prevalence thresholds.

## Methodological recommendation
- Prefer distance-based or reduced-space approaches over taxon-level network edges for phase 1.
- Embedding-based integration kingdom-wise CLR plus low-rank axes is safer than direct high-dimensional coupling statistics.

## Critical risk statement
The hypothesis is promising but can become underpowered if framed as precise threshold estimation with many covariates at n about 84. It is more defensible as a gradient and coupling-strength hypothesis in phase 1.
