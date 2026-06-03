# Title
Environment-structured cross-domain soil microbiome coupling with AMF-linked plant responsiveness: an integrated ecological synthesis

## Abstract
Cross-domain concordance in soil microbiomes can emerge from shared environmental filtering, biological interaction, or both, but observational amplicon datasets rarely separate these pathways directly. We synthesized completed analysis outputs for BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK across presence/absence and CLR data representations. The strongest combined coupling signal was BAC↔ITS presence/absence, with an integrated coupling index of 0.574 (a unitless composite score summarizing distance-matrix concordance metrics), followed by EUK↔ITS presence/absence (0.538) and EUK↔ITS CLR (0.535). Environmental structure was substantial, with adjusted explained-variation values ranging from 0.188 to 0.278, indicating that abiotic filtering is a major component of cross-domain structure. Added explanatory signal from plant-diversity terms was smaller but repeatable, with increases of approximately 0.007 to 0.019 in adjusted explained variation; alpha diversity contributed more than dark diversity and completeness in the integrated summaries (mean standardized contributions: alpha 0.013, dark 0.003, completeness -0.004). AMF-linked pairings were not the highest in overall coupling magnitude but showed comparatively elevated plant-associated increments. Together, these results support a layered interpretation in which cross-domain coupling is strong, strongly environment-structured, and secondarily modulated by plant context.

## Introduction
Soil microbial communities are assembled through interacting deterministic and contingent processes that operate simultaneously across bacteria, fungi, and microeukaryotes. At community scale, cross-domain concordance can arise when multiple groups respond to the same abiotic gradients, when groups interact directly through trophic or metabolic links, or when both mechanisms act together (Jagadesh et al., 2024; Li et al., 2023). This inferential overlap is a central challenge in observational microbiome ecology: strong association structure does not, by itself, identify the dominant mechanism.

Bacteria-fungi coupling has repeatedly been linked to decomposition dynamics, rhizosphere turnover, and nutrient transformations. Fungal substrate access and bacterial metabolite processing can generate coordinated community responses under shared resource regimes, while local context determines the relative contribution of co-response versus direct interaction (Rossmann et al., 2020; Wang et al., 2024; Slanzon et al., 2025). For this reason, cross-domain concordance is ecologically meaningful, but mechanism claims must remain conservative when manipulative evidence is unavailable.

Arbuscular mycorrhizal fungi (AMF) add a distinct ecological axis because they connect soil communities to plant carbon allocation, root architecture, and host filtering. AMF-linked cross-domain patterns therefore may be most visible as plant-context sensitivity rather than maximal global coupling strength. This perspective predicts that AMF-associated pairings can carry strong ecological relevance even when they are not top-ranked by aggregate concordance metrics.

Environmental filtering is especially important in this context. Edaphic gradients, and pH in particular, are known to organize broad microbial turnover across domains by integrating multiple chemical and physiological constraints, including nutrient availability, ion stress, and enzyme operating space (Rath et al., 2018). If cross-domain concordance tracks these gradients, high coupling may largely represent shared filtering with additional biological modulation.

Dark diversity and completeness metrics provide a complementary assembly lens by representing absent-but-ecologically-possible taxa and realized occupancy relative to the species pool (Pärtel et al., 2013; Pärtel, 2014; Pärtel et al., 2025). However, dark-diversity formulations can depend strongly on pool definition and detection boundaries, so comparative interpretation with observed alpha diversity should be explicit about uncertainty and dependence structure.

The key knowledge gap addressed here is not whether cross-domain coupling exists, but how to interpret its ecological layers without overstating mechanism. We therefore integrate completed outputs in a fixed order: coupling strength, environmental structure, and plant-diversity increment. Our working expectations are that BAC↔ITS will show the strongest overall coupling, environmental filtering will explain a substantial share of structure, and AMF-linked pairings will show comparatively stronger plant-context responsiveness than their global coupling rank suggests.

## Methods
### Study dataset and sample counts
All analyses were based on the completed cohort used in the project outputs. The shared sample cohort included 84 samples (sample-level overlap file), enabling direct cross-domain comparisons among BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK pairings.

### Sequencing datasets and domain pair definitions
The synthesis uses previously generated community tables and pairing summaries for bacterial (BAC), fungal ITS (ITS), eukaryotic (EUK), and AMF-resolved subsets. Pairwise integration was performed at the sample level and interpreted only through completed artifacts.

### Data transformations and distance representations
Two data representations were carried through the completed outputs: presence/absence and CLR-based representations. These are treated as complementary encodings of community structure rather than competing truth models.

### Mantel workflow
Distance-matrix correlation outputs were used to summarize cross-domain concordance. Mantel statistics were interpreted as matrix-level association magnitudes between paired community-distance structures, with significance and uncertainty taken from completed permutation-based outputs.

### Procrustes workflow
Ordination-concordance outputs were used as a geometric complement to matrix-correlation results. Procrustes-derived quantities were interpreted as shape-alignment indicators between paired ordination configurations, and then integrated with Mantel-layer information in downstream ranking summaries.

### Environmental-structure workflow
Environmental contribution was quantified from completed constrained-ordination summaries using adjusted explained variation. The interpreted range in the integrated outputs was 0.188 to 0.278 (unitless adjusted explained-variation values), and predictor prominence summaries consistently highlighted pH-centered structure.

### Plant-diversity model workflow
Plant-context increments were interpreted from completed comparisons that added plant-diversity descriptors to abiotic baselines. Reported increments represent additive changes in adjusted explained variation. Integrated summaries include alpha diversity, dark diversity, and completeness contribution patterns.

### Permutation settings and uncertainty framing
All inferential statistics were taken from completed outputs that used permutation-based significance estimation. P-values and confidence intervals were interpreted conservatively, with emphasis on effect-size ordering and consistency across analysis layers rather than threshold-only reasoning.

### Synthesis procedure
Final interpretation followed a fixed sequence: first rank pairings by integrated coupling index, then evaluate environmental explained variation, then quantify plant-associated increment. This order was used to separate total concordance from likely environmental structure and secondary plant-context modulation.

## Results
### Coupling structure from matrix concordance and geometric alignment
Cross-domain coupling was strongest for BAC↔ITS in the presence/absence representation, where the integrated coupling index reached 0.574. EUK↔ITS followed closely, with values of 0.538 in presence/absence and 0.535 in CLR. Here, each number in parentheses is the integrated coupling index value itself, expressed as a unitless composite score that ranks relative coupling strength across pairings and representations. AMF-linked pairings showed lower integrated coupling scores than BAC↔ITS and EUK↔ITS, indicating that AMF-associated signals are not the dominant component of total cross-domain concordance in this cohort.

### Environmental structure of cross-domain coupling
Environmental explained variation remained substantial across pairings. Adjusted explained-variation values ranged from 0.188 to 0.278, showing that nearly one-fifth to over one-quarter of modeled cross-domain structure aligned with measured environmental gradients. In this context, pH-centered predictors repeatedly appeared among the most influential environmental terms, supporting the interpretation that strong coupling can emerge from shared abiotic filtering across domains.

### Plant-diversity increments beyond abiotic baselines
When plant-diversity descriptors were added to abiotic baselines, added explained variation was modest but repeatable. The observed increment range was approximately 0.007 to 0.019 in adjusted explained variation (that is, about 0.7 to 1.9 additional percentage points of explained structure in unitless adjusted-R² terms). Integrated contribution summaries showed larger alpha-diversity contribution values (0.013) than dark-diversity (0.003) or completeness (-0.004), indicating stronger incremental signal from realized local diversity in this dataset.

### AMF-linked responsiveness relative to global coupling rank
Although AMF↔ITS and AMF↔EUK were not top-ranked in global coupling magnitude, their plant-associated increments were comparatively elevated relative to their coupling rank position. In natural-language terms, AMF-linked pairings behaved more like context-responsive components than globally dominant coupling hubs. This pattern is consistent with AMF functioning at the plant-soil interface, where response sensitivity to host context can be strong even when aggregate cross-domain concordance is moderate.

### Integrated ecological reading across analysis layers
Taken together, the ordered results indicate a layered structure: high total cross-domain concordance, substantial environmental organization, and smaller but recurring plant-context additions. This sequence supports conservative mechanism language: strong coupling is evident, shared environmental filtering is a major explanation for that structure, and plant-associated effects refine rather than replace the environmental signal.

## Discussion
### Environmental filtering as a primary organizing axis
The strongest pairings co-occurred with substantial adjusted explained variation from environmental terms, and this repeated pattern supports environmental filtering as a major structuring process. The recurrent prominence of pH-centered predictors further strengthens this interpretation because pH integrates multiple chemical and physiological constraints that can synchronize turnover across bacterial and fungal components.

### Ecological meaning of BAC↔ITS dominance
BAC↔ITS remained the highest-ranked integrated coupling signal. Ecologically, this is compatible with known bacterial-fungal complementarity in decomposition and nutrient cycling, but the present evidence supports a combined interpretation of shared filtering plus potential interaction rather than direct interaction alone. This distinction is important for causal restraint in observational studies.

### Why AMF-linked patterns remain important
AMF-linked pairings were not the strongest in absolute coupling rank, yet their comparatively elevated plant-associated increments indicate a distinct response profile. This supports interpretation of AMF-linked structure as a plant-interface sensitivity signal. In other words, AMF-linked effects may be most informative for context-dependent assembly rather than for maximal whole-matrix concordance.

### Interpreting alpha, dark diversity, and completeness
Alpha diversity produced stronger incremental signal than dark diversity and completeness under the current modeling structure. This result does not invalidate dark-diversity concepts; instead, it suggests that realized local diversity carried clearer explanatory information in this cohort, while dark-diversity and completeness terms likely retain value when uncertainty in species-pool definition is more explicitly modeled.

### Methodological boundaries and inference limits
All findings are based on completed observational outputs and should be interpreted with corresponding limits. Composite coupling indices are ranking tools, permutation-based significance has finite resolution, and compositional plus sparsity properties can shape distance-based behavior. These constraints limit mechanism claims but do not negate the consistency of the layered ecological signal identified here.

## Conclusions
Cross-domain coupling is strong in this dataset, with BAC↔ITS providing the highest integrated signal and EUK↔ITS close behind. Environmental structure is substantial, with adjusted explained-variation values from 0.188 to 0.278 and repeated pH-centered prominence. Plant-diversity additions are smaller but consistent, ranging from approximately 0.007 to 0.019, and alpha diversity contributes more than dark diversity or completeness in integrated summaries. AMF-linked pairings are best interpreted as plant-context-responsive components rather than dominant global coupling hubs. Overall, the completed outputs support a layered ecological interpretation that is quantitatively grounded and causally conservative.

## References
Bastiaanssen, T., Quinn, T., & Loughman, A. (2022). Bugs as features (part 1): Concepts and foundations for the compositional data analysis of the microbiome-gut-brain axis. https://www.semanticscholar.org/paper/98f14db0c26bf35059d1cf59146fbd1956acea09

Jagadesh, M., Dash, M., Kumari, A., Singh, S. K., Verma, K., & Kumar, P. (2024). Revealing the hidden world of soil microbes: Metagenomic insights into plant, bacteria, and fungi interactions for sustainable agriculture and ecosystem restoration. https://www.semanticscholar.org/paper/bef531e148192fce5f047c071646deff6b4aa97d

Li, Y., Chen, Z., Wagg, C., Castellano, M. J., Zhang, N., & Ding, W. (2023). Soil organic carbon loss decreases biodiversity but stimulates multitrophic interactions that promote belowground metabolism. https://www.semanticscholar.org/paper/1e120b5423e78fe48c255ef67ef7702e5cc3a804

Pärtel, M. (2014). Community ecology of absent species: Hidden and dark diversity. https://www.semanticscholar.org/paper/9ace84d02cec657111c95295014e0185e225b3cb

Pärtel, M., Szava-Kovats, R., & Zobel, M. (2013). Community completeness: Linking local and dark diversity within the species pool concept. https://www.semanticscholar.org/paper/ad5e291154b3edb084f90c90f6f9c949aa4db79b

Pärtel, M., Tamme, R., Carmona, C. P., Riibak, K., Moora, M., & Bennett, J. A. (2025). Global impoverishment of natural vegetation revealed by dark diversity. https://www.semanticscholar.org/paper/3c126e3f14a48d2875ff7a66ab84b2594c967cba

Rath, K. M., Fierer, N., Murphy, D., & Rousk, J. (2018). Linking bacterial community composition to soil salinity along environmental gradients. https://www.semanticscholar.org/paper/d00c46b5c0a95da3cc3b45fb2d1995dfec68ecdf

Rossmann, M., Pérez-Jaramillo, J., Kavamura, V. N., Chiaramonte, J., Dumack, K., & Fiore-Donno, A. (2020). Multitrophic interactions in the rhizosphere microbiome of wheat: From bacteria and fungi to protists. https://www.semanticscholar.org/paper/42d03d0b39981b892d93906ab599f2fb05e02344

Slanzon, G. S., Yuan, M., Estera-Molina, K., Chew, A., Blazewicz, S., & Allen, M. (2025). Quantitative stable isotope probing (qSIP) and cross-domain networks reveal bacterial-fungal interactions in the hyphosphere. https://www.semanticscholar.org/paper/d3d786e9358dcd5877889917be2582a7fc39dd3e

Wang, B., Chen, C., Xiao, Y., Chen, K., Wang, J., & Zhao, S. (2024). Trophic relationships between protists and bacteria and fungi drive the biogeography of rhizosphere soil microbial community and impact plant physiological and ecological functions. https://www.semanticscholar.org/paper/0e79f563128e9c8b3487b5dc217e44186627e9f3

Weiss, S. J., Xu, Z., Peddada, S., Amir, A., Bittinger, K., & Gonzalez, A. (2017). Normalization and microbial differential abundance strategies depend upon data characteristics. https://www.semanticscholar.org/paper/5415ab67f45cff058ddb86a65d073da7714b91c0
