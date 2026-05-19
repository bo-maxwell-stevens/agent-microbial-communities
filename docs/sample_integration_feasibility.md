# Sample Integration Feasibility Audit

Generated: 2026-05-19T13:22:43.626749+00:00  
Git commit: `eb784829b2b24d988d2b07e12a30765935b6fdcc`

## Key counts
- META samples: 99
- AMF samples: 120
- BAC samples: 140
- EUK samples: 135
- ITS samples: 139
- Union across META+AMF+BAC+EUK+ITS: 143
- Full-overlap cohort all five: 84

## Pairwise overlap counts
See `results/feasibility/pairwise_overlap_counts_matrix.csv` and `pairwise_overlap_jaccard_matrix.csv`.

## Missingness structure
- Presence matrix: `results/feasibility/sample_presence_matrix.csv`
- Pattern frequencies: `results/feasibility/missingness_patterns.csv`

Most missingness is driven by metadata coverage META having fewer samples than sequencing tables, not by large discordance among AMF/BAC/EUK/ITS, which are largely co-registered.

## Duplicate sample audit
See `results/feasibility/duplicate_sample_ids.csv`.
- Interpretation: duplicates should be treated as technical anomalies requiring de-duplication before inferential modeling.

## Overlap by region and site.id
See `results/feasibility/region_overlap_summary.csv`.

Statistical structure check region-level permutation on full-overlap membership among META samples:
- observed max-minus-min overlap rate across regions: 1.000
- permutation p-value: 1.0000
- permutations: 2000

Interpretation:
- If p lower than 0.05, overlap loss is region-structured, increasing confounding risk.
- If p at least 0.05, strong structure is not statistically evident, but power is limited.
- `site.id` has about one sample per site, so inferential site-level missingness tests are underpowered.

## Integration strategy assessment
Given overlap geometry and dimensionality:

1. Full-overlap only n=84
   - Pros: cleanest inferential alignment across plant metrics and all kingdoms.
   - Cons: reduced n and power, especially for high-dimensional supervised models.
   - Use for: primary integrative analyses.

2. Pairwise overlap subsets
   - Pros: larger effective n for targeted kingdom-pair questions.
   - Cons: effect-size comparability across pairs is harder.
   - Use for: sensitivity analyses and mechanism probing.

3. Kingdom-specific analyses
   - Pros: maximizes per-kingdom sample and feature signal.
   - Cons: does not directly test cross-kingdom coupling.
   - Use for: supporting analyses and robustness checks.

4. Latent embeddings and hierarchical integration
   - Pros: compresses p much larger than n regime and improves statistical stability.
   - Cons: may reduce direct taxon-level interpretability.
   - Use for: core integrative pipeline under current n.

## Statistical tradeoff conclusion
A defensible architecture is full-overlap for primary cross-kingdom inference plus pairwise and kingdom-specific sensitivity analyses, with aggressive dimensionality reduction and blocked validation to mitigate pseudoreplication and overfitting.
