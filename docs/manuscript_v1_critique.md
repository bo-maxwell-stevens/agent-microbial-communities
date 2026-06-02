# Manuscript v1 Critical Scientific Review

Scope: Critical review of `docs/manuscript_v1.md` informed by companion artifacts (`manuscript_v1_review_notes`, `reviewer_simulation`, `discussion_outline`, `introduction_package`, `results_storyboard`, `phase5d_synthesis_summary`).

Reviewer lenses integrated:
- ISME Journal-style reviewer
- Microbial community ecologist
- AMF specialist
- Quantitative/statistical reviewer

## 1) Major strengths
- **Strong synthesis discipline and scope control** (Methods: *Study design and scope lock*): explicitly states no rerun analyses/HPC and keeps interpretation anchored to completed phases.
- **Good cross-phase integration** (Results sections 1–4): integrates coupling, environmental, and plant-diversity layers coherently.
- **Numerically grounded narrative** (Abstract/Results): major claims are supported with specific values (e.g., coupling rankings, adjusted R² ranges, delta adjusted R² effects).
- **Appropriate caution language appears in places** (Discussion): acknowledges correlative design, metric discordance risk, and threshold-label limitations.
- **AMF signal not erased despite lower coupling** (Results section 3): preserves AMF ecological relevance via plant-associated increments.

## 2) Major weaknesses
- **Introduction underdevelops mechanistic alternatives** (Introduction): environmental filtering vs biotic coupling is stated, but mechanistic framing is not fully developed for expected ISME-level skepticism.
- **Methods lacks operational detail needed for reproducibility audit** (Methods): synthesis provenance is described, but manuscript-level methods do not fully expose data-flow decisions, tie-breaking rules, and branch-wise selection edge cases.
- **Discussion currently too concise for high-impact journal standards** (Discussion): key tensions (Mantel vs Procrustes, AMF modest effect vs ecological importance, biological meaning of small delta adjusted R²) need deeper treatment.
- **Reference integration is functional but not yet rhetorically optimized** (Introduction/Discussion): some citations are listed but not fully tied to specific inferential boundaries.
- **Placeholder sections are not publication-ready** (Author contributions, Acknowledgements).

## 3) Missing interpretations
- **BAC↔ITS alternative explanation depth is insufficient** (Discussion): manuscript states environmental compatibility but does not fully partition interpretation into “shared filtering likely dominant” vs “possible residual biotic linkage.”
- **Mantel-Procrustes divergence is acknowledged but not interpreted ecologically** (Results section 1; Discussion): no explicit explanation of why matrix-correlation and geometric-concordance could diverge by branch.
- **Alpha-diversity signal non-independence interpretation is thin** (Results section 3; Discussion): needs explicit treatment of whether alpha is proxying broader plant community structure.
- **AMF lower coupling + higher plant-associated increment is not fully theorized** (Results section 3; Discussion): currently descriptive, not mechanistically framed.

## 4) Missing ecological context
- Need stronger positioning of **soil pH as broad assembly axis across domains** and what that implies for interpreting BAC↔ITS as interaction vs co-response (Introduction/Discussion).
- Need a clearer statement that **cross-domain coupling does not equal interaction** without perturbation or temporal evidence (Introduction/Discussion).
- Need explicit framing of **effect-size hierarchy** (environmental >> plant-diversity incremental terms) as a biological interpretation guardrail (Discussion).

## 5) Missing AMF-specific context
- AMF interpretation needs explicit caveat around **marker/resolution constraints** and taxonomic/ecophysiological heterogeneity (Discussion).
- Add clearer ecological framing for why AMF may show **lower global coupling but stronger plant-linked increments** (Discussion; tie to root-association ecology).
- Clarify boundaries of AMF conclusions to avoid broad claims beyond evaluated pairings (Results section 3; Conclusions).

## 6) Statistical concerns
- **Composite coupling strength averaging** (Methods; Results section 1): useful as summary, but manuscript should state the assumptions and risks of averaging unlike metrics.
- **No uncertainty propagation in the composite metric** (Results/Discussion): CIs are discussed for components but not translated into synthesis uncertainty language.
- **Thresholded interpretation labels** (Methods: *Synthesis labeling and interpretive constraints*): needs clearer reminder these are communication categories, not inferential cutoffs.
- **Potential predictor collinearity/non-independence** (Results section 3; Discussion): alpha/pool/dark/completeness relationships need explicit caveat in interpretation.
- **Permutation floor context** should be reiterated wherever p-values are interpreted (Methods/Results).

## 7) Figure concerns
- Current text references Figures 1–5, but narrative guidance for each figure is uneven; strongest for Figure 1 and weaker for Figures 4–5.
- Figure sequence should better mirror argument progression: metric divergence -> environmental filtering -> plant-additive context -> AMF nuance.
- Need explicit caption-level guardrails so Figure 1 does not visually imply causality for BAC↔ITS.

## 8) Table concerns
- Table roles are partially clear, but **Table 2 is not explicitly integrated in Results flow** (Results mostly references Tables 1, 3, 4).
- Table text should reinforce metric-specific vs composite interpretations (especially coupling tables).
- Supplementary tables are available but underleveraged in main-text defensibility (Results/Methods cross-references could be improved).

## 9) Overstatements
- Risk of overstatement in framing BAC↔ITS as “strongest coupled” without immediately co-emphasizing strong environmental structuring (Abstract, Conclusions).
- Risk of implying robust AMF-specific inference beyond effect size scale and marker constraints (Results section 3, Conclusions).
- Risk that “biologically relevant” language for ~0.01 delta adjusted R² appears stronger than evidence unless tightly qualified (Discussion).

## 10) Underdeveloped arguments
- Why **Mantel and Procrustes disagreement** matters for ecological interpretation and ranking confidence.
- Why **modest but consistent plant-diversity increments** can still be meaningful in complex ecological systems.
- Why AMF patterns might reflect **different coupling architecture** rather than weaker ecological role.

## 11) Sections needing expansion
- **Introduction**: deepen mechanism-framing and inferential boundaries.
- **Methods**: add transparent synthesis decision rules and uncertainty communication.
- **Discussion**: expand into a full interpretation hierarchy (environmental filtering first, plant context second, AMF nuance third, limitations/reproducibility fourth).
- **Data and code availability**: increase reproducibility detail (artifact map + minimal rerun recipe pointers for future coauthors/reviewers).

## 12) Sections needing shortening
- **Abstract**: compress repetitive caution phrasing and reserve detail for Discussion.
- **Results section 4**: reduce label-centric wording and focus on biological takeaways.
- **References annotations in prose**: streamline parenthetical metadata to journal style in later drafting pass.

## Cross-reviewer synthesis (bottom line)
- The manuscript is **scientifically promising and structurally coherent**, but requires a stronger Discussion and tighter inferential framing before coauthor circulation for journal-grade critique.
- Biggest scientific risk is **interpretive overreach relative to correlative synthesis design**, not numerical inconsistency.
