# Methods Change Log — V13

## Scope
- Source: `manuscript/manuscript_v12.md`
- Output: `manuscript/manuscript_v13.md`
- Scope-limited rewrite: **Methods only**
- Preserved unchanged: Results, Discussion, figures, references

## Reviewer-targeted updates applied
1. Expanded study-system description in Section 2.1 with DarkDivNet context, plot/region definitions, and plant-diversity metric provenance.
2. Explicitly defined prevalence filtering in Section 2.3 (taxa removed below 5% and 10% occurrence thresholds).
3. Replaced software-style phrasing with ecological/statistical reasoning in environmental-model and hypothesis text.
4. Added explicit rationale for alpha diversity, dark diversity, species pool, and completeness hypotheses in Section 2.6.
5. Removed unnecessary implementation-specific wording while retaining reproducibility-critical numeric parameters.
6. Preserved and clarified Mantel-Procrustes complementarity and the integrated score as a synthesis aid.

## Quantitative QA
- Methods word count (V12): 803
- Methods word count (V13): 1044
- Methods growth: 30.0%
- Total manuscript word count (V12): 3481
- Total manuscript word count (V13): 3722
- RESULTS_IDENTICAL: True
- DISCUSSION_IDENTICAL: True

## Reproducibility parameters preserved in Methods
- Prevalence thresholds: 0.05 and 0.10
- CLR pseudocount: 1×10⁻⁶
- Permutations: 999
- Procrustes bootstraps: 120
- Percentile interval summary: 2.5th–97.5th
- Integrated synthesis thresholds: coupling ≥0.50, env adj. R² ≥0.20, plant Δ adj. R² ≥0.01; low-plant <0.005

## Estimated Methods score (editorial, not inferential)
- Estimated before (V12): 8.0/10
- Estimated after (V13): 8.6/10
- Rationale: improved ecological framing, explicit prevalence definition, reduced software-like wording, and clearer plant-diversity hypothesis justification.
