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
### 1. Study system and dataset
Analyses were conducted on a matched soil-community dataset that integrated bacterial (BAC), fungal ITS (ITS), microbial eukaryote (EUK), and arbuscular mycorrhizal fungal (AMF) community matrices. All pairwise analyses used the shared overlap cohort reported in the results tables (n = 84 for each analyzed pair×branch combination in Phase 5 outputs). Pair definitions carried through the coupling, environmental, plant-diversity, and synthesis tables were BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK for the integrated layer, with BAC↔AMF and BAC↔EUK additionally retained in bacterial-integration coupling summaries.

### 2. Community data processing
Detailed sequencing and bioinformatics procedures are provided elsewhere and are not repeated here. Community data were analyzed under two representation branches documented in the analysis manifests: presence/absence and CLR. Presence/absence analyses used Jaccard distances and PCoA ordination in coupling tables; CLR analyses used Euclidean distances and PCA ordination. Threshold values were taken directly from manifest files. Coupling integration evaluated thresholds 0.05 and 0.10 (phase5_combo_manifest.csv), while environmental and plant-diversity models were evaluated at threshold 0.05 (phase5b_manifest.csv, phase5c_manifest.csv).

### 3. Cross-domain coupling analyses
Cross-domain concordance was quantified with two complementary outputs from results/phase5_bac_integration/: (i) Mantel Spearman correlations with permutation p-values and confidence intervals (phase5_bac_mantel_inference.csv), and (ii) Procrustes alignment summaries captured as fit and derived similarity (phase5_bac_coupling_summary.csv, phase5_bac_procrustes_bootstrap.csv). For each pair×branch, threshold-specific estimates (0.05, 0.10) were summarized as means and bounds. Pair-level ranking used phase5_bac_rank_summary.csv, with separate rank columns for Mantel and Procrustes similarity and an overall rank statistic. In integrated synthesis (final_coupling_rankings.csv), coupling strength was defined as the arithmetic mean of Mantel and Procrustes similarity for each pair×branch entry.

### 4. Environmental driver analyses
Environmental structure of pairwise community correspondence was quantified with distance-based redundancy analysis (dbRDA) summaries in results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv. Two model scopes were retained in the tables: primary models (pH_KCl, N_pct, bio12now.100, and context-specific biotic terms) and geography-sensitivity models that additionally included latitude and longitude. Predictor-level contributions were extracted from phase5b_predictor_ranking.csv using leave-one-predictor reduction statistics (delta R² and delta adjusted R²), and pair-level ordering was taken from phase5b_pair_rankings.csv. The final synthesis environmental layer (final_environment_driver_summary.csv) selected the best adjusted R² model per pair×branch and retained top predictor identity, pH contribution, and geography sensitivity deltas.

### 5. Plant-diversity hypothesis testing
Plant-diversity effects were evaluated using pre-specified nested hypothesis sets A–G from results/phase5c_plant_diversity/phase5c_model_comparison.csv: A (abiotic base), B (abiotic+alpha), C (abiotic+dark), D (abiotic+pool), E (abiotic+completeness), F (abiotic+alpha+dark), and G (abiotic+pool+completeness). For each pair×branch, model support was quantified as delta adjusted R² relative to hypothesis A (delta_adjusted_r2_vs_base). Hypothesis-level means and contrasts were read from phase5c_hypothesis_summary.csv, pair-level rankings from phase5c_pair_rankings.csv, and predictor-level reductions from phase5c_predictor_effects.csv. Final synthesis retained the strongest plant-diversity increment per pair×branch in final_plant_diversity_summary.csv.

### 6. Integrated synthesis
Integrated synthesis combined coupling (final_coupling_rankings.csv), environmental (final_environment_driver_summary.csv), and plant-diversity (final_plant_diversity_summary.csv) layers into final_pair_synthesis.csv. For each pair×branch, the synthesis table reports (i) coupling strength, (ii) environmental explained variation (dbRDA adjusted R² from the selected best model), and (iii) plant-diversity added variation (best non-base delta adjusted R²). This harmonized output was used for cross-layer ranking and pattern description.

### 7. Statistical analyses
All reported inferential statistics are taken directly from committed result tables without rerunning analyses. Mantel p-values and dbRDA/model-comparison p-values are permutation-based (499 permutations in the reported tables). Confidence intervals and bootstrap-derived variability were extracted exactly as recorded in the output CSVs (for example, Mantel confidence bounds by pair×branch×threshold and Procrustes conservative interval bounds in coupling summaries). Reported values in this manuscript are table-grounded and are presented as descriptive comparisons of ranked effects across pairings, branches, and hypothesis sets.


## Results
Figure 1 defines the shared analysis cohort (n = 84) used in the integrated pairwise summaries, and all numerical statements below are taken directly from the phase5 and synthesis result tables.

### 3.1 Cross-domain coupling hierarchy
The integrated coupling table (final_coupling_rankings.csv) showed a clear but non-uniform hierarchy across 12 pair×branch configurations. Coupling strength ranged from 0.319 (BAC↔AMF, CLR) to 0.574 (BAC↔ITS, presence/absence), a spread of 0.255. The top three integrated entries were BAC↔ITS (presence/absence, 0.574), EUK↔ITS (presence/absence, 0.538), and EUK↔ITS (CLR, 0.535). The next tier included BAC↔ITS (CLR, 0.462), AMF↔ITS (CLR, 0.460), and AMF↔ITS (presence/absence, 0.445), followed by BAC↔EUK (CLR, 0.440), AMF↔EUK (CLR, 0.433), and AMF↔EUK (presence/absence, 0.400). The three lowest integrated entries were BAC↔EUK (presence/absence, 0.360), BAC↔AMF (presence/absence, 0.359), and BAC↔AMF (CLR, 0.319).

The strongest Mantel signal was BAC↔ITS (presence/absence; Mantel = 0.584, p = 0.002), whereas the strongest Procrustes similarity was EUK↔ITS (CLR; 0.683). This divergence appears in phase5_bac_rank_summary.csv: BAC↔ITS (presence/absence) ranked first by Mantel but fifth by Procrustes similarity, while EUK↔ITS (CLR) ranked first by Procrustes similarity but seventh by Mantel.

Threshold-level Mantel outputs (phase5_bac_mantel_inference.csv) showed that ordering was not driven by a single threshold. BAC↔ITS (presence/absence) remained high at both thresholds (0.597 at 0.05; 0.571 at 0.10). EUK↔ITS remained moderate across branches (presence/absence: 0.438 at 0.05, 0.390 at 0.10; CLR: 0.409 at 0.05, 0.365 at 0.10). AMF↔ITS also remained positive (presence/absence: 0.460 and 0.459; CLR: 0.556 and 0.495). BAC↔EUK (presence/absence) was weak at both thresholds (0.201 and 0.143), including the only conservative Mantel p-value in this table that rose above 0.002 at threshold 0.10 (p = 0.018).

Procrustes similarities in phase5_bac_coupling_summary.csv separated pairs differently: EUK↔ITS was highest (0.662 presence/absence; 0.683 CLR), BAC↔ITS was intermediate-high (0.564 presence/absence; 0.565 CLR), and BAC↔AMF was lowest (0.339 presence/absence; 0.351 CLR). Thus, integrated hierarchy combined a BAC↔ITS Mantel maximum with an EUK↔ITS Procrustes maximum.

### 3.2 Environmental structure
Environmental explanatory power from final_environment_driver_summary.csv was non-trivial across all eight integrated pair×branch entries. Best-model adjusted R² values ranged from 0.188 (AMF↔EUK, CLR) to 0.278 (BAC↔ITS, CLR), with mean 0.223. Ordering by adjusted R² was: BAC↔ITS CLR (0.278) > BAC↔ITS presence/absence (0.265) > AMF↔ITS presence/absence (0.225) > EUK↔ITS presence/absence (0.222) > AMF↔EUK presence/absence (0.206) > AMF↔ITS CLR (0.204) > EUK↔ITS CLR (0.195) > AMF↔EUK CLR (0.188).

All final entries selected geography-sensitivity as best model, and all listed pH_KCl as top predictor. The pH contribution statistic ranged from 0.09195 (AMF↔ITS CLR) to 0.15099 (BAC↔ITS CLR), with mean 0.11260. Geography sensitivity deltas were positive in every entry, ranging from 0.00795 to 0.02189 (mean 0.01389); the largest delta occurred for EUK↔ITS presence/absence (0.02189), and the smallest for AMF↔EUK CLR (0.00795).

The full dbRDA table (phase5b_dbRDA_summary.csv) was concordant with synthesis values: primary and geography-sensitivity models were significant for each pair×branch (permutation p = 0.002), and geography-sensitivity adjusted R² exceeded primary adjusted R² in all cases. Pair-level ordering in phase5b_pair_rankings.csv was stable by model type (BAC↔ITS first, AMF↔ITS second, EUK↔ITS third, AMF↔EUK fourth). Predictor ranking rows in phase5b_predictor_ranking.csv also retained pH-first ordering in primary models: pH_KCl (0.10939) > alpha (0.01145) > N_pct (0.00945) > bio12now.100 (0.00636) > compl (-0.00548).

### 3.3 Plant-diversity hypotheses
Plant-diversity model comparison tables showed consistent ranking among hypotheses A–G. In phase5c_hypothesis_summary.csv, mean delta adjusted R² relative to abiotic base (A) followed: B (abiotic+alpha) = 0.01319, F (abiotic+alpha+dark) = 0.01099, D (abiotic+pool) = 0.00870, G (abiotic+pool+completeness) = 0.00776, C (abiotic+dark) = 0.00286, A = 0.00000, and E (abiotic+completeness) = -0.00373. All eight models per hypothesis were significant by permutation (n_significant = 8 of 8).

Direct contrasts in the same table reinforced this order: C_vs_B = -0.01033, D_vs_B = -0.00449, E_vs_B = -0.01693, F_vs_B = -0.00221, and G_vs_D = -0.00094. Thus alpha-containing model B outperformed dark-only, pool-only, and completeness-only alternatives on mean delta adjusted R².

Pair-level best-model extraction from phase5c_model_comparison.csv showed that hypothesis B was the highest non-base model in every primary-scope pair×branch. Delta adjusted R² for B ranged from 0.00732 (BAC↔ITS CLR) to 0.01898 (AMF↔ITS presence/absence). Ordering across the eight integrated entries was: AMF↔ITS presence/absence (0.01898) > AMF↔EUK presence/absence (0.01716) > AMF↔ITS CLR (0.01651) > EUK↔ITS CLR (0.01303) > AMF↔EUK CLR (0.01279) > EUK↔ITS presence/absence (0.01083) > BAC↔ITS presence/absence (0.00893) > BAC↔ITS CLR (0.00732).

The final synthesis plant table (final_plant_diversity_summary.csv) showed alpha effect positive in all eight entries and equal to selected best delta (because B was best throughout). Pool effect was also positive in all entries (0.00510 to 0.01158), dark effect was smaller but positive (0.00077 to 0.00495), and completeness effect was negative in all entries (-0.00500 to -0.00281).

### 3.4 AMF-linked responses
AMF-linked pairings (AMF↔ITS and AMF↔EUK, both branches) differed from BAC↔ITS by balance among layers rather than by a single metric reversal.

Coupling ranks were lower for AMF-linked entries than for BAC↔ITS presence/absence. BAC↔ITS presence/absence had coupling strength 0.574, while AMF↔ITS and AMF↔EUK entries ranged from 0.400 to 0.460. BAC↔ITS CLR (0.462) exceeded AMF↔EUK CLR (0.433) and AMF↔EUK presence/absence (0.400), and was near AMF↔ITS CLR (0.460).

AMF-linked entries were also not the strongest environmental fits: their best adjusted R² values ranged from 0.188 to 0.225, versus 0.265–0.278 for BAC↔ITS. AMF↔EUK CLR had the lowest environmental adjusted R² in the integrated table (0.188).

In contrast, AMF-linked entries had the largest plant-diversity increments. The top three deltas in final_plant_diversity_summary.csv were AMF↔ITS presence/absence (0.01898), AMF↔EUK presence/absence (0.01716), and AMF↔ITS CLR (0.01651), compared with 0.00893 and 0.00732 for BAC↔ITS presence/absence and CLR. AMF↔ITS plant increments were therefore ~2.13× and ~2.25× the corresponding BAC↔ITS values.

### 3.5 Integrated ecological synthesis
The synthesis table (final_pair_synthesis.csv) aligned coupling, environmental, and plant-diversity layers across eight integrated pair×branch entries.

At the upper coupling end, BAC↔ITS presence/absence (0.574) and both EUK↔ITS entries (0.538 and 0.535) formed the dominant concordance cluster. Within this cluster, environmental explained variation remained substantial (0.195 to 0.265), and plant-diversity added variation remained positive but smaller (0.00893 to 0.01303).

At intermediate coupling levels, BAC↔ITS CLR (0.462) and AMF↔ITS CLR (0.460) had similar coupling strengths but contrasting auxiliary layers: BAC↔ITS CLR had maximum environmental explained variation (0.278) and the smallest plant increment (0.00732), while AMF↔ITS CLR had lower environmental explained variation (0.204) and higher plant increment (0.01651).

At lower coupling levels, AMF↔EUK presence/absence (0.400) and AMF↔EUK CLR (0.433) retained positive plant additions (0.01716 and 0.01279) despite lower coupling and lower environmental adjusted R² (0.206 and 0.188).

Across all eight integrated entries, numerical ranges were: coupling strength 0.400–0.574; environmental explained variation 0.188–0.278; plant-diversity added variation 0.00732–0.01898. Overall, integrated outputs identified a coupling hierarchy led by BAC↔ITS and EUK↔ITS, a consistently pH-led environmental layer with positive geography deltas in every entry, and a plant-diversity layer uniformly led by hypothesis B with strongest increments in AMF-linked pairings.


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
