# Title

Cross-domain soil microbial coupling is jointly structured by abiotic gradients and plant-diversity context

## Abstract
Understanding whether cross-domain microbial coupling reflects shared environmental filtering, plant-context dependence, or both remains a central challenge in soil ecology. Using only completed phase outputs from a fixed 84-sample cohort, we synthesized pairwise coupling (Mantel and Procrustes), environmental driver models, and plant-diversity hypothesis comparisons across BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK combinations. BAC↔ITS (presence/absence) showed the highest composite coupling strength (0.574), while EUK↔ITS combinations ranked second and third (0.538 and 0.535). Mantel and Procrustes highlighted partially different pair orderings, motivating metric-specific interpretation before synthesis. Environmental structure was substantial across pair-branch combinations (adjusted R² 0.188–0.278), with pH_KCl consistently the top predictor and the largest mean predictor delta adjusted R² (0.111). Plant-diversity effects were modest in magnitude but reproducible: hypothesis B (abiotic_plus_alpha) ranked highest (mean delta adjusted R² = 0.013), and alpha diversity showed the largest mean plant-associated increment (0.013) relative to pool (0.009), dark (0.003), and completeness (-0.004). AMF-linked pairs had lower overall coupling than BAC↔ITS/EUK↔ITS but stronger plant-associated increments (up to 0.019), indicating domain-specific ecological patterning rather than absence of signal. We interpret BAC↔ITS as strongly coupled and strongly environment-structured, with direct interaction and shared filtering remaining alternative explanations. Overall, the synthesis supports cautious, multi-layer interpretation: environmental filtering appears dominant, while plant-diversity context provides secondary but non-negligible explanatory structure. [R1, R2, R3, R4, R5, R6, R7, R8]

## Introduction
Cross-domain organization of soil microbial communities is increasingly recognized as a systems-level property, yet the relative roles of abiotic filtering and plant-context modulation remain unresolved [R1, R2, R8]. Prior work has shown that bacteria, fungi, and protists can exhibit coordinated network-level responses under shared environmental pressures, but correlation-based coupling does not uniquely identify mechanism [R1, R8, R10].

Environmental filtering, particularly soil pH, is among the most reproducible large-scale structuring forces reported for soil microbiomes [R3, R4, R5]. In parallel, arbuscular mycorrhizal fungi (AMF) are ecologically positioned at the plant–soil interface and may encode plant-associated assembly signatures that differ from BAC-inclusive pairings [R6, R7].

Plant diversity, dark diversity, and community completeness concepts provide an additional framework for evaluating whether biotic context contributes explanatory signal beyond abiotic gradients [R11, R12]. However, these effect layers are often modest in size and can be confounded by metric non-independence, requiring careful interpretation [R9, R10].

Here, we present an integrated manuscript synthesis built from completed project phases only (Phase 2, 4, 5B, 5C, 5D). We ask three constrained questions: (i) how coupling strength ranks across pair-branch combinations, (ii) how much of that structure aligns with environmental predictors, and (iii) whether plant-diversity metrics add incremental explanatory variation beyond abiotic baselines. We explicitly separate Mantel and Procrustes interpretation before reporting the composite coupling summary.

## Methods
### Study design and scope lock
This manuscript draft is derived from completed outputs only, with no rerun analyses, no HPC reruns, and no modification of scientific result files. Analyses are anchored to branch `phase5d-synthesis`, nearest tag `v0.8-phase5c-plant-diversity`, and an 84-sample cohort (`results/phase2_confirmatory_coupling/sample_cohort_used.csv`).

### Pair/branch structure and transformations
Pairwise analyses covered BAC↔ITS, BAC↔EUK, BAC↔AMF, EUK↔ITS, AMF↔ITS, and AMF↔EUK where available by phase integration, with two branches (presence/absence and CLR). Core preprocessing parameters included pseudocount 1e-6 and component cap 10. Thresholds included 0.05 and 0.10 in coupling inference stages.

### Coupling inference inputs
Coupling synthesis used existing outputs from `results/phase5_bac_integration/phase5_bac_coupling_summary.csv` and downstream Phase 5D derived tables. Mantel and Procrustes values were reported independently before averaging into the descriptive composite `coupling_strength = (Mantel + Procrustes similarity)/2`.

### Environmental driver layer
Environmental summaries used completed Phase 5B outputs (`phase5b_dbRDA_summary.csv`, `phase5b_predictor_ranking.csv`) with default permutations = 499 and best-model selection between `primary` and `geography_sensitivity` by adjusted R². Primary predictor policy included pH_KCl, N_pct, bio12now.100, alpha, and compl, with geography sensitivity adding lat and lon.

### Plant-diversity layer
Plant-diversity summaries used completed Phase 5C outputs (`phase5c_model_comparison.csv`, `phase5c_hypothesis_summary.csv`) and Phase 5D integrated summaries. Seven primary hypotheses (A–G) were compared against abiotic baseline, with hypothesis-level ranking by mean delta adjusted R².

### Synthesis labeling and interpretive constraints
Phase 5D rule-based labels used fixed thresholds: coupling strength >= 0.50, environmental adjusted R² >= 0.20, plant-diversity delta adjusted R² >= 0.01, and low-plant qualifier at plant delta < 0.005. These labels are descriptive communication aids rather than new inferential tests.

### Reproducibility controls
Completed scripts documented fixed seeds across phases (20260601, 20260602, 20260603), permutations = 499, and bootstrap count = 120 where applicable. Methods parameter traceability is maintained in `results/manuscript_preparation/methods_parameter_inventory.csv`.

## Results
### 1. Coupling hierarchy and metric-specific contrasts
Coupling was heterogeneous across pair-branch combinations (Figure 1; Table 1). BAC↔ITS (presence/absence) had the highest composite coupling strength (0.574), followed by EUK↔ITS (presence/absence, 0.538) and EUK↔ITS (CLR, 0.535) (`final_coupling_rankings.csv`).

Mantel and Procrustes were not fully concordant in ranking. The strongest Mantel value occurred for BAC↔ITS (presence/absence; Mantel = 0.584, p = 0.002), whereas the strongest Procrustes similarity occurred for EUK↔ITS (CLR; 0.683). For BAC↔ITS, Mantel differed between branches (0.584 presence/absence vs 0.358 CLR), while Procrustes similarity was comparatively stable (0.564 vs 0.565).

These metric-specific differences support reporting Mantel and Procrustes separately prior to synthesis and caution against over-interpreting the composite score as a standalone inferential metric.

### 2. Environmental structuring and pH-centered filtering
Environmental explained variation in final synthesis ranged from 0.188 to 0.278 (Figure 2; Table 3), with the maximum at BAC↔ITS (CLR; adjusted R² = 0.278) and minimum at AMF↔EUK (CLR; adjusted R² = 0.188) (`final_environment_driver_summary.csv`).

Across pair-branch combinations, pH_KCl was the top predictor and its contribution ranged from 0.092 to 0.151. In the broader predictor ranking summary, pH_KCl had the largest mean delta adjusted R² (0.111), exceeding lat (0.013) and lon (0.012) (`phase5b_predictor_ranking.csv`).

These patterns are consistent with strong environmental filtering, especially for BAC↔ITS, and support interpreting high coupling as compatible with shared abiotic structure rather than direct interaction alone.

### 3. Plant-diversity effects and AMF-linked contrasts
Plant-diversity effects were positive but modest in aggregate (Figures 3–5; Table 4). Hypothesis B (abiotic_plus_alpha) ranked first (mean delta adjusted R² = 0.013), followed by hypothesis F (0.011) (`phase5c_hypothesis_summary.csv`).

In integrated summaries, mean effect ordering was alpha (0.013) > pool (0.009) > dark (0.003) > compl (-0.004) (`final_plant_diversity_summary.csv`). Pair-specific increments were highest for AMF↔ITS (presence/absence; delta adjusted R² = 0.019), with AMF↔EUK also showing elevated plant-associated increments relative to BAC↔ITS.

Thus, AMF-linked pairs were weaker in total coupling than BAC↔ITS/EUK↔ITS but stronger in plant-associated added variation, indicating potentially distinct ecological structuring dimensions.

### 4. Integrated synthesis interpretation
Integrated pair labels combined coupling, environmental, and plant-diversity layers (Table 1). BAC↔ITS (presence/absence) was classified as strongly coupled/environment structured, EUK↔ITS (presence/absence) as strongly coupled/environment structured + plant associated, and AMF-linked pairs largely as weakly coupled but plant associated (`final_pair_synthesis.csv`).

Plant-diversity added variation ranged from 0.007 to 0.019 in the synthesis layer, reinforcing that plant effects are secondary to environmental structure in magnitude but not uniformly negligible.

## Discussion
This synthesis supports a cautious multi-process interpretation. First, BAC↔ITS is the strongest coupled combination overall (composite 0.574), but it is also among the most environment-structured combinations (adjusted R² up to 0.278 with pH_KCl as dominant predictor), making shared environmental filtering a parsimonious explanation that must be considered alongside direct biotic coupling.

Second, Mantel and Procrustes do not fully tell the same story for all pair-branch combinations. The strongest Mantel and strongest Procrustes rankings occur in different combinations, indicating that rank conclusions depend on whether one emphasizes distance-matrix correlation or geometric concordance. Composite coupling is therefore best treated as a summary heuristic, not a replacement for metric-specific interpretation.

Third, plant-diversity signals are reproducible but modest. Alpha-inclusive models are consistently top-ranked (mean delta adjusted R² = 0.013), yet effect sizes remain small relative to total unexplained variance. We interpret these increments as biologically relevant context signals rather than dominant drivers. AMF-linked pairs appear particularly informative in this respect: they show lower coupling magnitudes but larger plant-associated increments (up to 0.019), suggesting ecological specificity rather than simple weak-signal noise.

Several limitations constrain inference. The framework is correlative and synthesis-based, with no new manipulative confirmation. Compositionality and sparsity in amplicon-derived community matrices can affect distance-based metrics and downstream coupling interpretation. Environmental and plant predictors may also share covariance structure, and thus individual predictor attribution should be interpreted conservatively. Finally, rule-based synthesis labels communicate patterns but do not constitute additional hypothesis testing.

Overall, environmental filtering appears dominant across domains, while plant-diversity context provides a smaller but structured explanatory layer, especially in AMF-linked combinations.

## Conclusions
Across completed phase outputs, cross-domain coupling in this system is heterogeneous and best interpreted through layered evidence rather than single-metric rankings. BAC↔ITS shows strongest overall coupling, but strong environmental structure—particularly pH_KCl dominance—supports a filtering-forward interpretation. Plant-diversity effects are modest in magnitude yet reproducible, with alpha diversity as the strongest plant-associated signal and AMF-linked pairs showing comparatively larger plant-associated increments than BAC↔ITS. These findings support cautious ecological interpretation and motivate targeted follow-up testing rather than strong causal claims.

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
