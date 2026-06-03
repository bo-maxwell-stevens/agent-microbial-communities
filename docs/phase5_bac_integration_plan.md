# Phase 5A BAC Integration Plan

## Objective
Extend deterministic Phase 2 + Phase 4 cross-domain coupling to include BAC and evaluate whether bacterial community structure dominates, matches, or differs from AMF/fungal/eukaryotic coupling.

## Inputs
- data/AMF_OTU_table_final.tsv
- data/BAC_OTU_table_final.tsv
- data/EUK_OTU_table_final.tsv
- data/ITS_OTU_table_final.tsv
- results/phase2_confirmatory_coupling/sample_cohort_used.csv

## Cohort policy
- Use the existing 84-sample cohort from Phase 2.
- Hard fail if any domain lacks any cohort sample.

## Domain pairs
- BAC↔AMF
- BAC↔ITS
- BAC↔EUK
- AMF↔ITS
- AMF↔EUK
- EUK↔ITS

## Branches and thresholds
- Branches: presence/absence, CLR
- Prevalence thresholds: 0.05 and 0.10

## Methods reused
- Presence/absence branch: prevalence filter -> binary transform -> Jaccard distance -> deterministic PCoA
- CLR branch: prevalence filter -> relative abundance -> CLR transform -> Euclidean distance -> deterministic PCA (svd_solver="full")
- Mantel permutation inference: N_PERMUTATIONS=999 (seeded)
- Procrustes bootstrap: N_BOOTSTRAPS=120 (seeded)

## Outputs
Directory: results/phase5_bac_integration/

- phase5_bac_coupling_summary.csv
- phase5_bac_mantel_inference.csv
- phase5_bac_procrustes_bootstrap.csv
- phase5_bac_rank_summary.csv
- figures/mantel_effect_sizes.png
- figures/procrustes_effect_sizes.png
- figures/domain_pair_rankings.png

## QC gates
1. Confirm all four domains cover the 84-sample cohort.
2. Deterministic rerun check on summary metrics.
3. Confirm branches are not globally identical.
4. Confirm no environmental predictor logic is used.
5. Pass py_compile, full script run, pytest -q, and git diff --check.

## Notes
- Script writes checkpoint CSV outputs after every pair/branch/threshold combination.
- Phase 5A is coupling-only (no environmental partitioning in this stage).
