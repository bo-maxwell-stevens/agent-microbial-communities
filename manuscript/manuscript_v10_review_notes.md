# manuscript_v10 review notes

## Verification checklist
- [x] Methods rewritten into requested 7 journal-style sections.
- [x] Results rewritten and expanded with requested subsections 3.1–3.5.
- [x] Numerical values sourced from phase5 CSV outputs and synthesis tables.
- [x] No analysis reruns.
- [x] No output files modified under results/.
- [x] No new hypotheses introduced.

## Source-of-truth audit
- Coupling values and rankings: results/phase5d_synthesis/final_coupling_rankings.csv and results/phase5_bac_integration/phase5_bac_*.csv
- Environmental values: results/phase5d_synthesis/final_environment_driver_summary.csv, results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv, phase5b_predictor_ranking.csv
- Plant hypothesis values: results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv, phase5c_model_comparison.csv, phase5c_predictor_effects.csv, and synthesis plant summary
- Integration values: results/phase5d_synthesis/final_pair_synthesis.csv

## Notes for coauthor review
- docs/manuscript_v9.md did not exist at current commit; source manuscript read from manuscript/manuscript_v9.md.
- Results section is intentionally descriptive (rank/order/range emphasis) to keep interpretation centered in Discussion.
- If desired, a final pass can harmonize terminology for presence/absence formatting and decimal precision style across all sections.
