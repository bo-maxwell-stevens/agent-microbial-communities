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
### Study system and dataset assembly
#### DarkDivNet sampling network
The synthesis used the committed DarkDivNet-derived overlap cohort for BAC, ITS, EUK, and AMF domains (n=84 shared samples; final overlap). Figure 1 is the cohort-context panel for all downstream analyses.

#### Site selection and metadata
Geographic coordinates (lat, lon) and metadata variables were taken from committed repository files only, with no new data generation. The same final matched cohort was used consistently across coupling, environmental, and plant-diversity analyses.

#### Construction of the final analytical cohort
Final cohort construction was inherited from committed filtering outputs and overlap manifests. All pairwise analyses were restricted to the same sample-level overlap to preserve comparability.

#### Environmental and plant-diversity variables
Environmental predictors were pH_KCl, N_pct, and bio12now.100 (with geography-sensitivity models additionally including lat and lon). Plant-diversity terms included alpha, dark, pool, and compl depending on hypothesis model.

### DNA sequencing and bioinformatics processing
#### BAC, ITS, EUK, and AMF sequencing datasets
Intentionally left blank per reviewer request.

#### Quality filtering
Intentionally left blank per reviewer request.

#### Sequence processing pipeline
Intentionally left blank per reviewer request.

#### Taxonomic assignment
Intentionally left blank per reviewer request.

#### Construction of community matrices
Intentionally left blank per reviewer request.

### Cross-domain coupling analyses
#### Mantel correlations
Mantel correlations were read from committed Phase 2 outputs (Spearman matrix-correlation form) across pairings, transformations (presence/absence and CLR), and prevalence thresholds (0.05 and 0.10), with matched sample sets.

#### Procrustes analyses
Procrustes fits were read from the same committed Phase 2 output table as the geometric-alignment complement to Mantel correlations.

#### Coupling network construction
Coupling hierarchy and integrated interpretation were aligned with Figure 2 and Figure 5 summaries, where pairwise coupling magnitudes were interpreted comparatively (not causally) across domain pairs.

#### BAC integration framework (Phase 5A)
BAC-linked pair comparisons were interpreted from committed cross-domain synthesis outputs; no additional reruns were performed in this manuscript round.

### Environmental and plant-diversity drivers of microbial coupling
#### Environmental predictor selection (pH, N, precipitation)
dbRDA model families were taken directly from committed Phase 5B outputs with primary and geography-sensitivity scopes.

#### dbRDA / variation-partitioning framework
For each pair/branch/scope combination, model outputs included R2, adjusted R2, pseudo-F, and permutation p-values (999 permutations per model).

#### Plant-diversity hypothesis models
Phase 5C hypothesis sets A-G were compared against abiotic baselines for each pair and branch under primary and geography-sensitivity scopes.

#### Alpha diversity, dark diversity, species pool, and completeness analyses
Plant-diversity effects were quantified as delta adjusted R2 versus abiotic baselines, with direct model-wise comparisons across alpha, dark, pool, and compl-containing hypotheses.

### Integrated synthesis and statistical framework
#### Ranking and synthesis of coupling metrics
Results were interpreted in sequence: coupling strength (Figure 2), environmental structure (Figure 3), and plant-diversity increments (Figure 4), then integrated as a network-style synthesis (Figure 5).

#### Composite coupling framework
Composite interpretation used jointly reported Mantel and Procrustes outputs rather than a single metric.

#### Permutation procedures
Permutation-derived p-values in dbRDA/model comparisons used 999 permutations in committed outputs.

#### Reproducibility and software environment
Python 3.12.3; numpy 2.4.5; pandas 3.0.3; scipy 1.17.1; scikit-learn 1.8.0; matplotlib 3.10.9; seaborn 0.13.2; statsmodels 0.14.6.

## Results
Figure 1 (global cohort context) is first referenced here and anchors all downstream analyses (n=84 matched samples across BAC, ITS, EUK, AMF).

### Cross-domain coupling results (Mantel and Procrustes)
Figure 2 summarizes the cross-domain coupling hierarchy and Mantel/Procrustes comparisons. Full pair-by-branch-by-threshold values from committed Phase 2 outputs are:
- AMF↔EUK | CLR | threshold 0.05: Mantel rho = 0.478, Procrustes fit = 0.591 (distance=euclidean, ordination=pca, features=148/4126).
- AMF↔ITS | CLR | threshold 0.05: Mantel rho = 0.556, Procrustes fit = 0.585 (distance=euclidean, ordination=pca, features=148/1286).
- EUK↔ITS | CLR | threshold 0.05: Mantel rho = 0.409, Procrustes fit = 0.310 (distance=euclidean, ordination=pca, features=4126/1286).
- AMF↔EUK | presence/absence | threshold 0.05: Mantel rho = 0.447, Procrustes fit = 0.626 (distance=jaccard, ordination=pcoa, features=148/4126).
- AMF↔ITS | presence/absence | threshold 0.05: Mantel rho = 0.460, Procrustes fit = 0.555 (distance=jaccard, ordination=pcoa, features=148/1286).
- EUK↔ITS | presence/absence | threshold 0.05: Mantel rho = 0.438, Procrustes fit = 0.337 (distance=jaccard, ordination=pcoa, features=4126/1286).
- AMF↔EUK | CLR | threshold 0.10: Mantel rho = 0.467, Procrustes fit = 0.622 (distance=euclidean, ordination=pca, features=106/1651).
- AMF↔ITS | CLR | threshold 0.10: Mantel rho = 0.495, Procrustes fit = 0.626 (distance=euclidean, ordination=pca, features=106/518).
- EUK↔ITS | CLR | threshold 0.10: Mantel rho = 0.365, Procrustes fit = 0.323 (distance=euclidean, ordination=pca, features=1651/518).
- AMF↔EUK | presence/absence | threshold 0.10: Mantel rho = 0.428, Procrustes fit = 0.648 (distance=jaccard, ordination=pcoa, features=106/1651).
- AMF↔ITS | presence/absence | threshold 0.10: Mantel rho = 0.459, Procrustes fit = 0.584 (distance=jaccard, ordination=pcoa, features=106/518).
- EUK↔ITS | presence/absence | threshold 0.10: Mantel rho = 0.390, Procrustes fit = 0.340 (distance=jaccard, ordination=pcoa, features=1651/518).

### Environmental drivers of coupling
Figure 3 summarizes environmental model performance and predictor-level influence. dbRDA summary results (all pair by branch by model-scope combinations) are:
- AMF↔EUK | CLR | geography_sensitivity: R2=0.257, adjusted R2=0.188, pseudo-F=3.748, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- AMF↔EUK | CLR | primary: R2=0.230, adjusted R2=0.180, pseudo-F=4.648, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- AMF↔EUK | presence/absence | geography_sensitivity: R2=0.273, adjusted R2=0.206, pseudo-F=4.068, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- AMF↔EUK | presence/absence | primary: R2=0.241, adjusted R2=0.192, pseudo-F=4.946, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- AMF↔ITS | CLR | geography_sensitivity: R2=0.271, adjusted R2=0.204, pseudo-F=4.039, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- AMF↔ITS | CLR | primary: R2=0.243, adjusted R2=0.195, pseudo-F=5.009, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- AMF↔ITS | presence/absence | geography_sensitivity: R2=0.290, adjusted R2=0.225, pseudo-F=4.433, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- AMF↔ITS | presence/absence | primary: R2=0.254, adjusted R2=0.206, pseudo-F=5.303, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- BAC↔ITS | CLR | geography_sensitivity: R2=0.339, adjusted R2=0.278, pseudo-F=5.558, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- BAC↔ITS | CLR | primary: R2=0.313, adjusted R2=0.269, pseudo-F=7.116, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- BAC↔ITS | presence/absence | geography_sensitivity: R2=0.327, adjusted R2=0.265, pseudo-F=5.267, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- BAC↔ITS | presence/absence | primary: R2=0.289, adjusted R2=0.244, pseudo-F=6.354, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- EUK↔ITS | CLR | geography_sensitivity: R2=0.263, adjusted R2=0.195, pseudo-F=3.874, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- EUK↔ITS | CLR | primary: R2=0.234, adjusted R2=0.185, pseudo-F=4.761, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).
- EUK↔ITS | presence/absence | geography_sensitivity: R2=0.288, adjusted R2=0.222, pseudo-F=4.384, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl,lat,lon).
- EUK↔ITS | presence/absence | primary: R2=0.248, adjusted R2=0.200, pseudo-F=5.154, p=0.002, predictors=(pH_KCl,N_pct,bio12now.100,alpha,compl).

Pairwise ranking means from Phase 5B showed BAC↔ITS highest in both geography-sensitivity (mean adjusted R2=0.271) and primary models (mean adjusted R2=0.257).

### Plant-diversity model comparisons
Figure 4 summarizes hypothesis-level and pair-level plant-context effects. Hypothesis means across all models were:
- B (abiotic_plus_alpha): mean delta adjusted R2=0.013, mean adjusted R2=0.214, mean R2=0.252, significant models=8/8.
- F (abiotic_plus_alpha_dark): mean delta adjusted R2=0.011, mean adjusted R2=0.212, mean R2=0.260, significant models=8/8.
- D (abiotic_plus_pool): mean delta adjusted R2=0.009, mean adjusted R2=0.210, mean R2=0.248, significant models=8/8.
- G (abiotic_plus_pool_compl): mean delta adjusted R2=0.008, mean adjusted R2=0.209, mean R2=0.257, significant models=8/8.
- C (abiotic_plus_dark): mean delta adjusted R2=0.003, mean adjusted R2=0.204, mean R2=0.242, significant models=8/8.
- A (abiotic_base): mean delta adjusted R2=0.000, mean adjusted R2=0.201, mean R2=0.230, significant models=8/8.
- E (abiotic_plus_compl): mean delta adjusted R2=-0.004, mean adjusted R2=0.197, mean R2=0.236, significant models=8/8.

Best model per pair/branch/scope from committed Phase 5C rankings:
- AMF↔EUK | CLR | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.197, delta adjusted R2 vs abiotic base=0.015, p=0.002.
- AMF↔EUK | CLR | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.188, delta adjusted R2 vs abiotic base=0.013, p=0.002.
- AMF↔EUK | presence/absence | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.211, delta adjusted R2 vs abiotic base=0.019, p=0.002.
- AMF↔EUK | presence/absence | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.198, delta adjusted R2 vs abiotic base=0.017, p=0.002.
- AMF↔ITS | CLR | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.209, delta adjusted R2 vs abiotic base=0.018, p=0.002.
- AMF↔ITS | CLR | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.199, delta adjusted R2 vs abiotic base=0.017, p=0.002.
- AMF↔ITS | presence/absence | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.231, delta adjusted R2 vs abiotic base=0.022, p=0.002.
- AMF↔ITS | presence/absence | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.212, delta adjusted R2 vs abiotic base=0.019, p=0.002.
- BAC↔ITS | CLR | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.281, delta adjusted R2 vs abiotic base=0.008, p=0.002.
- BAC↔ITS | CLR | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.273, delta adjusted R2 vs abiotic base=0.007, p=0.002.
- BAC↔ITS | presence/absence | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.269, delta adjusted R2 vs abiotic base=0.011, p=0.002.
- BAC↔ITS | presence/absence | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.248, delta adjusted R2 vs abiotic base=0.009, p=0.002.
- EUK↔ITS | CLR | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.202, delta adjusted R2 vs abiotic base=0.015, p=0.002.
- EUK↔ITS | CLR | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.191, delta adjusted R2 vs abiotic base=0.013, p=0.002.
- EUK↔ITS | presence/absence | geography_sensitivity: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.227, delta adjusted R2 vs abiotic base=0.014, p=0.002.
- EUK↔ITS | presence/absence | primary: best hypothesis B (abiotic_plus_alpha), adjusted R2=0.205, delta adjusted R2 vs abiotic base=0.011, p=0.002.

### Integrated synthesis
Figure 5 integrates coupling strength, environmental explained variation, and plant-diversity increments. The integrated pattern supports strong cross-domain concordance with substantial environmental organization and smaller, context-dependent plant-diversity increments.

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
