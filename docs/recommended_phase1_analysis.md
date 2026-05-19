# Recommended Phase 1 Analysis

Generated: 2026-05-19T13:22:43.626749+00:00  
Git commit: `eb784829b2b24d988d2b07e12a30765935b6fdcc`

## Recommended pipeline
Distance-based multi-kingdom coupling analysis on full-overlap cohort with prevalence-filtered CLR embeddings and blocked permutation inference.

## Exact samples to use
- Primary cohort: samples present in META+AMF+BAC+EUK+ITS n=84.
- Sensitivity cohort: full-overlap with minimum library threshold at least 1000 reads in all kingdoms n=52. See `full_overlap_retention_by_library_threshold.csv`.

## Exact kingdoms to include
AMF, BAC, EUK, ITS linked to plant dark-diversity and completeness metrics from META.

## Filtering recommendations
1. Remove zero-library samples per kingdom.
2. Within each kingdom in the analysis cohort, prevalence-filter taxa at least 5 percent with 2 percent and 10 percent sensitivity checks.
3. Optional cap on ultra-low-library samples if instability remains threshold grid already provided.

## Normalization strategy
- Convert counts to compositional representation with conservative pseudocount.
- Apply CLR transform after filtering.
- Standardize reduced components before cross-kingdom integration.

## Dimensionality reduction approach
- Kingdom-wise PCA or sparse PCA on CLR matrix.
- Retain a small fixed number of axes per kingdom for example top 5 to 10, justified by explained variance and stability.

## Validation strategy
- Blocked permutation tests respecting region and site structure where possible.
- Sensitivity analyses over prevalence thresholds and library thresholds.
- Avoid unconstrained feature-level model tuning in phase 1.

## Expected outputs
- Coupling-strength versus completeness gradients effect sizes and permutation p-values.
- Robustness profile across filtering choices.
- Clear decision on whether stronger integrative modeling is justified in phase 2.

## Computational cost
Moderate and feasible on current infrastructure without heavy HPC.

## Expected novelty and manuscript potential
High ecological relevance and publishable if effect directions are consistent and robust under sensitivity checks.

## Key risks
- n about 84 remains limiting for complex interaction models.
- Over-interpretation risk if coupling metrics are not robust across filtering settings.

## Why this is the strongest next step
It is biologically meaningful, statistically defensible under current overlap constraints, and provides a decisive feasibility signal before expensive model development.
