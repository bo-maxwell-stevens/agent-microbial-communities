# Research Ideas: DarkDivNet × Multi-Kingdom Soil Microbiomes

All ideas below prioritize the axis:

**plant dark diversity/community completeness ↔ soil multi-kingdom microbiome structure**

and use all four microbial datasets (AMF, BAC, EUK, ITS) with metadata constraints.

## Confirmed metadata variables available for modeling

- Core predictors of interest: `dark`, `compl`, `compl.perc`, `pool`, `alpha`, `gamma`, `beta`, `beta.perc`
- Environmental covariates: `pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`, `hfp.300`, `bio1now.100`, `bio12now.100`, `bio1min.100`, `lat`, `lon`, `region`, `site.id`, `PC1`-`PC4`
- Important absent variables (as named): `soil_moisture`, `SOC`, `elevation`, `land_use`, `management_intensity`, `sequencing_batch`

## Idea 1 — Microbial signatures of plant community completeness

- **Ecological hypothesis**: Increasing `compl` / `compl.perc` corresponds to convergent, environmentally filtered microbial states across AMF+BAC+EUK+ITS.
- **Literature support**: plant-diversity–microbiome association and environmental filtering studies from query blocks 11–18; compositional method support from 19.
- **Novelty assessment**: high; completeness is used as the primary plant assembly metric rather than generic richness.
- **Datasets involved**: AMF OTU, BAC OTU, EUK OTU, ITS OTU, metadata.
- **Exact metadata variables likely usable**: `compl`, `compl.perc`, `dark`, `pool`, `alpha`, `pH_KCl`, `N_pct`, `C_pct`, `region`, `site.id`.
- **Preprocessing requirements**:
  - harmonize IDs by `canonical` ↔ OTU row-ID columns,
  - intersect complete cases across all 5 sources (n=84) for integrated runs,
  - kingdom-wise prevalence filtering.
- **Compositional-data handling**: CLR with pseudocount after prevalence filtering; Aitchison distances for beta-diversity.
- **Rare-taxa filtering strategy**: keep taxa present in >=5% of samples per kingdom; sensitivity check at 2% and 10%.
- **Proposed workflow**:
  1. build per-kingdom CLR matrices,
  2. ordination constrained by completeness and covariates,
  3. multi-block integration (concatenated CLR or block-level latent factors).
- **Validation strategy**: grouped CV by `site.id` / `region`; permutation tests for constrained ordination terms.
- **Expected figures/tables**:
  - completeness gradient vs ordination axes,
  - variance partition barplot,
  - per-kingdom effect-size table.
- **Manuscript potential**: strong primary results section.
- **Risks/limitations**: overlap reduction to n=84 may limit power; confounding by pH.
- **Computational difficulty**: medium-high.

## Idea 2 — Cross-kingdom coupling strength along dark-diversity gradients

- **Ecological hypothesis**: High `dark` and low `compl` weaken coupling among kingdom-specific community structures (AMF↔BAC↔EUK↔ITS).
- **Literature support**: cross-kingdom interaction and assembly searches (6–10, 15–18), network caution search (22).
- **Novelty assessment**: very high in DarkDivNet context.
- **Datasets involved**: all four OTU tables + metadata.
- **Exact metadata variables likely usable**: `dark`, `compl`, `pool`, `beta`, `pH_KCl`, `bio1now.100`, `bio12now.100`, `region`.
- **Preprocessing requirements**:
  - standardize sample overlap,
  - kingdom-wise CLR transforms,
  - construct kingdom-level distance matrices.
- **Compositional-data handling**: Aitchison distances + Procrustes / RV-coefficient style coupling metrics.
- **Rare-taxa filtering strategy**: prevalence >=5% primary; remove ultra-rare singletons pre-CLR.
- **Proposed workflow**:
  1. compute kingdom-specific beta diversity,
  2. quantify pairwise coupling of distance structures,
  3. model coupling as function of `dark`/`compl` + covariates.
- **Validation strategy**: spatially/group-blocked permutations within `region` strata.
- **Expected figures/tables**:
  - coupling heatmaps across completeness bins,
  - regression coefficient plots,
  - sensitivity table by filtering threshold.
- **Manuscript potential**: centerpiece novelty claim.
- **Risks/limitations**: coupling is not direct interaction evidence.
- **Computational difficulty**: medium.

## Idea 3 — Deterministic vs stochastic assembly shifts with completeness

- **Ecological hypothesis**: high `compl` systems exhibit stronger deterministic assembly signatures; low-completeness systems show higher stochasticity and turnover.
- **Literature support**: deterministic/stochastic assembly and environmental filtering queries (15–18).
- **Novelty assessment**: high, especially with four-kingdom comparative framing.
- **Datasets involved**: AMF/BAC/EUK/ITS OTUs + metadata.
- **Exact metadata variables likely usable**: `compl`, `compl.perc`, `dark`, `beta`, `beta.perc`, `pH_KCl`, `N_pct`, `C_pct`, `site.id`.
- **Preprocessing requirements**: balanced sample subsets across completeness quantiles to avoid class imbalance artifacts.
- **Compositional-data handling**: CLR + null-model compatible distance framework.
- **Rare-taxa filtering strategy**: prevalence >=5% plus robustness at >=10%.
- **Proposed workflow**:
  1. partition samples by completeness quantiles,
  2. compare observed beta structure to null expectations,
  3. quantify deterministic signal by kingdom and jointly.
- **Validation strategy**: bootstrap confidence intervals by kingdom and region.
- **Expected figures/tables**:
  - deterministic/stochastic index vs completeness,
  - kingdom comparison forest plot,
  - null-model diagnostics.
- **Manuscript potential**: high (ecological theory angle).
- **Risks/limitations**: null-model choice sensitivity.
- **Computational difficulty**: medium-high.

## Idea 4 — Predicting plant completeness from integrated microbial composition

- **Ecological hypothesis**: combined multi-kingdom microbiome profiles predict `compl` better than any single kingdom.
- **Literature support**: sparse ML + SHAP searches (20–21) and compositional methods (19).
- **Novelty assessment**: high translational value (predictive + interpretable).
- **Datasets involved**: all four OTU datasets + metadata.
- **Exact metadata variables likely usable**:
  - target: `compl` (continuous) and/or `compl.perc`,
  - predictors: CLR features from AMF/BAC/EUK/ITS,
  - controls: `pH_KCl`, `N_pct`, `C_pct`, `region`, `site.id`.
- **Preprocessing requirements**:
  - nested feature filtering/selection inside CV,
  - avoid leakage in any scaling/CLR/pseudocount pipeline.
- **Compositional-data handling**: CLR features; consider PCA-on-CLR per kingdom before late fusion.
- **Rare-taxa filtering strategy**: prevalence >=5% then variance thresholding inside training folds only.
- **Proposed workflow**:
  1. single-kingdom baseline models,
  2. stacked multi-kingdom model,
  3. SHAP-based interpretation and stability checks.
- **Validation strategy**: grouped nested CV by `site.id` or `region`; repeated splits.
- **Expected figures/tables**:
  - model performance comparison (single vs integrated),
  - SHAP summary for top microbial predictors,
  - calibration and residual diagnostics.
- **Manuscript potential**: high (method + ecology bridge).
- **Risks/limitations**: high-dimensional p>>n, overfitting risk.
- **Computational difficulty**: high.

## Idea 5 — Environmental mediation of dark-diversity effects on microbiomes

- **Ecological hypothesis**: dark-diversity/completeness effects on microbiomes are partially mediated by abiotic gradients (especially `pH_KCl` and nutrient variables).
- **Literature support**: pH and environmental filtering searches (17–18), plant-microbiome searches (11–14).
- **Novelty assessment**: medium-high; clarifies mechanism, not just association.
- **Datasets involved**: all four OTU datasets + metadata.
- **Exact metadata variables likely usable**: `dark`, `compl`, `compl.perc`, `pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`, `bio1now.100`, `bio12now.100`.
- **Preprocessing requirements**: collinearity diagnostics among edaphic/climate covariates.
- **Compositional-data handling**: CLR-based response summaries (ordination axes, diversity indices in Aitchison space).
- **Rare-taxa filtering strategy**: prevalence + abundance floor to stabilize ordination loadings.
- **Proposed workflow**:
  1. fit baseline dark-diversity effect models,
  2. add environmental mediators,
  3. compare direct vs mediated pathways (variance partition / path-style decomposition).
- **Validation strategy**: blocked resampling by region; robustness to alternative covariate sets.
- **Expected figures/tables**:
  - path diagram of direct/indirect effects,
  - variance partition stacked bars,
  - kingdom-specific mediation table.
- **Manuscript potential**: strong companion/secondary paper.
- **Risks/limitations**: mediation remains observational (non-causal without experiments).
- **Computational difficulty**: medium.

## Most promising immediate manuscript direction

A unified manuscript combining Ideas 1–3 appears strongest: **completeness-gradient structure + cross-kingdom coupling + assembly mechanism shifts**, with Idea 4 as a predictive extension.
