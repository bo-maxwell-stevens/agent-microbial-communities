# Manuscript V16 Review Notes

## Objective
Final Results-only polish for submission readiness, with strict preservation of analytical outputs.

## Guardrails respected
- No re-analysis performed.
- No HPC jobs rerun.
- No scientific result files modified.
- No new hypotheses introduced.
- Non-Results sections preserved unchanged.

## Verification workflow

### A) Full-manuscript and scope checks
- Read full `manuscript_v15.md` before editing.
- Generated `manuscript_v16.md` by replacing Results section only.
- Verified section identity against V15:
  - INTRO_IDENTICAL = True
  - METHODS_IDENTICAL = True
  - DISCUSSION_IDENTICAL = True
  - CONCLUSIONS_IDENTICAL = True
  - FIGLEG_IDENTICAL = True
  - REF_IDENTICAL = True

### B) Quantitative verification against repository outputs
Repository outputs were inspected directly to confirm all retained V16 Results claims, including:
- coupling strengths and ranking structure,
- Mantel/Procrustes contrast,
- threshold robustness contrasts,
- environmental model structure and predictor dominance,
- plant-diversity increment patterns,
- integrated pair-level consistency.

A structured verification ledger was generated:
- `/tmp/v16_results_verification.json`

Key verified anchors used in V16 text:
- strongest coupling: BAC↔ITS presence/absence (0.574)
- coupling span across 12 combinations: 0.319–0.574
- strongest Mantel: BAC↔ITS presence/absence (ρ = 0.584, p = 0.002)
- strongest Procrustes: EUK↔ITS CLR (0.683)
- BAC↔ITS threshold stability: 0.597 (0.05), 0.571 (0.10)
- BAC↔EUK presence/absence weaker, least significant at conservative threshold (p = 0.018)
- environmental explained variation range (integrated pairs): 0.188–0.278 (mean 0.223)
- top environmental predictor consistency: pH_KCl across integrated entries
- geography sensitivity consistently positive
- AMF-linked plant-diversity gains > BAC↔ITS, approximately two-fold for AMF↔ITS vs BAC↔ITS in both representations

### C) Pair structure consistency verification
Verified pair identity/count structure from repository outputs:
- coupling-layer analyses include 6 pairs (12 pair×representation combinations)
- integrated environmental/plant/synthesis layers include 4 pairs (8 pair×representation combinations)
- V16 now states this distinction explicitly to avoid ambiguity.

### D) Repository filename language removal check
Automated scan of V16 Results confirmed:
- no `.csv` references,
- no `phase*` internal artifact names,
- no known prior internal filename tokens.

## Word counts
- Results words: 555 → 472
- Total manuscript words: 2750 → 2667

## Corrections log
- Numerical corrections: none required.
- Pair-count/data corrections: none required.
- Narrative clarification added for 6-pair coupling scope vs 4-pair integrated scope.

## Editorial readiness assessment (Results section)
- V16 Results are concise, biologically framed, and internally consistent with repository outputs.
- Recommended status: **freeze Results after V16** and move effort to Discussion and references.
