# Title

Cross-domain soil microbial coupling reflects strong environmental filtering with secondary plant-diversity structure

## Abstract
Cross-domain coupling among soil microbial communities can emerge from shared environmental filtering, direct biotic interactions, or both. Using completed outputs only from a fixed 84-sample cohort, we synthesized pairwise coupling evidence (Mantel and Procrustes), environmental driver models, and plant-diversity hypothesis comparisons across BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK combinations. BAC↔ITS (presence/absence) retained the highest composite coupling summary value (0.574), while EUK↔ITS combinations ranked second and third (0.538 and 0.535). Environmental structure was substantial across pair-branch combinations (adjusted R² 0.188–0.278), with pH_KCl consistently dominant and the largest mean predictor delta adjusted R² (0.111). Plant-diversity increments were modest but repeatable: hypothesis B (abiotic_plus_alpha) ranked highest (mean delta adjusted R² = 0.013), and alpha diversity exceeded pool (0.009), dark (0.003), and completeness (-0.004). AMF-linked pairs showed lower overall coupling than BAC↔ITS/EUK↔ITS but larger plant-associated increments (up to 0.019). We therefore interpret BAC↔ITS as strongly coupled but also strongly environment-structured, with environmental filtering as the primary competing explanation and direct interaction remaining plausible but unconfirmed in this observational framework. Mantel and Procrustes are interpreted as complementary metrics that capture different properties of cross-domain organization rather than conflicting tests. Overall, environmental filtering provides the dominant explanatory axis, while plant-diversity context contributes secondary, biologically structured variation. [R1, R2, R3, R4, R5, R6, R7, R8]

## Introduction
Cross-domain organization of soil microbial communities is increasingly recognized as a systems-level property, but interpretation is often challenged by the coexistence of deterministic filtering and stochastic assembly processes [R1, R2, R8]. When community patterns co-vary across domains, the resulting coupling can arise through at least three non-exclusive routes: shared abiotic constraints, direct or indirect biotic interactions, and parallel responses to plant-context structure [R1, R8, R10]. Distinguishing among these routes is central for robust ecological inference.

Environmental filtering, particularly along soil pH gradients, is one of the most reproducible structuring mechanisms reported across soil microbiome studies [R3, R4, R5]. Consequently, strong cross-domain coupling should not be interpreted as interaction evidence by default; it may instead reflect synchronized responses to shared environmental gradients. This filtering-first interpretation is especially relevant when predictor rankings repeatedly identify pH-centered structure.

Plant diversity concepts (alpha diversity, species pool, dark diversity, and completeness) provide a complementary context for testing whether biotic environment adds explanatory structure beyond abiotic baselines [R9, R11, R12]. These metrics are ecologically informative but can be partially non-independent, requiring effect-size-aware and collinearity-aware interpretation. In parallel, AMF occupy a plant-root interface role that may produce different coupling architecture than BAC-inclusive pairings, even when total coupling is lower [R6, R7].

Within this constrained synthesis (completed Phases 2, 4, 5B, 5C, 5D only), we address three aims without introducing new analyses or hypotheses: (i) characterize coupling hierarchy across pair-branch combinations, (ii) quantify how strongly those patterns align with environmental structure, and (iii) evaluate whether plant-diversity metrics add reproducible incremental explanatory signal beyond abiotic models. To reduce overinterpretation risk, Mantel and Procrustes are interpreted separately before any integrated ranking summary.

## Methods
### Study design and scope lock
This manuscript draft is derived from completed outputs only, with no rerun analyses, no HPC reruns, and no modification of scientific result files. Analyses are anchored to branch `phase5d-synthesis`, nearest tag `v0.8-phase5c-plant-diversity`, and an 84-sample cohort (`results/phase2_confirmatory_coupling/sample_cohort_used.csv`).

### Pair/branch structure and transformations
Pairwise analyses covered BAC↔ITS, BAC↔EUK, BAC↔AMF, EUK↔ITS, AMF↔ITS, and AMF↔EUK where available by phase integration, with two branches (presence/absence and CLR). Core preprocessing parameters included pseudocount 1e-6 and component cap 10. Thresholds included 0.05 and 0.10 in coupling inference stages.

### Coupling inference inputs
Coupling synthesis used existing outputs from `results/phase5_bac_integration/phase5_bac_coupling_summary.csv` and downstream Phase 5D derived tables. Mantel and Procrustes values were reported independently before averaging into a descriptive composite `coupling_strength = (Mantel + Procrustes similarity)/2`.

### Composite score rationale and constraints
The integrated coupling summary was used only to provide a compact cross-pair ordering for manuscript synthesis. Individual metrics remain the primary evidence because they quantify different properties of cross-domain structure. Accordingly, composite ranking is interpreted as a navigation aid for pattern comparison, not as a replacement inferential statistic and not as evidence that one metric dominates the other.

### Environmental driver layer
Environmental summaries used completed Phase 5B outputs (`phase5b_dbRDA_summary.csv`, `phase5b_predictor_ranking.csv`) with default permutations = 499 and best-model selection between `primary` and `geography_sensitivity` by adjusted R². Primary predictor policy included pH_KCl, N_pct, bio12now.100, alpha, and compl, with geography sensitivity adding lat and lon.

### Plant-diversity layer
Plant-diversity summaries used completed Phase 5C outputs (`phase5c_model_comparison.csv`, `phase5c_hypothesis_summary.csv`) and Phase 5D integrated summaries. Seven primary hypotheses (A–G) were compared against abiotic baseline, with hypothesis-level ranking by mean delta adjusted R².

### Synthesis labeling and interpretive constraints
Phase 5D rule-based labels used fixed thresholds: coupling strength >= 0.50, environmental adjusted R² >= 0.20, plant-diversity delta adjusted R² >= 0.01, and low-plant qualifier at plant delta < 0.005. These labels are descriptive communication aids rather than new inferential tests.

### Reproducibility controls
Completed scripts documented fixed seeds across phases (20260601, 20260602, 20260603), permutations = 499, and bootstrap count = 120 where applicable. Methods parameter traceability is maintained in `results/manuscript_preparation/methods_parameter_inventory.csv`.

## Results
### 1. Coupling hierarchy across pair-branch combinations
Coupling was heterogeneous across pair-branch combinations (Figure 1; Table 1). BAC↔ITS (presence/absence) had the highest composite coupling summary (0.574), followed by EUK↔ITS (presence/absence, 0.538) and EUK↔ITS (CLR, 0.535) (`final_coupling_rankings.csv`).

The strongest Mantel signal occurred for BAC↔ITS (presence/absence; Mantel = 0.584, p = 0.002), while the strongest Procrustes similarity occurred for EUK↔ITS (CLR; 0.683). For BAC↔ITS, Mantel differed between branches (0.584 presence/absence vs 0.358 CLR), whereas Procrustes similarity was comparatively stable (0.564 vs 0.565).

### 2. Interpreting Mantel and Procrustes together
Mantel quantifies rank-based concordance between distance matrices, whereas Procrustes similarity quantifies geometric concordance after optimal superimposition of multivariate configurations. Because these metrics encode different structural properties, pair rankings may diverge without implying analytical failure.

In this dataset, ranking differences are informative: combinations with high matrix-level monotonic correspondence are not always those with the strongest geometric alignment in reduced multivariate space. This divergence indicates that cross-domain organization can be expressed differently depending on whether one emphasizes distance-relationship ordering (Mantel) or shape-level correspondence (Procrustes). We therefore treat both metrics as complementary evidence streams and avoid designating either as universally superior.

### 3. Environmental structuring and pH-centered filtering
Environmental explained variation in final synthesis ranged from 0.188 to 0.278 (Figure 2; Table 3), with the maximum at BAC↔ITS (CLR; adjusted R² = 0.278) and minimum at AMF↔EUK (CLR; adjusted R² = 0.188) (`final_environment_driver_summary.csv`).

Across pair-branch combinations, pH_KCl was the top predictor and its contribution ranged from 0.092 to 0.151. In the broader predictor ranking summary, pH_KCl had the largest mean delta adjusted R² (0.111), exceeding lat (0.013) and lon (0.012) (`phase5b_predictor_ranking.csv`).

Taken together, strong BAC↔ITS coupling and strong pH-centered structure support environmental filtering as a primary competing explanation for apparent cross-domain concordance.

### 4. Plant-diversity effects and AMF-linked contrasts
Plant-diversity effects were positive but modest in aggregate (Figures 3–5; Table 4). Hypothesis B (abiotic_plus_alpha) ranked first (mean delta adjusted R² = 0.013), followed by hypothesis F (0.011) (`phase5c_hypothesis_summary.csv`).

Integrated means followed alpha (0.013) > pool (0.009) > dark (0.003) > compl (-0.004) (`final_plant_diversity_summary.csv`). Pair-specific increments were highest for AMF↔ITS (presence/absence; delta adjusted R² = 0.019), with AMF↔EUK also elevated relative to BAC↔ITS.

These results distinguish two axes: strongest total coupling (BAC↔ITS/EUK↔ITS) versus strongest plant-diversity responsiveness (AMF-linked pairs). The AMF signal is therefore interpreted as context-sensitive responsiveness rather than strongest cross-domain coupling magnitude.

### 5. Integrated synthesis interpretation
Integrated pair labels combined coupling, environmental, and plant-diversity layers (Table 1). BAC↔ITS (presence/absence) was classified as strongly coupled/environment structured, EUK↔ITS (presence/absence) as strongly coupled/environment structured + plant associated, and AMF-linked pairs largely as weakly coupled but plant associated (`final_pair_synthesis.csv`).

Plant-diversity added variation ranged from 0.007 to 0.019 in the synthesis layer, reinforcing that plant effects are secondary to environmental structure in magnitude but not uniformly negligible.

## Discussion
Environmental filtering emerges as the dominant explanatory axis across this synthesis. The same pairings that appear strongly coupled (notably BAC↔ITS) are also strongly environmentally structured, and pH_KCl repeatedly ranks as the leading predictor. This pattern supports a filtering-first interpretation in which shared abiotic constraints generate substantial cross-domain concordance, with direct biotic interaction remaining possible but not established.

Cross-domain organization is therefore best interpreted as layered structure rather than a single-process signal. Strong coupling can coexist with strong environmental forcing, and these observations are not mutually exclusive. From a microbial assembly perspective, this is compatible with mixed deterministic/stochastic dynamics: deterministic environmental filtering defines broad configuration space, while within-space variation may include additional biological contingencies.

Plant context contributes a smaller but structured increment. Alpha diversity consistently outperformed alternative plant metrics in additive models, while dark diversity and completeness showed weaker or negative incremental effects. Because plant metrics can be partially non-independent (e.g., shared dependence on species pool structure), alpha should be viewed as the most robust incremental signal in this dataset rather than an isolated causal mechanism. The consistent alpha pattern may reflect a broad integrative proxy for local plant-community state, whereas dark-diversity-derived metrics may be more sensitive to estimation uncertainty and covariance structure.

AMF-linked contrasts refine this interpretation. AMF pairs were not the strongest in total coupling, yet they showed comparatively larger plant-associated increments. This separation of coupling magnitude and plant responsiveness suggests that AMF-centered assembly signals may be especially informative for plant-context sensitivity even when global cross-domain concordance is lower than BAC↔ITS or EUK↔ITS.

### Limitations
This synthesis has six major limitations. First, compositional amplicon data and sparsity can influence distance-based metrics and effect-size estimates. Second, strong environmental filtering—especially pH-centered structure—can produce cross-domain concordance without requiring direct interaction. Third, Mantel statistics have known sensitivity to distance structure and should be interpreted as association summaries rather than mechanistic tests. Fourth, this is an observational integration and cannot establish causal direction. Fifth, plant-diversity metrics are partially collinear/non-independent, which constrains unique attribution among alpha, pool, dark, and completeness. Sixth, the analysis framework does not include experimental perturbation or temporal intervention, so causal inference remains out of scope.

Overall, this manuscript supports conservative ecological inference: environmental filtering dominates pattern formation, plant-diversity context provides reproducible but modest additional structure, and AMF-linked responsiveness highlights potentially distinct assembly dimensions that warrant targeted follow-up.

## Conclusions
Across completed phase outputs, cross-domain coupling is heterogeneous and most defensibly interpreted through combined metric-specific and environmental-context evidence. BAC↔ITS shows the highest integrated coupling summary but also strong environmental structuring, making filtering-first interpretation essential. Mantel and Procrustes differences are informative about distinct structural aspects of organization rather than contradictions. Plant-diversity effects are modest yet repeatable, with alpha diversity the strongest incremental signal and AMF-linked pairs showing greater plant-context responsiveness than coupling magnitude alone would suggest. These findings motivate cautious, reviewer-resistant interpretation and targeted future testing, not causal claims.

## Data and code availability
All analyses referenced here derive from existing project artifacts in `/srv/hermes_projects/agent_microbial_communities`, including:
- `results/phase4_coupling_inference/*`
- `results/phase5b_environmental_drivers/*`
- `results/phase5c_plant_diversity/*`
- `results/phase5d_synthesis/*`
- `results/manuscript_preparation/*`

No new analyses were run for this manuscript draft. Script provenance is documented in `results/manuscript_preparation/methods_parameter_inventory.csv` and phase-specific analysis scripts under `scripts/analysis/`.

## Author contributions (placeholder)
[Placeholder for CRediT-style contribution statement to be completed with coauthors.]

## Acknowledgements (placeholder)
[Placeholder for funding, institutional support, and contributor acknowledgements.]

## References
[R1] Zhou Y, Sun B, Xie B, Feng K, Zhang Z. 2021. Warming reshaped the microbial hierarchical interactions. (Semantic Scholar record: d1eb20c8a4f7a6487b380b9ee28363cfe2ff1ead).

[R2] Du S, Li X-Q, Hao X, Hu H, Feng J. 2022. Stronger responses of soil protistan communities to legacy mercury pollution than bacterial and fungal communities in agricultural systems. (Semantic Scholar record: 8cc605f34ca4893c115973d77f625074977483a4).

[R3] Fierer N, Jackson RB. 2006. The diversity and biogeography of soil bacterial communities. DOI: 10.1073/pnas.0507535103.

[R4] Lauber CL, Hamady M, Knight R, Fierer N. 2009. Pyrosequencing-Based Assessment of Soil pH as a Predictor of Soil Bacterial Community Structure at the Continental Scale. DOI: 10.1128/AEM.00335-09.

[R5] Rousk J, Bååth E, Brookes PC, Lauber CL, Lozupone C, Caporaso JG, Knight R, Fierer N. 2010. Soil bacterial and fungal communities across a pH gradient in an arable soil. DOI: 10.1111/j.1462-2920.2010.02234.x.

[R6] Davison J, Moora M, Öpik M, Adholeya A, Ainsaar L, et al. 2015. Global assessment of arbuscular mycorrhizal fungus diversity reveals very low endemism. DOI: 10.1126/science.aab1161.

[R7] van der Heijden MGA, Klironomos JN, Ursic M, Moutoglis P, Streitwolf-Engel R, et al. 1998. Mycorrhizal fungal diversity determines plant biodiversity, ecosystem variability and productivity. DOI: 10.1038/23932.

[R8] Stegen JC, Lin X, Fredrickson JK, Chen X, Kennedy DW, et al. 2013. Quantifying community assembly processes and identifying features that impose them. DOI: 10.1038/ismej.2013.93.

[R9] Pärtel M, Szava-Kovats R, Zobel M. 2013. Community Completeness: Linking Local and Dark Diversity within the Species Pool Concept. DOI: 10.1007/s12224-013-9169-x.

[R10] Dohlman AB, Shen X. 2019. Mapping the microbial interactome: Statistical and experimental approaches for microbiome network inference. DOI: 10.1177/1535370219836771.

[R11] Carmona CP, Pärtel M. 2020. Estimating probabilistic site-specific species pools and dark diversity from co-occurrence data. DOI: 10.1111/geb.13203.

[R12] Pärtel M, Tamme R, Carmona CP, Riibak K, Moora M, et al. 2025. Global impoverishment of natural vegetation revealed by dark diversity. DOI: 10.1038/s41586-025-08814-5.
