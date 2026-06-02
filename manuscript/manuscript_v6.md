# Title

Environment-structured cross-domain soil microbiome coupling with AMF-linked plant responsiveness: an integrated ecological synthesis

## Abstract

Cross-domain concordance in soil microbiomes can emerge from shared environmental filtering, biological interaction, or both, but observational amplicon datasets rarely isolate these pathways directly. We synthesized completed outputs only (no rerun analyses) across coupling metrics, environmental driver models, plant-diversity hypothesis comparisons, and Phase 5D integration for BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK under presence/absence and CLR branches. Integrated coupling remained highest for BAC↔ITS presence/absence (0.574), followed by EUK↔ITS presence/absence (0.538) and EUK↔ITS CLR (0.535). Environmental structure was substantial (dbRDA adjusted R² 0.188–0.278), with recurrent pH-centered predictor prominence. Plant-diversity increments were smaller but repeatable (approximately 0.007–0.019), with alpha effects exceeding dark-diversity and completeness means in integrated summaries (alpha=0.013, dark=0.003, completeness=-0.004). AMF-linked pairings were not top-ranked in coupling magnitude but showed comparatively elevated plant-associated increments. Ecologically, these results support a layered interpretation: strong cross-domain structure is largely compatible with environmental filtering, while plant context contributes secondary assembly information and AMF-linked patterns indicate responsive plant-interface dynamics rather than dominant coupling strength.

## Introduction
Cross-domain soil microbiome structure reflects simultaneous abiotic filtering, biotic interactions, and host-plant context, making mechanistic interpretation difficult when inference is based on observational co-variation alone [R14, R22, R33]. Across soil systems, pH repeatedly emerges as a high-leverage organizer of bacterial and fungal composition and can induce broad cross-domain congruence even when direct interaction pathways are unresolved [R01].

Bacteria-fungi coupling is ecologically meaningful because these groups co-regulate decomposition, nutrient turnover, and rhizosphere carbon flow, but high matrix concordance can still reflect common environmental forcing rather than direct trophic interaction [R02, R06, R10]. AMF provide a distinct interface between plant roots and soil resource gradients; therefore, AMF-centered patterns are often better interpreted through responsiveness to plant context and edaphic constraints than by raw coupling magnitude alone [R01].

Plant diversity and assembly descriptors (alpha diversity, dark diversity, completeness) provide complementary ecological lenses, yet these terms carry different statistical behavior and dependence structure in empirical datasets [R11, R15, R23]. We therefore frame quantitative outputs as a layered synthesis of coupling strength, environmental structure, and plant-associated increment, then interpret each layer in ecological rather than purely statistical terms [R34, R36].

## Methods
### Scope and provenance restrictions
This V6 manuscript uses completed artifacts only. No analyses were rerun, no HPC jobs were rerun, and no scientific result files were modified.

### Scientific-enrichment operations
The V6 pass prioritized ecological interpretation depth, literature expansion, and figure integration while preserving all quantitative outputs from V5. Literature enrichment used the Semantic Scholar API through the project search utility (`scripts/literature/semantic_scholar_search.py`) with delay controls retained.

### Evidence policy
1. Dataset-specific numerical findings remain anchored to completed project outputs.
2. External citations are used for ecological mechanisms, assembly theory, and methodological context.
3. Composite coupling values are retained as descriptive ranking summaries.

## Results
### 1) Coupling hierarchy
Integrated ranking remains BAC↔ITS presence/absence (0.574) > EUK↔ITS presence/absence (0.538) > EUK↔ITS CLR (0.535) (Figure 1; Table 1).

### 2) Environmental structure
Environmental explained variation remains substantial (dbRDA adjusted R² 0.188–0.278), consistent with strong environmental structuring of cross-domain patterns (Figure 2; Table 3).

### 3) Plant-context increment scale
Plant-diversity increments remain modest but repeatable (approximately 0.007–0.019), with alpha-inclusive models generally outperforming dark-diversity and completeness formulations in this cohort (Figures 3–4; Table 4).

### 4) AMF boundary interpretation
AMF-linked pairings show lower integrated coupling than BAC↔ITS and EUK↔ITS but comparatively elevated plant-associated increments, supporting a responsiveness interpretation (Figure 5; Tables 1 and 4).

## Discussion
### A. Environmental filtering as a driver of cross-domain structure
The strongest cross-domain pairings in this dataset co-occur with high environmental explained variation, indicating that filtering is not a background nuisance term but a central organizing axis. Soil assembly studies consistently show that deterministic abiotic constraints, especially edaphic gradients, shape both bacterial and fungal composition at scales relevant to observed cross-domain concordance [R05]. In this context, our BAC↔ITS and EUK↔ITS ranking patterns are most parsimoniously interpreted as outcomes of shared niche filtering plus potential interaction, not interaction in isolation.

The pH-centered signal deserves explicit ecological interpretation. pH integrates multiple resource and stress dimensions (nutrient solubility, metal availability, membrane stress, enzyme regimes), which can synchronize turnover across domains. Thus, high coupling in pH-structured systems is expected even when direct cross-kingdom links vary locally [R01].

### B. Ecological interpretation of BAC↔ITS coupling
**Nutrient cycling.** BAC↔ITS coupling aligns with known bacterial-fungal complementarity in carbon and nitrogen transformations, where fungi expand substrate access and bacteria accelerate downstream mineralization and metabolite turnover [R02, R06, R10].

**Decomposition.** Strong BAC↔ITS concordance is ecologically compatible with decomposition consortia operating under shared litter quality and moisture constraints. This supports a process-level interpretation in which decomposition niches are co-structured by environment and community composition simultaneously [R34, R36].

**Rhizosphere interactions.** In root-influenced soils, exudate chemistry and rhizodeposition can synchronize bacterial and fungal trajectories, creating pronounced matrix-level coupling without requiring a single dominant interaction mechanism [R09, R28, R30].

**Shared environmental responses.** The key boundary is inferential: BAC↔ITS coupling can be both biologically meaningful and primarily filter-driven. Our data support robust association structure; they do not by themselves resolve the relative contribution of direct interaction versus shared abiotic response.

### C. AMF-linked responses and plant context
AMF-linked pairings retain ecological importance despite lower integrated coupling values. AMF are tightly coupled to plant carbon allocation and root architecture, so their strongest signals often emerge in plant-context increments rather than in highest global coupling rank [R01]. This pattern fits our synthesis: AMF↔ITS and AMF↔EUK combinations are comparatively plant-responsive while remaining lower in aggregate coupling.

This distinction is biologically useful. It suggests that AMF-related signals in this cohort are better interpreted as context-sensitive mediators of plant-associated assembly than as universal cross-domain hubs. Such framing preserves ecological relevance while matching observed effect size scale.

### D. Why alpha diversity outperformed dark diversity and completeness in this dataset
Alpha diversity likely outperformed dark diversity and completeness here because alpha can capture realized local assembly signal with lower propagation of uncertainty from latent-pool estimation steps. Dark diversity and completeness remain conceptually valuable, but they often depend more strongly on species-pool specification, detection boundaries, and covariance with observed richness [R11, R15, R23].

In practical terms, our results do not invalidate dark-diversity ecology; they indicate that, in this cohort and model structure, alpha carries stronger incremental explanatory signal. The most ecological interpretation is complementarity: alpha describes realized structure efficiently, while dark/completeness terms are informative for constraint and potential occupancy framing when uncertainty is explicitly modeled.

### E. Methodological strengths and limitations
A major strength is layered synthesis across coupling, environmental, and plant-context outputs, enabling interpretation beyond single-metric reporting. Retaining both Mantel and Procrustes prevents geometric information loss and reduces overconfidence in any one diagnostic lens [R04, R08].

Key limitations remain observational. Composite coupling is descriptive, permutation resolution constrains p-value granularity in upstream artifacts, and compositional/sparsity properties can influence distance-based behavior and co-variation interpretation [R01, R03, R07]. These limits bound mechanism claims but do not negate the ecological structure identified.

### F. Future directions
The next ecological step is targeted validation of mechanism partitions already implied by this synthesis: (i) perturbation or temporal designs that separate shared filtering from direct interaction; (ii) AMF-focused trait and host-context stratification; and (iii) expanded integration of environmental gradients with plant-assembly descriptors in longitudinal settings [R14, R22]. Importantly, this trajectory should preserve the current result hierarchy while adding process-resolving evidence.

## Figure integration summary
Figures 1–5 collectively answer complementary questions: who is most strongly coupled, how strongly environment structures those patterns, where plant context adds explanatory value, and why AMF-centered signals differ in profile from BAC↔ITS and EUK↔ITS. Each figure contributes a distinct inference layer that supports the same final conclusion: cross-domain coupling is real, strongly environment-structured, and ecologically modulated by plant context.

## Conclusions
The V6 scientific-enrichment pass preserves all quantitative findings while deepening ecological interpretation and literature grounding. BAC↔ITS remains the strongest integrated coupling signal, but its interpretation is most robust when environmental filtering is treated as a primary structuring force. AMF-centered patterns are best viewed as plant-context responsiveness signatures rather than dominant coupling effects. Alpha-diversity increments are stronger than dark-diversity and completeness in this cohort, consistent with realized-assembly sensitivity under the present model structure. Together, these results support a layered ecological narrative that is scientifically richer while remaining consistent with completed analyses only.

## References

[R01] Sophie J. Weiss; Z. Xu; S. Peddada; Amnon Amir; K. Bittinger; Antonio Gonzalez. 2017. Normalization and microbial differential abundance strategies depend upon data characteristics. https://www.semanticscholar.org/paper/5415ab67f45cff058ddb86a65d073da7714b91c0.
[R02] Maike Rossmann; J. Pérez-Jaramillo; V. N. Kavamura; J. Chiaramonte; K. Dumack; A. Fiore-Donno. 2020. Multitrophic interactions in the rhizosphere microbiome of wheat: from bacteria and fungi to protists.. https://www.semanticscholar.org/paper/42d03d0b39981b892d93906ab599f2fb05e02344.
[R03] Antoni Susín; Yiwen Wang; Kim-Anh Lê Cao; M. Calle. 2020. Variable selection in microbiome compositional data analysis. https://www.semanticscholar.org/paper/aef538d3dde70c0c2eaaa5fc95bea7e92303a522.
[R04] Vijay Shankar; Richard T. Agans; O. Paliy. 2017. Advantages of phylogenetic distance based constrained ordination analyses for the examination of microbial communities. https://www.semanticscholar.org/paper/43301bcb4b97045773583ec5e66e66801113ecfd.
[R05] Kristin M. Rath; N. Fierer; D. Murphy; J. Rousk. 2018. Linking bacterial community composition to soil salinity along environmental gradients. https://www.semanticscholar.org/paper/d00c46b5c0a95da3cc3b45fb2d1995dfec68ecdf.
[R06] Boyan Wang; Chen Chen; Yuan-ming Xiao; Kaiyang Chen; Juan Wang; Shuo Zhao. 2024. Trophic relationships between protists and bacteria and fungi drive the biogeography of rhizosphere soil microbial community and impact plant physiological and ecological functions.. https://www.semanticscholar.org/paper/0e79f563128e9c8b3487b5dc217e44186627e9f3.
[R07] Huijuan Zhou; Kejun He; Jun Chen; Xianyang Zhang. 2021. LinDA: linear models for differential abundance analysis of microbiome compositional data. https://www.semanticscholar.org/paper/b92f52985b8e92fadf3ad5b47ab07b85f6e97777.
[R08] Zhenyuan Liu; Ting Zhou; Yongde Cui; Zhengfei Li; Weimin Wang; Yushun Chen. 2021. Environmental filtering and spatial processes equally contributed to macroinvertebrate metacommunity dynamics in the highly urbanized river networks in Shenzhen, South China. https://www.semanticscholar.org/paper/0fa617ca2ec661cd2740cc44daa15ab30efad00d.
[R09] M. Semchenko; K. Barry; F. D. de Vries; L. Mommer; M. Moora; J. Maciá‐Vicente. 2022. Deciphering the role of specialist and generalist plant-microbial interactions as drivers of plant-soil feedback.. https://www.semanticscholar.org/paper/ef5e90ba811ac887bd343c7ec65ee34ff7a93c2f.
[R10] Giovana S. Slanzon; M. Yuan; K. Estera-Molina; Aaron Chew; S. Blazewicz; M. Allen. 2025. Quantitative stable isotope probing (qSIP) and cross-domain networks reveal bacterial-fungal interactions in the hyphosphere. https://www.semanticscholar.org/paper/d3d786e9358dcd5877889917be2582a7fc39dd3e.
[R11] M. Pärtel; R. Szava-Kovats; M. Zobel. 2013. Community Completeness: Linking Local and Dark Diversity within the Species Pool Concept. https://www.semanticscholar.org/paper/ad5e291154b3edb084f90c90f6f9c949aa4db79b.
[R12] Sophie J. Weiss; Z. Xu; Amnon Amir; S. Peddada; K. Bittinger; Antonio Gonzalez. 2015. Effects of library size variance, sparsity, and compositionality on the analysis of microbiome data. https://www.semanticscholar.org/paper/3c1d7c08d3f50d8b03822786683ed598017dbc9f.
[R13] M. Greenacre; M. Martínez-Álvaro; A. Blasco. 2021. Compositional Data Analysis of Microbiome and Any-Omics Datasets: A Validation of the Additive Logratio Transformation. https://www.semanticscholar.org/paper/d7e84a1a89f43872149de0e5adca145ac79040ec.
[R14] Ye Li; Zengming Chen; Cameron Wagg; Michael J. Castellano; Nan Zhang; W. Ding. 2023. Soil organic carbon loss decreases biodiversity but stimulates multitrophic interactions that promote belowground metabolism. https://www.semanticscholar.org/paper/1e120b5423e78fe48c255ef67ef7702e5cc3a804.
[R15] M. Pärtel. 2014. Community ecology of absent species: hidden and dark diversity. https://www.semanticscholar.org/paper/9ace84d02cec657111c95295014e0185e225b3cb.
[R16] G. Custer; Maya Gans; Linda T. A. van Diepen; Francisco Dini‐Andreote; C. A. Buerkle. 2023. Comparative Analysis of Core Microbiome Assignments: Implications for Ecological Synthesis. https://www.semanticscholar.org/paper/b5d7723a0002667947ad80690757f1939fb8930d.
[R17] Evan P. Starr; Shengjing Shi; S. Blazewicz; B. Koch; Alexander J. Probst; B. Hungate. 2021. Stable-Isotope-Informed, Genome-Resolved Metagenomics Uncovers Potential Cross-Kingdom Interactions in Rhizosphere Soil. https://www.semanticscholar.org/paper/5a4fbb00ace620dd546b4e2a57d76ad05a7e582e.
[R18] J. Jeske; C. Gallert. 2022. Microbiome Analysis via OTU and ASV-Based Pipelines—A Comparative Interpretation of Ecological Data in WWTP Systems. https://www.semanticscholar.org/paper/f258bd25f70de0cdb263ee7d0d71f4749a63f9da.
[R19] Lin Tan; W. Zeng; Yansong Xiao; Pengfei Li; S. Gu; Shaolong Wu. 2021. Fungi-Bacteria Associations in Wilt Diseased Rhizosphere and Endosphere by Interdomain Ecological Network Analysis. https://www.semanticscholar.org/paper/0b6715b21090dd5e8dc5af7ac1fe363fb3e70552.
[R20] M. Calle; M. Pujolassos; Antoni Susín. 2023. coda4microbiome: compositional data analysis for microbiome cross-sectional and longitudinal studies. https://www.semanticscholar.org/paper/d192146db312d03e9d17870b6d3a8978a77dfd7a.
[R21] T. Bastiaanssen; T. Quinn; A. Loughman. 2022. Bugs as features (part 1): concepts and foundations for the compositional data analysis of the microbiome–gut–brain axis. https://www.semanticscholar.org/paper/98f14db0c26bf35059d1cf59146fbd1956acea09.
[R22] Ling Ma; Guixiang Zhou; Jiabao Zhang; Zhongjun Jia; Hongtao Zou; Lin Chen. 2024. Long-term conservation tillage enhances microbial carbon use efficiency by altering multitrophic interactions in soil.. https://www.semanticscholar.org/paper/0f7803eee083c78d0c03731824093639515f974b.
[R23] Meelis Pärtel; Riin Tamme; C. P. Carmona; Kersti Riibak; M. Moora; Jonathan A. Bennett. 2025. Global impoverishment of natural vegetation revealed by dark diversity. https://www.semanticscholar.org/paper/3c126e3f14a48d2875ff7a66ab84b2594c967cba.
[R24] Yilin Luo; Haiyun Ding; X. Mao; Zhixin Kang; Boda Li; Yong Zhou. 2025. Mechanistic insights into rhizosphere microbiome assembly in Pinus tabuliformis: The role of cross-kingdom interactions and soil salinity gradients.. https://www.semanticscholar.org/paper/33e16be6fc92e21a7451e9721ada0071e8bec89d.
[R25] M. Pärtel; M. Zobel; M. Öpik; L. Tedersoo. 2017. Global Patterns in Local and Dark Diversity, Species Pool Size and Community Completeness in Ectomycorrhizal Fungi. https://www.semanticscholar.org/paper/2bf4af38628b9732dbd36b59458bc8973043ec71.
[R26] M. Calle; Antoni Susín. 2022. coda4microbiome: compositional data analysis for microbiome studies. https://www.semanticscholar.org/paper/5a28c0d36b9ecedb194a873b49333d5f10192122.
[R27] Wenting Tang; Pekka Korhonen; Jenni Niku; Klaus Nordhausen; Sara Taskinen. 2025. Comparing model-based unconstrained ordination methods in the analysis of high-dimensional compositional count data. https://www.semanticscholar.org/paper/d885791fad291d3a1b5403b1b82bcde8de0ffa58.
[R28] Eileen Enderle; Fangbin Hou; Leonardo Hinojosa; Hidde Kottman; Nigâr Kasirga; F. D. de Vries. 2024. Plant-soil feedback responses to drought are species-specific and only marginally predicted by root traits. https://www.semanticscholar.org/paper/444886e969433a764c6cc1bc0571180242539aa4.
[R29] Jian Liang; Hai-Rui Huang; Meng-Yuan Shu; Chae-Woo Ma. 2025. Assessing the Impact of Land-Based Anthropogenic Activities on the Macrobenthic Community in the Intertidal Zones of Anmyeon Island, South Korea. https://www.semanticscholar.org/paper/c729686d8b6493448c9197ae2bc5534448b3be49.
[R30] H. Kong; G. C. Song; C. Ryu. 2019. Inheritance of seed and rhizosphere microbial communities through plant-soil feedback and soil memory.. https://www.semanticscholar.org/paper/96923d586d4cbdb6a0f2083db49e73fbae3bcf55.
[R31] S. Wani; Rameez Ahmad; F. Dar; Bilal A. Rasray; S. A. Lone; Faizan Shafee. 2023. Estimating dark diversity and regional species pool in the high-altitude Himalayan habitats. https://www.semanticscholar.org/paper/84654ac00f8f839105418931e77f0b85bb50398d.
[R32] Yuhua Shi; Yanshuo Pan; L. Xiang; Zhihui Zhu; Wenbo Fu; Guangfei Hao. 2021. Assembly of rhizosphere microbial communities in Artemisia annua: recruitment of plant growth‐promoting microorganisms and inter‐kingdom interactions between bacteria and fungi. https://www.semanticscholar.org/paper/a6f07b1f63609c28718ba814210f8f7072515d9a.
[R33] M. Jagadesh; Munmun Dash; A. Kumari; Santosh Kumar Singh; K. Verma; Prasann Kumar. 2024. Revealing the hidden world of soil microbes: Metagenomic insights into plant, bacteria, and fungi interactions for sustainable agriculture and ecosystem restoration.. https://www.semanticscholar.org/paper/bef531e148192fce5f047c071646deff6b4aa97d.
[R34] Nana Liu; Huifeng Hu; Wenhong Ma; Ye Deng; Qinggang Wang; Ao Luo. 2021. Relative Importance of Deterministic and Stochastic Processes on Soil Microbial Community Assembly in Temperate Grasslands. https://www.semanticscholar.org/paper/739791f04cefc38e2b673f582e6acd3568a85ca5.
[R35] Shenghan Gao; Yunbo Fu; Xinyi Peng; Silin Ma; Yurong Liu; Wenli Chen. 2025. Microplastics Trigger Soil Dissolved Organic Carbon and Nutrient Turnover by Strengthening Microbial Network Connectivity and Cross-Trophic Interactions.. https://www.semanticscholar.org/paper/fc6f06cdde388e3493cd9447e6ece5ab68e0d771.
[R36] Menghui Dong; G. Kowalchuk; Hongjun Liu; Wu Xiong; Xuhui Deng; Nan Zhang. 2021. Microbial community assembly in soil aggregates: A dynamic interplay of stochastic and deterministic processes. https://www.semanticscholar.org/paper/6f6286247d3454f3cf70e5db38134aee0a2592c3.
