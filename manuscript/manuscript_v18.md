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
### 2.1 Study system and matched cohort
We analyzed a matched cross-domain soil microbiome cohort containing 84 sites with complete overlap across bacterial communities (BAC), fungal internal transcribed spacer profiles (ITS), microbial eukaryotes (EUK), and arbuscular mycorrhizal fungi (AMF). This study included 84 sites distributed across six continents within the DarkDivNet framework (Europe 54, Asia 14, North America 8, Africa 1, South America 4, and Oceania 3; Fig. 1). Plant community data and derived plant-diversity metrics were taken from Pärtel et al. (2025, Nature), based on standardized DarkDivNet vegetation surveys at each site. In that framework, each site corresponds to a 100 m² (10 × 10 m) vegetation plot embedded within a study region of approximately 300 km², defined as a circle of 20 km diameter subject to coastline and access constraints. Vegetation-side predictors included local plant richness, plant dark diversity (absent species that can potentially inhabit the study site), plant species pool size (local plant richness plus dark diversity), and plant community completeness (the percentage of local plant richness from species pool size). Local observed plant richness was recorded by experienced botanists. Dark diversity was estimated from species co-occurrence patterns within each region using 30 similar vegetation plots and dark-diversity probabilities for species absent from the focal site but present regionally. Additional details are provided in Pärtel et al. (2025).

Pairwise cross-domain analyses included BAC↔ITS, EUK↔ITS, AMF↔ITS, AMF↔EUK, BAC↔AMF, and BAC↔EUK, all evaluated on the same matched sample set.

### 2.2 Sequencing and bioinformatics
Laboratory sequencing and initial bioinformatics processing protocols are documented in the underlying project workflow and related DarkDivNet resources and are not repeated here. The present Methods focus on downstream ecological and statistical analyses applied to the completed community matrices.

### 2.3 Community representations and prevalence filtering
To evaluate cross-domain correspondence under complementary assumptions about community structure, each domain pair was analyzed in two representations: presence/absence and centered log-ratio (CLR) transformed abundance space. Presence/absence analyses used binary community matrices with Jaccard dissimilarity and principal coordinates analysis (PCoA). CLR analyses used a pseudocount of 1×10⁻⁶, CLR transformation, Euclidean distance, and principal component analysis (PCA) projected onto 10 ordination axes for cross-domain comparison.

Prevalence filtering was applied before ordination and coupling analyses to reduce sensitivity to extremely rare taxa and evaluate robustness to rare-taxon inclusion. Specifically, taxa with non-zero occurrence in fewer than 5% or 10% of samples were removed, corresponding to prevalence thresholds of 0.05 and 0.10. These dual thresholds were carried through coupling analyses to test whether inferred cross-domain structure depended on retention of low-prevalence taxa.

### 2.4 Cross-domain coupling analyses
Cross-domain coupling was quantified using two complementary statistics: Mantel Spearman correlation for concordance among inter-sample distance matrices and Procrustes analysis for geometric alignment between paired ordination configurations. Mantel inference used 499 permutations, and Procrustes uncertainty was summarized from 120 bootstrap replicates with percentile intervals (2.5th and 97.5th percentiles).

Because Mantel and Procrustes capture different facets of correspondence, both were reported separately and jointly through an integrated coupling score defined as the mean of Mantel correlation and Procrustes similarity. In this formulation, Mantel describes matrix-level concordance, whereas Procrustes describes alignment of multivariate spatial structure; averaging the two provides a descriptive synthesis metric and comparative integration aid when both rank-order and geometric agreement are of interest. The integrated score was used within a descriptive integration framework rather than as a formal inferential statistic.

### 2.5 Environmental-driver analyses
Environmental predictor selection was hypothesis-driven and focused on variables expected to influence microbial assembly across domains, including soil pH (pH_KCl), soil nitrogen content (N_pct), and annual precipitation (bio12). Geography-sensitivity models additionally included latitude and longitude to evaluate spatially structured residual variation. Distance-based redundancy analysis (dbRDA) was fitted for each pair×representation combination at the default prevalence threshold of 0.05 with 499 permutations.

Soil carbon percentage (C_pct) was not included in models containing soil nitrogen because of strong collinearity between variables. Predictor influence was quantified using leave-one-predictor reductions (ΔR² and Δ adjusted R²), and model adequacy across predictor sets was compared using adjusted R².

### 2.6 Plant-diversity hypothesis testing
To evaluate whether plant diversity explained variation in microbial coupling beyond abiotic conditions, we compared seven a priori candidate models (A–G) against an abiotic baseline model. Model A included abiotic predictors only; model B added alpha diversity; model C added dark diversity; model D added species pool size; model E added community completeness; model F added alpha plus dark diversity; and model G added species pool plus completeness.

Plant-diversity hypotheses were structured to distinguish realized local diversity (alpha diversity), potentially recruitable absent taxa (dark diversity), regional species-pool context, and the extent to which local communities approach that pool (completeness). Because alpha diversity, dark diversity, and species pool are mathematically related, these metrics were emphasized in separate candidate formulations rather than pooled into a single maximal model. Plant-diversity comparisons used CLR-transformed inputs (pseudocount 1×10⁻⁶), 10 ordination axes, the default prevalence threshold (0.05), and 499 permutations. Incremental support for each hypothesis was quantified as Δ adjusted R² relative to the abiotic baseline.

### 2.7 Integrated synthesis
To compare ecological signal layers across pair×representation combinations, we integrated three outputs: (i) coupling magnitude from Mantel-Procrustes summaries, (ii) environmental explained variation from best-performing dbRDA formulations, and (iii) added plant-diversity variation from best non-baseline plant models. For consistent interpretation across pairings, summaries were evaluated using descriptive thresholds (coupling strength ≥0.50, environmental adjusted R² ≥0.20, and plant-diversity Δ adjusted R² ≥0.01; low-plant criterion <0.005). These thresholds were used as interpretive guides for comparative synthesis and not as replacements for permutation-based inference.

### 2.8 Statistical analyses
All inferences in this manuscript were derived from completed analysis outputs, and no analyses were rerun during manuscript preparation. Significance testing for Mantel, dbRDA, and model-comparison layers used permutation-based inference (499 permutations). Procrustes uncertainty was estimated by bootstrap resampling (120 replicates), and uncertainty intervals were summarized with percentile limits (2.5th–97.5th). Across analytical layers, effect-size comparison and ranking focused on adjusted R² and Δ adjusted R² to support consistent interpretation across differing predictor structures.


## Results
Figure 1 defines the matched cohort (n = 84), and Figures 2–5 present a connected results sequence from cross-domain coupling to environmental structure, plant-diversity effects, and final synthesis.

### 3.1 Cross-domain coupling patterns
Cross-domain coupling was strongest for BAC↔ITS, especially in presence/absence space (coupling strength 0.574; Fig. 2). EUK↔ITS remained close behind across both representations (0.538 and 0.535), and total coupling values spanned 0.319–0.574 across 12 pair×representation combinations, indicating broad but uneven synchrony among domains.

Mantel and Procrustes highlighted complementary biological structure rather than a single ranking. BAC↔ITS showed the strongest distance-matrix concordance (Mantel ρ = 0.584, p = 0.002), whereas EUK↔ITS in CLR showed the highest geometric alignment (Procrustes similarity = 0.683). Together, these patterns indicate that pairings can align strongly in community-distance structure without being identical in ordination geometry, and vice versa.

This dominant BAC↔ITS signal was stable across prevalence thresholds (Mantel ρ = 0.597 at 0.05; 0.571 at 0.10). BAC↔EUK presence/absence remained comparatively weak and declined at the more conservative cutoff (ρ = 0.143, p = 0.018).

### 3.2 Environmental structure of coupled turnover
To keep cross-layer comparisons consistent, environmental synthesis focused on the four pairs carried into integration (BAC↔ITS, EUK↔ITS, AMF↔ITS, AMF↔EUK; Fig. 3). BAC↔ITS again showed the most pronounced environmental structuring (dbRDA adjusted R² = 0.278 in CLR; 0.265 in presence/absence), and explained variation across integrated pairings ranged from 0.188 to 0.278 (mean 0.223).

Environmental effects were coherent across pairings: geography-sensitive models were selected in all integrated cases, pH_KCl was the top predictor throughout, geography sensitivity was consistently positive (Δadjusted R² = 0.008–0.022), and pH contributions remained substantial (0.092–0.151). Model-level permutation tests were significant across pair×representation combinations (p = 0.002).

### 3.3 Plant-diversity contrasts across pairings
Plant-diversity effects were modest but consistently positive overall, with the largest gains concentrated in AMF-linked relationships (Fig. 4). Hypothesis-level summaries showed the highest mean gains for alpha-containing structure (model B), followed by pooled and dark-diversity formulations (models F and D), while completeness-only structure (model E) was negative on average.

At the pair level, AMF-linked combinations had the largest plant-diversity increments (about 0.017–0.019 in presence/absence), whereas BAC↔ITS remained smaller (0.009 in presence/absence; 0.007 in CLR). Thus, AMF↔ITS gains were approximately two-fold larger than BAC↔ITS gains in both representations, with alpha, pool, and dark components positive across integrated entries and completeness consistently negative (Fig. 4).

### 3.4 Integrated pattern across analytical layers
Taken together, Figures 2–5 resolve a consistent cross-layer ecological contrast. BAC↔ITS combines the highest coupling with the most pronounced environmental structure, but shows the smallest plant-diversity increment. AMF-linked pairings show the opposite profile: comparatively weaker coupling and lower-to-moderate environmental structuring, but the largest plant-diversity responsiveness.

EUK↔ITS is intermediate, retaining high coupling with moderate environmental and plant-diversity components. Across all layers, the main biological pattern is stable: BAC↔ITS leads system-level coupling and environmental organization, whereas AMF-linked relationships are most sensitive to plant-diversity variation.


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
