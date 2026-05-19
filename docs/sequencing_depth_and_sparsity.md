# Sequencing Depth and Sparsity Assessment

Generated: 2026-05-19T13:22:43.626749+00:00  
Git commit: `eb784829b2b24d988d2b07e12a30765935b6fdcc`

## Per-kingdom library-size and sparsity summaries
- **AMF**: n_samples=120, n_features=386, median_library=1792.5, IQR_library=[440.8, 4201.0], zero_library=0 (0.0%), median_richness=24.5, sparsity=0.9226
- **BAC**: n_samples=140, n_features=291699, median_library=15933.0, IQR_library=[7750.5, 27992.5], zero_library=0 (0.0%), median_richness=3537.0, sparsity=0.9874
- **EUK**: n_samples=135, n_features=58205, median_library=16124.0, IQR_library=[9528.5, 27647.0], zero_library=0 (0.0%), median_richness=789.0, sparsity=0.9859
- **ITS**: n_samples=139, n_features=26285, median_library=3498.0, IQR_library=[2232.5, 6309.5], zero_library=0 (0.0%), median_richness=261.0, sparsity=0.9898

Source tables:
- `results/feasibility/sequencing_qc_by_kingdom.csv`
- `results/feasibility/sample_library_sizes_long.csv`
- `results/feasibility/sample_richness_long.csv`
- `results/feasibility/taxon_prevalence_quantiles.csv`
- `results/feasibility/prevalence_threshold_retention.csv`

## Zero-library and imbalance checks
- Zero-library samples should be excluded before compositional transforms.
- Strong feature and sample imbalance is expected especially BAC and necessitates prevalence filtering and dimensionality reduction.

## Prevalence and suggested thresholds
Threshold retention is in `prevalence_threshold_retention.csv`.

Recommended baseline filter for initial integrative work:
- Per kingdom retain taxa with prevalence at least 5 percent within analysis cohort.
- Sensitivity checks at 2 percent and 10 percent prevalence filters.

Rationale:
- Less than 2 percent retains many near-idiosyncratic features unstable for inference.
- At least 10 percent may over-prune and remove ecologically relevant rare taxa.

## Approximate compositional stability and CLR expectations
- Aitchison geometry is feasible after removing zero-library samples and prevalence-filtering sparse taxa.
- CLR on raw ultra-sparse matrices is unstable due to pseudocount sensitivity.
- Safer route: prevalence-filter then CLR then low-rank representation before integration.

## Dimensionality reduction necessity
Dimensionality reduction is essential for BAC/EUK/ITS and still advisable for AMF, given n about 84 for full-overlap analyses.
