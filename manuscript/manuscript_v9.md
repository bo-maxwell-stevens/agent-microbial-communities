# Title
## Five title options
1. Environmental filtering dominates cross-domain soil microbiome coupling, with secondary AMF-linked plant-context effects
2. Do shared abiotic gradients or plant context better explain cross-domain soil microbiome coupling?
3. Layered ecological organization of BAC, ITS, EUK, and AMF coupling across a globally distributed 84-sample cohort
4. From concordance to mechanism constraints: integrated coupling, environmental, and plant-diversity synthesis in soil microbiomes
5. Cross-domain microbial coupling is strong, pH-structured, and differentially sensitive to plant diversity

## Abstract
We synthesized committed outputs for cross-domain coupling among BAC, ITS, EUK, and AMF using the final matched cohort (n=84), and integrated matrix-concordance (Mantel), geometric-alignment (Procrustes), environmental constrained-ordination (dbRDA), and plant-diversity model-comparison layers. Coupling was strongest for BAC↔ITS in presence/absence space, while AMF-linked pairs showed comparatively larger plant-context sensitivity than expected from their global coupling rank. Environmental structure was substantial across models (adjusted R2 values generally around 0.18 to 0.28; p=0.002 in all dbRDA summaries), and pH_KCl repeatedly ranked as the largest predictor-level contribution. Plant-diversity increments over abiotic baselines were positive but smaller, with alpha-containing hypotheses producing the highest mean delta adjusted R2. Together, the evidence supports a layered interpretation: strong cross-domain concordance, major environmental organization, and secondary plant-context modulation.

## Introduction
Soil microbial communities are assembled through interacting deterministic and stochastic processes that operate simultaneously across bacteria, fungi, and microbial eukaryotes. Deterministic processes include environmental filtering and biotic interactions, whereas stochastic processes include dispersal limitation, ecological drift, and historical contingency. The relative importance of these mechanisms varies among microbial groups, across spatial scales, and along environmental gradients. Consequently, concordant patterns among microbial domains can arise because different groups respond similarly to environmental conditions, because they interact directly through trophic, competitive, or metabolic relationships, or because both mechanisms operate together. Cross-domain concordance is therefore informative about ecological organization, but it does not by itself identify the mechanisms responsible for observed patterns.

Bacteria and fungi are expected to exhibit strong cross-domain coupling because they jointly mediate decomposition, nutrient turnover, and rhizosphere processes. Root exudates influence bacterial community composition through substrate-specific selection, while fungal communities contribute to resource acquisition, organic matter transformation, and habitat structuring. These shared ecological functions can generate coordinated turnover among bacterial and fungal communities across environmental gradients. However, bacterial-fungal associations may also reflect common responses to soil conditions rather than direct interactions, emphasizing the need to distinguish ecological concordance from mechanistic dependence.

Arbuscular mycorrhizal fungi (AMF) introduce an additional ecological dimension because they directly connect plant communities with belowground microbial organization. AMF depend on host-derived carbon and influence nutrient acquisition through extensive hyphal networks that extend beyond the root zone. Variation in host identity, plant functional traits, and nutrient availability can therefore alter AMF-associated microbial assemblages in ways that differ from patterns observed for free-living soil microorganisms. Experimental studies have shown that AM fungi can recruit distinct bacterial, fungal, and protistan communities and modify network structure within the hyphosphere. These observations suggest that AMF-linked microbial relationships may be particularly sensitive to plant-community context.

Although individual microbial groups have been extensively studied, comparatively few investigations have integrated bacteria, fungi, microbial eukaryotes, and AMF within a common analytical framework. Most studies focus on a single domain or a limited set of pairwise interactions, making it difficult to evaluate whether environmental filtering and plant-community context influence different microbial domains in similar or contrasting ways. A broader cross-domain perspective is needed to determine whether observed coupling reflects shared environmental organization, plant-mediated effects, or combinations of both processes.

Environmental filtering is likely to explain an important proportion of cross-domain concordance. Among soil variables, pH is consistently identified as one of the strongest predictors of bacterial community composition and can influence the balance between deterministic and stochastic assembly processes. Soil pH also affects nutrient availability, enzyme activity, and microbial physiology, creating constraints that extend across multiple microbial groups. Other environmental factors, including nutrient availability and climate, can further structure microbial communities and contribute to coordinated turnover among domains. As a result, strong cross-domain coupling may often reflect shared environmental responses that are subsequently modified by biological interactions.

Plant-community context provides a complementary perspective on microbial assembly. Traditional diversity metrics focus on realized richness, but dark-diversity approaches extend this framework by considering taxa that are absent locally despite being members of the regional species pool. Community completeness quantifies the relationship between observed diversity and the diversity that could potentially occur at a site. Together, these metrics offer a means of evaluating whether microbial community organization is associated primarily with realized plant diversity or with broader constraints related to species pools and community assembly processes. However, dark-diversity and completeness estimates depend on species-pool definition and should be interpreted cautiously.

In this study, we evaluated soil microbial coupling across bacterial, fungal ITS, microbial eukaryote, and AMF communities using a hierarchical analytical framework. First, we quantified cross-domain coupling strength using complementary measures of community concordance. Second, we evaluated the extent to which environmental variables explained observed coupling patterns. Third, we tested whether plant-diversity metrics provided additional explanatory power beyond environmental structure alone. We hypothesized that (1) bacterial-fungal communities would exhibit the strongest overall coupling, reflecting their shared ecological functions and responses to rhizosphere processes; (2) environmental filtering, particularly soil pH, would explain a substantial fraction of cross-domain concordance; and (3) AMF-linked associations would show greater sensitivity to plant-community context than would be predicted from coupling strength alone. By integrating coupling analyses, environmental drivers, and plant-diversity effects within a single framework, this study aims to clarify how multiple ecological layers contribute to the organization of soil microbial communities.

## Methods
### 1. Study system and DarkDivNet dataset
This manuscript revision is synthesis-only and uses completed project artifacts without rerunning analyses. The analytical context is the DarkDivNet-derived soil microbiome dataset integrated across BAC, ITS, EUK, and AMF domains. Cohort context, geographic distribution, and environmental space are summarized in Figure 1, which anchors all downstream coupling and driver analyses.

### 2. Cohort matching and sample selection (n=84)
All analyses used the final matched overlap cohort of 84 samples shared across the required microbial domains for each phase-specific comparison. Cohort membership was inherited from committed overlap/filtering outputs and was held fixed across coupling (Phase 2 and Phase 5A), environmental-driver (Phase 5B), plant-diversity (Phase 5C), and integrated synthesis (Phase 5D) analyses to preserve comparability.

### 3. Microbial domains and pair definitions
Four domains were included in the integrated manuscript framework: BAC, ITS, EUK, and AMF. Phase 2 pairwise coupling focused on EUK↔ITS, AMF↔ITS, and AMF↔EUK combinations. Phase 5A bacterial integration added BAC-inclusive coupling contrasts, with BAC↔ITS carried forward as the strongest integrated coupling configuration in final synthesis summaries. Pairwise comparisons were evaluated within explicitly tracked branch definitions (presence/absence and CLR) and retained as pair×branch units through Phase 5D integration.

### 4. Presence/absence and CLR transformations
Two representation branches were used throughout coupling workflows. In the presence/absence branch, community matrices were binarized and analyzed with Jaccard distance and PCoA ordination in the coupling workflow context. In the CLR branch, count matrices were transformed using a pseudocount of 1e-6 and centered log-ratio transformation, followed by Euclidean distance and PCA-based ordination context. Prevalence thresholds of 0.05 and 0.10 were retained exactly as in committed outputs.

### 5. Phase 2 coupling analyses (Mantel + Procrustes)
Phase 2 coupling analyses used complementary matrix concordance and geometric alignment metrics. Mantel analyses were summarized as Spearman matrix correlations with paired permutation support from committed outputs. Procrustes analyses were reported as fit/similarity summaries from the same pair×branch comparisons. For manuscript interpretation, coupling comparisons were treated as relative ranking evidence across pair×branch combinations rather than as stand-alone mechanistic tests.

### 6. Phase 5A bacterial integration
Phase 5A integrated BAC into the cross-domain coupling framework by combining BAC-inclusive coupling summaries with existing AMF/EUK/ITS results in a common ranking structure. The primary Phase 5A output table (`results/phase5_bac_integration/phase5_bac_coupling_summary.csv`) provided Mantel means, conservative p-values, confidence interval bounds, and Procrustes similarity summaries used downstream in Phase 5D. No BAC integration statistics were recomputed for this manuscript revision.

### 7. Phase 5B environmental driver analyses
Environmental-driver synthesis used committed dbRDA outputs from `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv` and predictor-level rankings from `results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv`. Primary predictor sets included pH_KCl, N_pct, and bio12now.100 with plant/diversity terms as specified by the model family; geography-sensitivity models additionally included lat and lon. Reported model statistics followed committed outputs (R2, adjusted R2, pseudo-F, and permutation p-values with 999 permutations), and manuscript interpretation emphasized adjusted R2 ranges and predictor-level delta adjusted R2 rankings.

### 8. Phase 5C plant diversity hypothesis framework
Plant-diversity effects were evaluated using hypothesis models A-G from committed Phase 5C comparisons (`results/phase5c_plant_diversity/phase5c_model_comparison.csv`), with abiotic-base model A as the reference for delta adjusted R2 comparisons. Hypotheses were interpreted at two levels: (i) global hypothesis means across pair×branch combinations and (ii) best-hypothesis rankings per pair×branch×scope. Effects for alpha, dark, pool, and completeness were interpreted from committed model summaries without changing model structure or refitting.

### 9. Phase 5D synthesis workflow
Integrated synthesis followed `scripts/analysis/phase5d_synthesis.py` and merged completed outputs from Phase 5A, 5B, and 5C into four derived tables: `final_coupling_rankings.csv`, `final_environment_driver_summary.csv`, `final_plant_diversity_summary.csv`, and `final_pair_synthesis.csv` under `results/phase5d_synthesis/`. In this workflow, coupling strength was reported as the mean of Mantel and Procrustes similarity values, environmental summaries selected best adjusted R2 between primary and geography-sensitivity scopes, and plant-diversity summaries reported best non-base delta adjusted R2 signals.

### 10. Statistical testing, permutations, and reproducibility
All inferential statistics reported in this manuscript derive from already completed analyses and their committed permutation outputs; no new inferential runs were executed. Permutation-based p-values reported in the environmental and plant-diversity model summaries use 999 permutations. Deterministic controls and parameterization followed committed workflows (including fixed branch manifests, prevalence thresholds, and documented seeds in phase scripts), and manuscript packaging was performed in the project Python environment (`.venv/bin/python`; Python 3.12.3 with numpy 2.4.5, pandas 3.0.3, scipy 1.17.1, scikit-learn 1.8.0, matplotlib 3.10.9, seaborn 0.13.2, statsmodels 0.14.6).

## Results
Figure 1 (global cohort context) anchors all downstream analyses and confirms the final matched cohort used in this manuscript (n=84 across required domain overlaps).

### 3.1 Cross-domain coupling hierarchy
Cross-domain coupling was non-uniform across pair×branch combinations, and the integrated ranking identified BAC↔ITS (presence/absence) as the strongest coupling configuration (coupling strength 0.574). The next highest combinations were EUK↔ITS (presence/absence, 0.538) and EUK↔ITS (CLR, 0.535). The strongest Mantel association in integrated summaries was BAC↔ITS (presence/absence; Mantel 0.584, p=0.002), while the strongest Procrustes similarity was EUK↔ITS (CLR; 0.683). Together, these results show that BAC↔ITS occupies the top coupling rank even though Mantel and Procrustes emphasize partially different pair×branch extremes.

### 3.2 Environmental drivers of coupling
Environmental structure was substantial across pair×branch summaries. Adjusted R2 values spanned 0.188 to 0.278 across completed dbRDA summaries, with the highest adjusted R2 observed for BAC↔ITS (CLR; 0.278) and the lowest for AMF↔EUK (CLR; 0.188). Predictor-level rankings consistently identified pH-linked structure as dominant: mean predictor delta adjusted R2 was highest for pH_KCl (0.111), and pH contribution values ranged from 0.092 to 0.151 across pair×branch combinations. These patterns indicate that strong coupling does not occur in an abiotic vacuum; instead, the coupling hierarchy is embedded within a pH-centered environmental axis.

### 3.3 Plant diversity hypothesis comparison
Plant-diversity increments over abiotic baselines were positive but smaller than the environmental layer and followed a consistent ranking pattern across model summaries. Mean delta adjusted R2 values followed alpha (0.013) > pool (0.009) > dark (0.003) > completeness (-0.004). Hypothesis-level means also showed that abiotic_plus_alpha (B; mean delta adjusted R2=0.013) outperformed abiotic_plus_alpha_dark (F; 0.011), indicating alpha+dark did not improve over alpha alone. Similarly, abiotic_plus_pool (D; 0.009) exceeded abiotic_plus_pool_compl (G; 0.008), showing pool+completeness did not improve over pool alone. Across pair×branch rankings, the largest plant-added variation was 0.019 for AMF↔ITS (presence/absence).

### 3.4 AMF-centered ecological responses
AMF-centered pairs ranked below BAC↔ITS and top EUK↔ITS configurations in integrated coupling strength, but they retained comparatively elevated plant-associated increments. In practical terms, AMF↔ITS and AMF↔EUK combinations showed lower global coupling rank while repeatedly expressing positive plant-diversity added variation, including the top pair-specific plant increment (0.019 in AMF↔ITS presence/absence). This dissociation between coupling rank and plant responsiveness supports an AMF-linked ecological-response pattern that is not captured by coupling magnitude alone.

### 3.5 Integrated synthesis
Phase 5D integration across coupling, environmental, and plant-diversity layers converged on a layered result structure: (i) strongest cross-domain coupling in BAC↔ITS and EUK↔ITS combinations, (ii) substantial and recurrent pH-dominated environmental structuring, and (iii) smaller but consistent plant-diversity increments with alpha-centered models ranking highest. Integrated hierarchy bounds were coherent across layers: coupling strengths ranged from 0.400 to 0.574, environmental adjusted R2 ranged from 0.188 to 0.278, and plant-diversity added variation ranged from 0.007 to 0.019 in the final pair synthesis summaries.

## Discussion
Across Figures 1 to 5, the most defensible interpretation is layered: (i) strong cross-domain concordance, (ii) substantial environmental structuring with strong pH influence, and (iii) additional but smaller plant-diversity increments, especially for alpha-containing hypotheses.

## Conclusions
Using only committed outputs and reviewer-directed restructuring, v8 shows that cross-domain coupling is strong but heterogeneously structured; environmental gradients explain a substantial share of variation; and plant-diversity effects are positive but generally smaller than environmental effects, with alpha-associated increments ranking highest on average.

## Figure legends
Figure 1. Global cohort and environmental context of the cross-domain microbiome analysis. Global distribution of the final matched cohort (n=84), environmental gradient space (pH_KCl, bio12now.100), plant-diversity distributions, and pair-set analysis design.

Figure 2. Cross-domain coupling hierarchy. Left: rank ordering of pair-representation combinations by composite coupling strength. Right: Mantel vs Procrustes comparison for each combination.

Figure 3. Environmental driver analysis. Left: dbRDA adjusted R2 across pair-representation combinations. Right: predictor-level mean delta adjusted R2 rankings.

Figure 4. Plant-diversity hypothesis comparison (A-G). Left: mean delta adjusted R2 versus abiotic baseline. Right: pair-level response profiles across hypotheses.

Figure 5. Integrated ecological synthesis network. Network-style integration of coupling (C), environmental structure (E), and plant-diversity increments across domain pairs.

## References
- Legendre, P., and Legendre, L. (2012). Numerical Ecology.
- Peres-Neto, P. R., et al. (2006). Variation partitioning of species data matrices.
- McArdle, B. H., and Anderson, M. J. (2001). Fitting multivariate models to community data.
- Python Software Foundation. Python 3.12.3. https://www.python.org/
- Harris, C. R., et al. (2020). Array programming with NumPy. Nature.
- McKinney, W. (2010). Data structures for statistical computing in Python.
- Virtanen, P., et al. (2020). SciPy 1.0. Nature Methods.
- Pedregosa, F., et al. (2011). Scikit-learn. Journal of Machine Learning Research.
- Hunter, J. D. (2007). Matplotlib. Computing in Science and Engineering.
- Waskom, M. (2021). seaborn: statistical data visualization. Journal of Open Source Software.
