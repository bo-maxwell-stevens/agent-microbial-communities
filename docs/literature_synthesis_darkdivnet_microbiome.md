# Literature Synthesis: DarkDivNet Metrics × Multi-Kingdom Soil Microbiomes

## Scope and reproducibility

- Date: 2026-05-19 (UTC)
- Semantic Scholar run ID: `20260519T130542Z`
- Queries executed: 24 (all successful)
- Papers logged: 192 (`185` unique titles)
- Query + paper logs: `results/literature_search_records/`
  - `queries_20260519T130542Z.csv`
  - `papers_20260519T130542Z.csv`
  - `query_01.json` ... `query_24.json`
  - `run_20260519T130542Z.json`
  - `dataset_context_darkdivnet.json`

This synthesis prioritizes **plant dark diversity/community completeness** as the primary ecological axis and evaluates how it may structure **integrated AMF + BAC + EUK + ITS** soil communities.

## DarkDivNet conceptual grounding (project-specific)

Metadata includes direct DarkDivNet-style variables:

- `dark`
- `compl`
- `compl.perc`
- `pool`
- `alpha`
- `gamma`
- `beta`
- `beta.perc`

These allow explicit testing of whether microbial communities respond to:

1. realized plant richness (`alpha`),
2. missing-but-suitable taxa (`dark`), and
3. completeness state (`compl`, `compl.perc`) relative to pool (`pool`).

## Dataset-integration constraints that matter ecologically

From `results/literature_search_records/dataset_context_darkdivnet.json`:

- Union of all sample IDs across META+AMF+BAC+EUK+ITS: `143`
- Samples present in all five tables: `84`
- Set sizes:
  - META: 99
  - AMF: 120
  - BAC: 140
  - EUK: 135
  - ITS: 139

Implication: high-dimensional integrated analyses must either:

- restrict to the 84 complete-overlap samples, or
- use modality-specific models + careful late fusion.

This is a key pseudoreplication / comparability risk if ignored.

## What the literature supports most strongly

### 1) Assembly framing is appropriate (deterministic vs stochastic)
Searches on assembly and filtering consistently returned studies linking microbial beta diversity and composition to environmental gradients and host/plant context. This supports modeling microbial turnover as a function of:

- plant completeness (`compl`, `compl.perc`),
- dark diversity (`dark`),
- edaphic filtering (`pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`),
- macroclimate (`bio1now.100`, `bio12now.100`).

### 2) Cross-kingdom integration is conceptually justified but method-sensitive
Cross-domain and cross-kingdom searches support that fungi/bacteria/protists are coupled via shared filtering and interaction regimes, but methods differ in robustness. Co-occurrence-only claims are repeatedly cautioned as potentially confounded by shared environment.

### 3) Plant diversity effects on soil microbiomes are plausible but not uniform
Plant diversity and composition searches indicate frequent associations with microbial diversity/composition, but effect size and direction are context-dependent. This reinforces controlling for strong abiotic filters and regional structure (`region`, `site.id`, `PC1`-`PC4`).

### 4) Compositional methods are non-optional
Method-focused searches strongly reinforce compositional handling (CLR/Aitchison) and sparsity-aware workflows before ordination or machine learning.

## Mechanistic hypotheses suggested by synthesis

1. **Completeness-as-filter hypothesis**: sites with high `compl` / `compl.perc` host more environmentally filtered and compositionally stable multi-kingdom microbiomes.
2. **Dark-diversity opportunity-space hypothesis**: high `dark` indicates unrealized plant niches associated with higher microbial beta turnover and weaker cross-kingdom coupling.
3. **Abiotic-mediation hypothesis**: plant completeness effects are partly mediated by pH and nutrient covariates, not purely direct biotic control.
4. **Kingdom-decoupling threshold hypothesis**: AMF/BAC/EUK/ITS coupling weakens in low-completeness communities due to stronger stochasticity or habitat limitation.

## Methodological cautions (critical)

- **Compositionality**: do not interpret raw-count correlations as ecological interactions.
- **Sparsity/zero inflation**: prevalence-aware filtering required before CLR.
- **Pseudoreplication**: use grouped CV / blocked inference (`site.id`, `region`).
- **Integration mismatch**: avoid silently mixing different sample universes across kingdoms.
- **Network over-interpretation**: treat co-occurrence as hypothesis-generating unless validated.

## Variable availability check (explicit)

### Present and directly usable
- DarkDivNet axis: `dark`, `compl`, `compl.perc`, `pool`, `alpha`, `gamma`, `beta`, `beta.perc`
- Environmental controls: `pH_KCl`, `N_pct`, `C_pct`, `P_Mehlich3_mg_100g`, `K_Mehlich3_mg_100g`, `hfp.300`, `bio1now.100`, `bio12now.100`, `bio1min.100`, `lat`, `lon`, `region`, `site.id`, `PC1`, `PC2`, `PC3`, `PC4`

### Not found in metadata (as named)
- `soil_moisture`
- `SOC`
- `elevation`
- `land_use`
- `management_intensity`
- `sequencing_batch`

## Novelty assessment

The strongest novelty appears to be the explicit fusion of:

- DarkDivNet-style plant assembly metrics (`dark`/`compl`/`pool` axis), with
- synchronized multi-kingdom soil DNA structure (AMF + BAC + EUK + ITS),
- under compositional, sparsity-aware, and overlap-constrained integration.

This moves beyond single-kingdom response models and beyond plant-only dark diversity theory toward an integrated aboveground–belowground assembly framework.
