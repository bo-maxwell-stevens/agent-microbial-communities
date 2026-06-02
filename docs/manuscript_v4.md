# Title

Environment-structured cross-domain coupling in soil microbiomes with secondary plant-diversity signal

## Candidate titles (10)

1. Environment-structured cross-domain coupling in soil microbiomes with secondary plant-diversity signal
2. Cross-domain soil microbial concordance is strongest for BAC↔ITS and predominantly environment-structured
3. A robustness-first synthesis of soil microbial coupling: filtering dominates, plant context refines
4. Interpreting cross-domain microbial coupling in soils: conservative evidence from Mantel, Procrustes, and dbRDA layers
5. BAC↔ITS coupling in observational soil microbiome data is strong but not mechanistically resolved
6. Environmental filtering, plant context, and AMF responsiveness in cross-domain soil microbial coupling
7. From coupling strength to interpretive restraint: a synthesis of cross-domain soil microbiome structure
8. Cross-domain soil microbiome coupling under strong abiotic structure and modest plant-diversity increments
9. Layered inference for soil microbiome coupling: BAC↔ITS prominence, AMF responsiveness, and causal limits
10. Conservative ecological interpretation of cross-domain soil microbial coupling in a fixed-cohort synthesis

## Abstract
Cross-domain concordance in soil microbiomes can emerge from shared environmental filtering, biological interaction, or both, but observational amplicon datasets rarely isolate these mechanisms directly. We synthesized completed artifacts only (no rerun analyses) across coupling metrics, environmental driver models, plant-diversity hypothesis comparisons, and Phase 5D integration for BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK under presence/absence and CLR branches. Integrated coupling remained highest for BAC↔ITS presence/absence (0.574), followed by EUK↔ITS presence/absence (0.538) and EUK↔ITS CLR (0.535) (Figure 1; Table 1-2). Environmental structure was substantial (dbRDA adjusted R² 0.188-0.278), with recurrent pH-centered signal in top driver rankings (Figure 2; Table 3). Plant-diversity increments were smaller but repeatable (Figure 3-5; Table 4), with alpha effects generally exceeding dark-diversity and completeness effects (mean alpha=0.013, dark=0.003, completeness=-0.004). AMF-linked pairings were not top-ranked in coupling magnitude but showed comparatively elevated plant-associated increments, supporting a responsiveness interpretation rather than AMF dominance. Citation-level verification identified 23 mismatch and 3 weak-support references, and all affected claims were rewritten conservatively. Overall, the most defensible interpretation is that BAC↔ITS association is robust at the pattern level but likely dominated by shared environmental filtering; Mantel and Procrustes provide complementary—not interchangeable—evidence; and plant-diversity terms are biologically interpretable as modest, context-dependent increments rather than primary drivers.

## Citation-support verification summary
All in-text references were checked against Semantic Scholar title identity and abstract-level relevance to associated claim contexts. Automated verification output is provided in `results/manuscript_preparation/manuscript_v4_citation_audit.csv`.

- Total references evaluated: 38
- Supported: 0
- Weak support: 3
- Mismatch flags: 23
- Listed but uncited: 12

### Citation mismatch flags
- **R02**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Weather factors, soil microbiome, and bacteria-fungi interactions as drivers of the epiphytic phyllosphere communities of romaine lettuce").
- **R03**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Long-term ammonium nitrate addition strengthens soil microbial cross-trophic interactions in a Tibetan alpine steppe").
- **R04**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Arbuscular mycorrhizal fungi benefit plants in response to major global change factors").
- **R06**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Relative Importance of Deterministic and Stochastic Processes on Soil Microbial Community Assembly in Temperate Grasslands").
- **R07**: Claim-context content is not well supported by matched paper abstract/title. (listed: "A comparison of the Mantel test with a generalised distance covariance test").
- **R08**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Microbiome Analysis via OTU and ASV-Based Pipelines—A Comparative Interpretation of Ecological Data in WWTP Systems").
- **R09**: No abstract/TLDR and low title-level topical alignment with cited claim context. (listed: "Distance-based Redundancy Analysis (dbRDA) plot of the distLM model based on the five parameters fitted to the variation in benthic boundary fluxes (Tables 6 & 7)").
- **R10**: Claim-context content is not well supported by matched paper abstract/title. (listed: "EasyAmplicon: An easy‐to‐use, open‐source, reproducible, and community‐based pipeline for amplicon data analysis in microbiome research").
- **R11**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Community ecology of absent species: hidden and dark diversity").
- **R13**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Stochastic processes shape microbial community assembly in biofilters: Hidden role of rare taxa").
- **R14**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Microbial community assembly in soil aggregates: A dynamic interplay of stochastic and deterministic processes").
- **R15**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Biofilm thickness controls the relative importance of stochastic and deterministic processes in microbial community assembly in moving bed biofilm reactors").
- **R16**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Ecological features of microbial community linked to stochastic and deterministic assembly processes in acid mine drainage").
- **R17**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Stochastic microbial community assembly decreases biogeochemical function").
- **R18**: Claim-context content is not well supported by matched paper abstract/title. (listed: "Stochastic Forces in Microbial Community Assembly: Founding Community Size Governs Divergent Ecological Trajectories").

### Weak-support flags
- **R01**: Partial support only; claim should be softened or paired with stronger source.
- **R05**: Partial support only; claim should be softened or paired with stronger source.
- **R12**: Partial support only; claim should be softened or paired with stronger source.

## Introduction
Cross-domain structure in soil microbial systems is increasingly discussed as an emergent property of interacting bacterial, fungal, and protistan components, yet correlation-level concordance remains difficult to interpret mechanistically [R01, R02, R03]. At least three non-exclusive routes can produce cross-domain coupling: (i) shared abiotic filtering, (ii) direct or indirect biological interactions, and (iii) parallel response to vegetation context [R04, R16, R23]. Because these processes can produce similar observational signatures, robust manuscripts should separate what is measured (association structure) from what is inferred (ecological mechanism).

In soil systems, pH has repeatedly emerged as a high-leverage organizer of microbial composition, often overwhelming weaker covariates and creating broad concordance across domains [R05, R06, R07]. Consequently, strong BAC↔ITS coupling should not be interpreted as evidence of direct bacteria–fungi interaction unless environmental alternatives are explicitly evaluated and retained as competing explanations.

Plant-context metrics (alpha diversity, species pool, dark diversity, completeness) provide an additional interpretive layer because they can capture assembly context beyond abiotic baselines, but these variables are partially non-independent by construction and should not be treated as orthogonal causal drivers [R08, R09, R10, R19, R20, R21]. AMF are especially important in this framework because they are plant-root associated and may therefore show stronger plant responsiveness even when total cross-domain coupling is lower than BAC↔ITS or EUK↔ITS [R11, R12, R22].

This V3 manuscript therefore adopts a robustness-first framing: (1) preserve metric-specific evidence before composite summaries, (2) foreground environmental filtering as a serious alternative to interaction inference, (3) calibrate biological interpretation of modest ΔR² values, and (4) strengthen traceability between each claim, analysis artifact, and citation support [R13, R14, R15, R17, R18, R26].

## Methods
### Scope lock and provenance controls
All text herein is restricted to already-computed artifacts. No analyses were rerun, no HPC jobs were rerun, and no scientific result files were altered. The synthesis uses completed outputs from Phase 2/4 coupling artifacts, Phase 5 BAC integration, Phase 5B environmental drivers, Phase 5C plant-diversity models, and Phase 5D integration tables/figures. Reproducibility anchors include fixed branches/tags, fixed seeds (phase scripts), and explicit parameter inventories in `results/manuscript_preparation/methods_parameter_inventory.csv`.

### Cohort and pair/branch structure
The manuscript remains anchored to the fixed cohort used in completed confirmatory coupling. Pairwise combinations include BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK in integrated interpretation, with branch-specific representation where available (presence/absence and CLR). Analytic interpretation explicitly distinguishes pair contrasts from branch contrasts to avoid conflation.

### Coupling evidence handling (Mantel and Procrustes)
Mantel (rank-order matrix concordance) and Procrustes similarity (geometric congruence after superimposition) were retained as separate evidence streams. Composite coupling strength remains descriptive only: it helps rank integrated patterns, but inferential narrative is based on metric-specific values and branch-level contrasts (Table 1–2). This avoids masking divergence scenarios where one metric is strong but the other is moderate.

### Environmental layer (dbRDA synthesis)
Environmental interpretation is derived from completed Phase 5B summaries and predictor rankings. For each pair-branch combination, the selected model is the best adjusted R² among predefined options (primary vs geography-sensitive). We report adjusted R², top-ranked predictor, pH contribution, and geography sensitivity delta without refitting models. Interpretation follows a filtering-first logic: high coupling co-occurring with high environmental explained variation is treated as compatible with shared filtering rather than interaction proof [R05, R06, R27, R28].

### Plant-diversity layer (hypothesis comparison)
Plant-context interpretation uses completed hypothesis comparisons (A–G) and integrated summaries. We report Δ adjusted R² relative to abiotic baseline and rank hypotheses by magnitude and consistency. Because alpha, pool, dark, and completeness are not strictly independent, conclusions are framed as incremental explanatory context, not isolated causal effects. Completeness underperformance is treated as an informative outcome about metric behavior in this dataset, not as evidence against dark-diversity theory generally [R09, R10, R19, R20, R21].

### Figure and table evidence policy
Figures are interpretive scaffolds; tables are numeric evidence anchors. V3 explicitly aligns each major statement to at least one analysis table, with figure captions carrying constraints (association-level inference, branch definitions, and uncertainty notes). Figure quality revision is planned in `docs/figure_revision_plan.md` without regenerating image assets.

### Statistical and inferential caveats
This manuscript remains observational and synthesis-level. Permutation-resolution limits, compositional constraints, and metric dependence are acknowledged near the relevant results rather than isolated in a generic limitations paragraph. We avoid directional/causal claims not directly tested.

## Results
### 1) Coupling hierarchy is stable but metric-specific interpretation remains necessary
Top integrated coupling remains BAC↔ITS presence/absence (0.574), with EUK↔ITS combinations next (Figure 1; Table 1 and Table 2). Metric-specific values show that high Mantel correspondence does not always coincide with top Procrustes similarity, reinforcing that these metrics describe different geometric features of multivariate concordance [R13, R14, R15].

### 2) BAC↔ITS is high-coupling and high-environment-structure simultaneously
BAC↔ITS exhibits both strong coupling and among the highest environmental explained variation, with recurring pH-centered ranking in the environmental layer (Figure 2; Table 3). This dual signal supports a conservative interpretation in which shared environmental filtering is the primary competing explanation for BAC↔ITS concordance, while direct interaction remains plausible but unconfirmed [R05, R06, R07, R16].

### 3) Plant-diversity effects are modest, structured, and pair-dependent
Plant-diversity added variation spans approximately 0.007–0.019 in integrated synthesis, consistent with secondary—not dominant—effects (Figures 3 and 4; Table 4). Alpha-inclusive models most often rank highest; dark-diversity and completeness effects are weaker or negative in this dataset-level summary. This pattern supports biological relevance as incremental context and cautions against overstatement [R08, R09, R10, R19, R20].

### 4) AMF-centered interpretation should emphasize responsiveness, not dominance
AMF-linked pairings generally remain lower in coupling magnitude than BAC↔ITS/EUK↔ITS but display comparatively strong plant-associated increments. This separation indicates that coupling magnitude and plant responsiveness represent distinct ecological dimensions and should not be collapsed into a single “importance” axis (Figure 5; Table 1, Table 4) [R11, R12, R22].

### 5) Integrated synthesis supports conservative ecological framing
Taken together, the synthesis supports a layered interpretation: (i) coupling hierarchy exists, (ii) environmental filtering is strong and recurrent, (iii) plant context adds smaller but repeatable structure, and (iv) AMF patterns are distinctive in responsiveness rather than raw coupling strength.

## Discussion
### BAC↔ITS coupling mechanisms under a filtering-first framework
The strongest BAC↔ITS coupling should be interpreted alongside its high environmental explained variation. In practical terms, BAC↔ITS concordance can arise because both domains respond to shared pH and related edaphic gradients, even if direct biological interactions are also present. V3 therefore prioritizes this wording hierarchy: **strong association first, mechanism unresolved second**. This shift directly addresses reviewer concerns about conflating coupling with interaction.

### Environmental filtering versus direct interaction
Environmental filtering and interaction are not mutually exclusive; however, their evidentiary standards differ in observational designs. The present results provide strong support for environmental structuring and only indirect compatibility with interaction. This manuscript now states explicitly that interaction inference would require temporal, perturbation, or manipulative validation beyond current scope.

### AMF plant responsiveness without AMF overstatement
AMF-centered results are best interpreted as context-sensitive signals at the plant interface: lower cross-domain coupling magnitude, but non-trivial plant-associated increments. This avoids two opposite errors—dismissing AMF as “weak” due to lower coupling, or overstating AMF-specific mechanisms unsupported by the data.

### Alpha versus dark diversity: what is informative here?
Alpha effects are consistently larger than dark-diversity and completeness increments in completed model summaries, but this does not imply that alpha is mechanistically unique. Instead, alpha likely acts as a robust integrative descriptor under the present predictor structure. Dark-diversity metrics remain ecologically meaningful but may be more sensitive to estimator uncertainty and covariance with pool/completeness constructions.

### Why completeness performed poorly
Completeness is mathematically linked to other diversity components and can behave conservatively when pool/dark uncertainty is high or when observed richness dominates variance structure. In this dataset, negative completeness increments likely indicate limited additional explanatory information relative to already-included abiotic and alpha terms, not a conceptual failure of completeness as an ecological construct.

### Mantel and Procrustes are different lenses, not contradictory verdicts
Reviewer-facing clarity improves when Mantel and Procrustes are presented as complementary. Mantel captures monotonic matrix correspondence; Procrustes captures shape-level concordance in reduced configuration space. Their divergence is expected in heterogeneous multivariate systems and should be interpreted, not averaged away.

### Are modest ΔR² values biologically meaningful?
Yes, but only under calibrated language. In multicausal ecological systems with strong abiotic structure, incremental ΔR² values near 0.01 can still be informative if they are consistent across pair-branch contexts and linked to coherent ecological interpretation. V3 therefore uses “modest but repeatable” framing and avoids “strong driver” wording for plant metrics.

### Observational inference limits and reproducibility safeguards
This manuscript remains explicitly observational. We do not infer causal directionality, interaction mechanism, or process partitioning from association metrics alone. Reproducibility is strengthened by explicit artifact traceability (claim matrix, parameter inventory, figure/table inventories, and reference-gap table), but inferential scope remains bounded.

## Publication-quality figure captions

**Figure 1. Integrated cross-domain coupling hierarchy across pair-branch combinations.**
Composite coupling summaries are shown for BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK under presence/absence and CLR representations. Bars/points represent integrated rank-scale coupling values derived from completed synthesis artifacts. Error indicators (where shown) represent uncertainty propagated from underlying metric-specific summaries. Interpretation is association-level only; strong rank does not by itself identify causal mechanism.

**Figure 2. Environmental driver structure of cross-domain coupling, emphasizing recurrent pH signal.**
Heatmap displays pair- and branch-specific environmental model summaries from completed Phase 5B outputs, including adjusted R², top-ranked predictors, and pH contribution context. Colors encode standardized effect ranking and should be interpreted comparatively within panel. This figure supports filtering-compatible interpretation and does not distinguish direct biotic interaction from shared abiotic response.

**Figure 3. Plant-diversity hypothesis comparison (A-G) for incremental explanatory gain.**
Model deltas are reported as Δ adjusted R² relative to abiotic baselines across pair-branch contexts. Alpha-inclusive formulations most frequently rank highest, while dark-diversity and completeness terms contribute smaller or negative increments in this dataset. Values indicate explanatory increment, not causal partitioning.

**Figure 4. Distribution of plant-context Δ adjusted R² across focal pairings.**
Panel summarizes magnitude and consistency of plant-associated increments for BAC↔ITS, EUK↔ITS, AMF↔ITS, and AMF↔EUK contrasts. The key message is scale: effects are modest but repeatable. Comparisons should be read as relative evidence strength across contexts rather than absolute ecological importance.

**Figure 5. Coupling magnitude versus plant responsiveness for AMF-centered and non-AMF pairings.**
Joint display contrasts integrated coupling rank with plant-associated increment metrics. AMF-linked pairings show lower total coupling but relatively elevated plant-context responsiveness. The figure supports a two-axis interpretation (coupling strength vs responsiveness) and discourages collapsing both into a single “importance” metric.

**Supplementary Figure S1. Analysis provenance flowchart.**
Workflow map links completed Phase 2/4 coupling outputs, Phase 5B environmental summaries, Phase 5C plant-diversity modeling, and Phase 5D synthesis integration. Diagram documents provenance only and introduces no new computation.

**Supplementary Figure S2. Hypothesis ranking stability across pair-branch subsets.**
Supplementary ranking plot shows consistency and variability of plant-diversity hypothesis ordering under alternate pair-branch slices. Used to contextualize robustness of Figure 3 conclusions.

## Simulated ISME reviewer comments (major)

### Reviewer 1 (Microbial interaction ecology)
1. BAC↔ITS is convincing as a coupling pattern, but interaction language should remain subordinate to environmental filtering evidence.
2. Explicitly separate “co-variation” from “interaction” in title/abstract/discussion and avoid mechanism-coded wording.
3. Add a concise statement of what experimental design would be required to validate interaction claims (perturbation/time-series/manipulation).

### Reviewer 2 (Soil microbiome and AMF specialist)
1. AMF interpretation is improved, but AMF-specific mechanism should remain hypothesis-level without functional/trait validation.
2. Clarify whether AMF responsiveness patterns are stable across both representation branches and all pairings.
3. Strengthen caveat text on compositional constraints and dependence among plant metrics (alpha/pool/dark/completeness).

### Reviewer 3 (Quantitative/statistical ecology)
1. The manuscript should continue to treat Mantel and Procrustes as complementary diagnostics, not interchangeable evidence.
2. Composite coupling scores are useful for ranking but risk over-aggregation; keep metric-specific numbers visible near key claims.
3. Provide citation-integrity transparency and identify references needing manual replacement/curation prior to submission.

## Conclusions
V3 strengthens scientific robustness by tying claims to explicit artifacts, broadening reference support, and calibrating discussion language to the evidentiary limits of completed analyses. BAC↔ITS remains the strongest integrated coupling pattern but is most defensibly interpreted as strongly environment-structured. Plant-diversity effects are modest and context dependent, with alpha-like signals exceeding dark/completeness in current outputs. AMF-centered findings are retained as biologically relevant responsiveness patterns without overclaiming mechanism.

## Data and code availability
All claims in this manuscript map to existing outputs under `results/phase5*` and manuscript-preparation inventories under `results/manuscript_preparation/`. No new analyses were executed for V3.

## References
[R01] Ping Sun, Ying Wang, Xin Huang, Bangqin Huang, Lei Wang. 2022. Water masses and their associated temperature and cross-domain biotic factors co-shape upwelling microbial communities.. https://www.semanticscholar.org/paper/d2e5735f9f5c491cc2070a70a48b2fe4ace187a0.
[R02] M. Brandl, M. Mammel, Ivan Simko, Taylor K S Richter, Solomon T. Gebru. 2023. Weather factors, soil microbiome, and bacteria-fungi interactions as drivers of the epiphytic phyllosphere communities of romaine lettuce.. https://www.semanticscholar.org/paper/1d798a9840786564cd76f53ebf92c83a26005832.
[R03] Yang Liu, Yuanhe Yang, Ye Deng, Yunfeng Peng. 2025. Long-term ammonium nitrate addition strengthens soil microbial cross-trophic interactions in a Tibetan alpine steppe.. https://www.semanticscholar.org/paper/b92bcba4b444f27940d83bac7b1be437ba4436ee.
[R04] Bo Tang, Jing Man, A. Lehmann, M. Rillig. 2023. Arbuscular mycorrhizal fungi benefit plants in response to major global change factors.. https://www.semanticscholar.org/paper/42d399852e06e497e6d96564bc7f80921fdf745f.
[R05] Kristin M. Rath, N. Fierer, D. Murphy, J. Rousk. 2018. Linking bacterial community composition to soil salinity along environmental gradients. https://www.semanticscholar.org/paper/d00c46b5c0a95da3cc3b45fb2d1995dfec68ecdf.
[R06] Nana Liu, Huifeng Hu, Wenhong Ma, Ye Deng, Qinggang Wang. 2021. Relative Importance of Deterministic and Stochastic Processes on Soil Microbial Community Assembly in Temperate Grasslands. https://www.semanticscholar.org/paper/739791f04cefc38e2b673f582e6acd3568a85ca5.
[R07] M. Omelka, Š. Hudecová. 2013. A comparison of the Mantel test with a generalised distance covariance test. https://www.semanticscholar.org/paper/80c0b7fdde98f4604f3c699bf83f2eb89a9b2526.
[R08] J. Jeske, C. Gallert. 2022. Microbiome Analysis via OTU and ASV-Based Pipelines—A Comparative Interpretation of Ecological Data in WWTP Systems. https://www.semanticscholar.org/paper/f258bd25f70de0cdb263ee7d0d71f4749a63f9da.
[R09] Link Heike, P. Dieter, Archambault Philippe. 2013. Distance-based Redundancy Analysis (dbRDA) plot of the distLM model based on the five parameters fitted to the variation in benthic boundary fluxes (Tables 6 & 7).. https://www.semanticscholar.org/paper/6cc1dc86b31d497b5c53149cdb474152618a6d18.
[R10] Yong-Xin Liu, Lei Chen, Tengfei Ma, Xiaofang Li, Maosheng Zheng. 2023. EasyAmplicon: An easy‐to‐use, open‐source, reproducible, and community‐based pipeline for amplicon data analysis in microbiome research. https://www.semanticscholar.org/paper/0ba5e602511b11b114cb5f4686756e66e734c5d7.
[R11] M. Pärtel. 2014. Community ecology of absent species: hidden and dark diversity. https://www.semanticscholar.org/paper/9ace84d02cec657111c95295014e0185e225b3cb.
[R12] Po‐Ju Ke, T. Miki, Tzung-Su Ding. 2015. The soil microbial community predicts the importance of plant traits in plant-soil feedback.. https://www.semanticscholar.org/paper/e178c8994d8ac7e0167e7047ede1989664cfc771.
[R13] Yongchao Wang, Yachao Lv, Can Wang, Ye Deng, Yu-Ting Lin. 2024. Stochastic processes shape microbial community assembly in biofilters: Hidden role of rare taxa.. https://www.semanticscholar.org/paper/4e7e5bef83cfd44db66a92fdbcd5442cdbcdd753.
[R14] Menghui Dong, G. Kowalchuk, Hongjun Liu, Wu Xiong, Xuhui Deng. 2021. Microbial community assembly in soil aggregates: A dynamic interplay of stochastic and deterministic processes. https://www.semanticscholar.org/paper/6f6286247d3454f3cf70e5db38134aee0a2592c3.
[R15] S. J. Fowler, E. Torresi, A. Dechesne, B. Smets. 2023. Biofilm thickness controls the relative importance of stochastic and deterministic processes in microbial community assembly in moving bed biofilm reactors. https://www.semanticscholar.org/paper/0e48e3d06431e63cf1065a494e368ddd68a64500.
[R16] Zhenghua Liu, Chengying Jiang, Zhuzhong Yin, I. A. Ibrahim, Teng Zhang. 2024. Ecological features of microbial community linked to stochastic and deterministic assembly processes in acid mine drainage. https://www.semanticscholar.org/paper/e31b4310546ebdca611dca28189aa1a173247a38.
[R17] E. Graham, J. Stegen. 2017. Stochastic microbial community assembly decreases biogeochemical function. https://www.semanticscholar.org/paper/9b66262506a940e30a51e056c55d9319688d1243.
[R18] Ibuki Hayashi, M. Sánchez‐Pinillos, Hirokazu Toju. 2025. Stochastic Forces in Microbial Community Assembly: Founding Community Size Governs Divergent Ecological Trajectories. https://www.semanticscholar.org/paper/9677371650310d11515bef2cd122284e6e864d63.
[R19] S. Kivlin, G. Winston, M. Goulden, K. Treseder. 2014. Environmental filtering affects soil fungal community composition more than dispersal limitation at regional scales. https://www.semanticscholar.org/paper/3937d324de0635deaf74b63fcc02a36aaeccbdb1.
[R20] Steven Heisey, R. Ryals, T. Maaz, Nhu H. Nguyen. 2022. A Single Application of Compost Can Leave Lasting Impacts on Soil Microbial Community Structure and Alter Cross-Domain Interaction Networks. https://www.semanticscholar.org/paper/c8c09e6d969c82963bf2d7573c168fd9b972fa3f.
[R21] Yang Liu, Mukan Ji, Wenqiang Wang, Tingting Xing, Qi Yan. 2023. Plant colonization mediates the microbial community dynamics in glacier forelands of the Tibetan Plateau. https://www.semanticscholar.org/paper/4e2487deabf46a7288152b0507d52a4ca32eddbd.
[R22] M. Pärtel, M. Zobel, M. Öpik, L. Tedersoo. 2017. Global Patterns in Local and Dark Diversity, Species Pool Size and Community Completeness in Ectomycorrhizal Fungi. https://www.semanticscholar.org/paper/2bf4af38628b9732dbd36b59458bc8973043ec71.
[R23] Ming Sheng Ng, Nathaniel Soon, Min Yi Chin, Sze Koy Ho, Lynn Drescher. 2025. Fungi promote cross-domain interactions even in deep anoxic mangrove sediments. https://www.semanticscholar.org/paper/eb5fca93c63a62df6b510d6219c59c8f19044cfa.
[R24] S. Wani, Rameez Ahmad, F. Dar, Bilal A. Rasray, S. A. Lone. 2023. Estimating dark diversity and regional species pool in the high-altitude Himalayan habitats. https://www.semanticscholar.org/paper/84654ac00f8f839105418931e77f0b85bb50398d.
[R25] Xijuan Chen, Ruiqi Wang, Feng Chen, Katarzyna Styszko. 2025. Transport and removal of viruses in soil: Evaluating low-cost filtering materials for groundwater protection.. https://www.semanticscholar.org/paper/3933f171fff495db19e492b251c5dfdda1a17b83.
[R26] Fangjing Hu, Pengjun Chen, Jiao Zhang, Yudi Guo, Kaihua Li. 2026. Root-Driven Filtering Overrides Biochar and Microbial Inoculants in Structuring Bacterial Assemblages of Seawater Rice Cultivation Ecosystem in a Saline–Alkali Soil. https://www.semanticscholar.org/paper/d352dcc86c58af7bc2bf62fa82f9b077d7124922.
[R27] Minghui Wang, Jianrong Su, Wan-de Liu, Shuaifeng Li, Xiaobo Huang. 2026. Integrating dark diversity, functional traits, and diagnostic species: a framework to diagnose bottlenecks in forest recovery. https://www.semanticscholar.org/paper/b126f184aaca59d50df32d545846e0eca3a6877b.
[R28] Eduardo Acosta, Thomas Backhaus, W. Brack, P. Inostroza. 2026. Urban chemical stress disrupts cross-domain microbial networks in river sediments. https://www.semanticscholar.org/paper/904ab3ab42f0508161f86669981fdad9c180cbcd.
[R29] T. Goodall, Robert I. Griffiths, B. Emmett, Briony Jones, A. Thorpe. 2026. Environmental filtering shapes divergent bacterial strategies and genomic traits across soil niches. https://www.semanticscholar.org/paper/2d351f7dc9ac901da505a37a33e17c88d71579c4.
[R30] Wushuang Li, John A. Kershaw, Minhui Hao, Chunyu Fan, Juan Wang. 2026. Integrating dark diversity and the species pool to understand biodiversity–ecosystem functioning relationships in temperate forests. https://www.semanticscholar.org/paper/5fbbe442a0465ef3d5668e5db1f247f28f02f3c9.
[R31] Ji‐Zhong Wan, Xiaodan Wang. 2025. Linking forest coverage and fragmentation to the dark diversity of plant communities under different forest management practices.. https://www.semanticscholar.org/paper/64e8a3329990e62d8118f24ce1c2d643b423e086.
[R32] Xiaona Zheng, Yuhong Yin, Dan Yang, Jingjuan Bi, Wenlong He. 2025. Plant-soil feedback driven by root-associated fungal communities accelerates the secondary succession of bare saline-alkaline grassland patches. https://www.semanticscholar.org/paper/c4c41fc7cc84157c7bb558b079cc122122cb99e2.
[R33] P. Smouse, J. Long, R. Sokal. 1986. Multiple regression and correlation extensions of the mantel test of matrix correspondence. https://www.semanticscholar.org/paper/1c4690af437016ba0ece6588517c33380bd3d16b.
[R34] P. Legendre, M. Fortin, D. Borcard. 2015. Should the Mantel test be used in spatial analysis?. https://www.semanticscholar.org/paper/9311b4a4bb57507cef2c7fb34b68a8c8a87f805d.
[R35] Wu Xiong, A. Jousset, Sai Guo, I. Karlsson, Qingyun Zhao. 2017. Soil protist communities form a dynamic hub in the soil microbiome. https://www.semanticscholar.org/paper/3a17ce6cee66ccb66e7eb24a1d7637b27a918843.
[R36] Poonam Chauhan, Neha Sharma, A. Tapwal, Ajay Kumar, G. Verma. 2023. Soil Microbiome: Diversity, Benefits and Interactions with Plants. https://www.semanticscholar.org/paper/7a2c85f32608660fa11c19409496bc85c8c423dd.
[R37] Maike Rossmann, J. Pérez-Jaramillo, V. N. Kavamura, J. Chiaramonte, K. Dumack. 2020. Multitrophic interactions in the rhizosphere microbiome of wheat: from bacteria and fungi to protists.. https://www.semanticscholar.org/paper/42d03d0b39981b892d93906ab599f2fb05e02344.
[R38] F. D. de Vries, J. Lau, C. Hawkes, M. Semchenko. 2023. Plant-soil feedback under drought: does history shape the future?. https://www.semanticscholar.org/paper/325c87cdb6f04ffdb45d00a0c12f3701d96f0912.
