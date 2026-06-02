# Manuscript Blueprint (Phase M1)

## Scope lock

This blueprint is based only on completed outputs (Phase 2, 4, 5B, 5C, 5D) and does **not** introduce new analyses, altered scientific results, rerun HPC jobs, or new hypotheses.

## 1) Candidate title options

1. **Cross-domain soil microbial coupling is jointly structured by abiotic gradients and plant-diversity context**
2. **Integrative synthesis of bacteria–fungi–eukaryote coupling reveals pH-centered environmental structure and alpha-diversity-linked modulation**
3. **From coupling to context: a synthesis of cross-domain microbial structure across abiotic and plant-diversity gradients**
4. **BAC- and AMF-centered coupling patterns reveal distinct environmental and plant-associated signatures in soil microbial communities**

## 2) Central biological message

Cross-domain microbial coupling is strongest for BAC↔ITS and EUK↔ITS combinations, environmental structure is consistently pH-centered, and AMF-centered pairings—while more weakly coupled overall—retain reproducible plant-diversity-associated signal (especially alpha-diversity effects) when integrated across completed analyses.

## 3) Major hypotheses tested (already completed phases)

- **H1 (Coupling hierarchy):** Pairings differ in coupling strength (Mantel + Procrustes synthesis), with BAC↔ITS and EUK↔ITS expected to rank highest.
- **H2 (Environmental structuring):** Environmental predictors explain meaningful variation in pair-level structure, with pH among dominant predictors.
- **H3 (Geographic sensitivity):** Geography-aware model variants alter explained variation relative to primary models.
- **H4 (Plant-diversity incremental value):** Plant-diversity terms add explanatory power beyond abiotic baseline models.
- **H5 (Domain-specific interpretation):** AMF-centered pairings are comparatively less strongly coupled but comparatively more plant-associated.

## 4) Major findings (from existing outputs)

- Top synthesis coupling ranks: BAC↔ITS (presence/absence), EUK↔ITS (presence/absence), EUK↔ITS (CLR).
- Environmental layer: best-fit model class frequently geography-sensitivity; `pH_KCl` repeatedly appears as top predictor.
- Plant-diversity layer: hypothesis B (`abiotic_plus_alpha`) is repeatedly best-performing among non-base hypotheses.
- Integrated interpretation labels classify EUK↔ITS presence/absence as strongly coupled + environment structured + plant associated.
- AMF↔ITS and AMF↔EUK are weaker in coupling score but retain positive plant-diversity-added variation.

## 5) Proposed journal targets

Primary target:
- **The ISME Journal** (microbial ecology, community assembly, cross-domain interactions)

Secondary targets:
- **Microbiome** (multi-omics/microbial community structure emphasis)
- **Soil Biology and Biochemistry** (soil ecological mechanisms and environmental controls)
- **mSystems** (quantitative microbial systems and community assembly framing)

## 6) Main-text figure list

- **Figure 1:** `results/phase5d_synthesis/final_coupling_network.png`
  - Integrative cross-domain coupling structure and rank contrasts.
- **Figure 2:** `results/phase5d_synthesis/final_driver_heatmap.png`
  - Environmental driver contribution patterns across pairings/branches.
- **Figure 3:** `results/phase5d_synthesis/final_plant_hypothesis_comparison.png`
  - Plant-diversity hypothesis comparison and effect decomposition.
- **Figure 4:** `results/phase5c_plant_diversity/phase5c_model_delta_adj_r2.png`
  - Incremental adjusted R² gains over abiotic baselines.
- **Figure 5:** `results/phase5c_plant_diversity/phase5c_pair_comparisons.png`
  - Pair-level contrasts highlighting BAC-inclusive vs AMF-centered patterns.

## 7) Supplementary figure list

- **Supplementary Figure S1:** `results/phase5d_synthesis/final_analysis_flowchart.png`
  - Workflow provenance and synthesis-only integration path.
- **Supplementary Figure S2:** `results/phase5c_plant_diversity/phase5c_hypothesis_rankings.png`
  - Full ranking detail of plant-diversity hypotheses.

## 8) Required tables

Main text:
- **Table 1:** `results/phase5d_synthesis/final_pair_synthesis.csv`
- **Table 2:** `results/phase5d_synthesis/final_coupling_rankings.csv`
- **Table 3:** `results/phase5d_synthesis/final_environment_driver_summary.csv`
- **Table 4:** `results/phase5d_synthesis/final_plant_diversity_summary.csv`

Supplement:
- **Table S1:** `results/phase5_bac_integration/phase5_bac_coupling_summary.csv`
- **Table S2:** `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`
- **Table S3:** `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`
- **Table S4:** `results/phase5c_plant_diversity/phase5c_model_comparison.csv`
- **Table S5:** `results/phase5c_plant_diversity/phase5c_predictor_effects.csv`
- **Table S6:** `results/phase4_coupling_inference/phase4_mantel_inference.csv`
- **Table S7:** `results/phase4_coupling_inference/phase4_procrustes_bootstrap.csv`
- **Table S8:** `results/phase2_confirmatory_coupling/phase2_coupling_summary.csv`

## 9) Missing citations (priority gaps before drafting full manuscript)

High-priority gaps to close in final bibliography curation:

1. A canonical cross-domain soil network paper explicitly integrating bacteria + fungi + protists under ecological assembly framing (one broader benchmark beyond current retrieved set).
2. A dedicated AMF ecology synthesis in natural grassland/soil systems that directly supports AMF-centered interpretation in this manuscript context.
3. A dark-diversity methods/application paper that explicitly links community completeness metrics to plant–soil microbial inference scope.
4. One co-occurrence methodological caution reference focusing on compositional data constraints and false-positive edges.
5. One contemporary synthesis (post-2020) on deterministic vs stochastic microbial assembly in soil with network interpretation guidance.

## 10) Section-by-section manuscript outline

1. **Introduction**
   - Why cross-domain coupling matters for soil ecosystem interpretation.
   - Known environmental structuring (especially pH) and unresolved role of plant-diversity context.
   - Rationale for integrated synthesis across completed analytical phases.

2. **Study system and data provenance**
   - Cohort and matrix provenance from confirmed phase outputs.
   - Domain pair definitions (BAC↔ITS, EUK↔ITS, AMF↔ITS, AMF↔EUK).
   - Presence/absence and CLR branch rationale.

3. **Analytical framework (completed pipeline recap)**
   - Phase 2/4 coupling inference outputs.
   - Phase 5B environmental driver layer.
   - Phase 5C plant-diversity hypothesis layer.
   - Phase 5D synthesis-only integration logic.

4. **Results I: Coupling hierarchy**
   - Pair/branch ranking and uncertainty context.
   - BAC-inclusive vs AMF-centered contrasts.

5. **Results II: Environmental structure**
   - dbRDA explained variation patterns and model type contrasts.
   - pH-centered predictor recurrence and geography sensitivity deltas.

6. **Results III: Plant-diversity association layer**
   - Hypothesis ranking and incremental gains vs abiotic baseline.
   - Alpha/pool/dark/compl effect profile.

7. **Results IV: Integrated synthesis interpretation**
   - Rule-based interpretation classes.
   - Biological interpretation of strongly coupled vs weakly coupled-but-plant-associated pairings.

8. **Discussion**
   - Ecological implications for cross-domain soil organization.
   - AMF-centered interpretation nuance.
   - Environmental and plant-context co-structuring.
   - Limitations of synthesis metrics and non-inferential integration.

9. **Methods (manuscript-ready, reproducibility-focused)**
   - Exact source files/tables used by synthesis.
   - Derived metric definitions and classification thresholds.
   - No-new-analysis compliance statement.

10. **Data/code availability and reproducibility appendix**
   - Inventory tables/figures and artifact map.
   - Version anchor and branch/checkpoint references.

## Artifact links created in Phase M1

- `results/manuscript_preparation/figure_inventory.csv`
- `results/manuscript_preparation/table_inventory.csv`
- `results/manuscript_preparation/citation_inventory.csv`

