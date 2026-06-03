# Manuscript V17 Review Notes

## 1) Verification protocol completed before edits
I read the full current manuscript (`manuscript_v16.md`) before editing and then verified Methods/Results numerical statements against committed repository outputs.

Primary verification artifacts used:
- `results/phase5d_synthesis/final_coupling_rankings.csv`
- `results/phase5d_synthesis/final_environment_driver_summary.csv`
- `results/phase5d_synthesis/final_plant_diversity_summary.csv`
- `results/phase5_bac_integration/phase5_bac_rank_summary.csv`
- `results/phase5_bac_integration/phase5_bac_mantel_inference.csv`
- `results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv`
- `results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv`
- `results/manuscript_preparation/methods_parameter_inventory.csv`

Machine-readable audit snapshot:
- `/tmp/v17_verification.json`

## 2) Key verified anchors used in V17 text
- Best coupling row: BAC↔ITS presence/absence, coupling `0.5740768828`, Mantel `0.5842070605`, `p=0.002`.
- EUK↔ITS coupling values: `0.5378532210` and `0.5352122895`.
- Coupling range: `0.3190034192–0.5740768828`.
- BAC↔ITS threshold robustness (Mantel): `0.5972515497` at 0.05 and `0.5711625713` at 0.10.
- BAC↔EUK at threshold 0.10: Mantel `0.1425007227`, `p=0.018`.
- Environmental adjusted R² range: `0.1881364249–0.2776637106`; mean `0.2227137059`.
- Geography sensitivity range: `0.0079546440–0.0218934528`.
- pH contribution range: `0.0919503027–0.1509953841`.
- Plant-diversity top increments: `0.0189834474`, `0.0171597305`, `0.0165046833`.
- BAC↔ITS plant increments: `0.0089288597` (presence/absence), `0.0073233570` (CLR).

All manuscript values remained aligned with these outputs after rounding where biologically non-material.

## 3) Consistency audit
### Sample size
- Abstract: `n=84` present.
- Methods: 84-site matched cohort stated.
- Results: Figure 1 cohort framing `n = 84` present.
- Conclusions: no contradictory value present.

### Pairs, representations, permutations, predictors, hypotheses
- Pair counts: 6 analyzed pairs overall; 4 carried into integrated synthesis.
- Representations: presence/absence + CLR (both consistently described).
- Permutations: 999 consistently stated for Mantel/dbRDA/model-comparison layers.
- Environmental predictors/geography sensitivity framing consistent with outputs.
- Plant-diversity model set A–G vs abiotic baseline consistent.

Consistency issues discovered and corrected: **none required**.

## 4) Scope-control checks
- Discussion unchanged.
- References unchanged.
- Figure captions unchanged.
- No scientific results files modified.
- No analyses rerun; no HPC jobs rerun.

## 5) Edit counts and word counts
- Numerical precision changes made: **8**
- Wording/readability improvements made: **7**

Word counts:
- Methods: **978 → 978**
- Results: **474 → 481**
- Total manuscript: **2682 → 2689**
