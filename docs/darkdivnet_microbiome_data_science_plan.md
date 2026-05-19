# DarkDivNet × Microbiome Data Science Plan

## 1) Recommended first analyses (lightweight, high-yield)

1. **Canonical overlap lock-in**
   - Build integrated sample set (`n=84` complete overlap) and kingdom-specific extended sets.
2. **Kingdom-wise compositional preprocessing sanity checks**
   - prevalence/zero profiles, CLR readiness, filtering sensitivity.
3. **Completeness-gradient ordination pilot**
   - Aitchison distance ordinations per kingdom + integrated block.
4. **Variance partition pilot**
   - dark-diversity/completeness variables vs edaphic/climate controls.

## 2) Sample harmonization strategy

- Use metadata `canonical` as primary join key.
- Map OTU first-column sample IDs (`Unnamed: 0`) to canonical IDs.
- Maintain three analysis tiers:
  - **Tier A**: all-kingdom strict overlap (`n=84`) for integrated analyses.
  - **Tier B**: kingdom-specific overlaps for sensitivity/power checks.
  - **Tier C**: metadata-only contextual checks.
- Store explicit inclusion/exclusion logs for each tier.

## 3) Filtering strategy

- Remove taxa absent in >95% of samples (primary threshold).
- Sensitivity runs at 90% and 98% absence.
- Keep filtering decisions kingdom-specific (different sparsity regimes).

## 4) CLR/Aitchison recommendations

- Add small pseudocount post-filtering.
- Perform CLR separately per kingdom.
- Use Aitchison distance for beta-diversity and clustering.
- Do not mix raw counts with CLR-derived models.

## 5) Ordination roadmap

- Per kingdom:
  - PCoA/NMDS on Aitchison distances
  - envfit-style overlays for `dark`, `compl`, `compl.perc`, `pH_KCl`.
- Cross-kingdom:
  - concatenate standardized CLR latent components
  - integrated ordination colored by completeness quantiles.
- Report constrained variance with and without abiotic controls.

## 6) ML roadmap

- Targets:
  - primary: `compl`
  - secondary: `compl.perc`, `dark`
- Model sequence:
  1. baseline environmental-only model,
  2. single-kingdom microbial models,
  3. integrated multi-kingdom model.
- Use sparse/regularized learners and tree ensembles as complementary tools.

## 7) SHAP interpretation strategy

- Compute SHAP only on held-out predictions from grouped CV.
- Aggregate SHAP by taxonomic/functional groups where possible.
- Compare SHAP stability across CV folds and filtering thresholds.
- Avoid causal language from SHAP importance.

## 8) Cross-kingdom integration strategy

- Preferred initial approach:
  - per-kingdom CLR + dimensionality reduction,
  - late-fusion model combining kingdom embeddings,
  - compare against early-fusion concatenation.
- Evaluate whether integrated models outperform best single kingdom.

## 9) Reproducibility plan

- Keep all query/model/preprocessing manifests under `results/`.
- Save full parameter files for each analysis run.
- Enforce branch-local development (`darkdivnet-microbiome-ideas` and descendants).
- Keep raw data read-only (`data/` untouched).

## 10) Branch structure recommendations

- `darkdivnet-microbiome-ideas` (current): literature + planning docs/scripts
- future branches:
  - `darkdivnet-harmonization`
  - `darkdivnet-compositional-qc`
  - `darkdivnet-ordination-v1`
  - `darkdivnet-ml-v1`
  - `darkdivnet-manuscript-figures`

## 11) Future HPC scaling opportunities

- Parallel kingdom-wise CLR and distance computations.
- Distributed hyperparameter tuning with grouped CV.
- Bootstrap/permutation workflows (variance partition, null models) on cluster.
- Potential sparse matrix acceleration for BAC high-dimensional features.

## 12) Biggest technical risks to manage early

- Sample-overlap attrition (84 complete cases).
- Confounding of completeness effects with pH and region.
- p>>n overfitting in integrated ML.
- Over-interpretation of co-occurrence as interaction.
