# manuscript_v14_review_notes

## Verification procedure
- Audited every quantitative statement in the V14 Results against repository outputs before finalizing text.
- Cross-checked coupling, environmental, plant-diversity, and integrated synthesis values against committed CSV outputs.
- Did not rerun analyses, HPC jobs, or modify any scientific result files.

## Numerical corrections and consistency checks
1. Plant-diversity source consistency corrected
   - In V13, pair-level B-model delta values were described as extracted from phase5c_model_comparison.csv, but the reported numbers matched synthesis-level outputs (final_plant_diversity_summary.csv and final_pair_synthesis.csv) rather than geography-sensitivity deltas from phase5c_model_comparison.csv.
   - Geography-sensitivity B deltas in phase5c_model_comparison.csv are:
     - BAC↔ITS CLR 0.00840
     - BAC↔ITS presence/absence 0.01140
     - EUK↔ITS CLR 0.01549
     - EUK↔ITS presence/absence 0.01443
     - AMF↔ITS CLR 0.01826
     - AMF↔ITS presence/absence 0.02194
     - AMF↔EUK CLR 0.01490
     - AMF↔EUK presence/absence 0.01947
   - V14 resolves this by using pair-level plant increments from final synthesis tables for Results-layer comparisons and keeping hypothesis-level means from phase5c_hypothesis_summary.csv.

2. Coupling/environment/integration numbers verified
   - No additional numeric mismatches were found in the V14 Results text after verification against:
     - final_coupling_rankings.csv
     - phase5_bac_rank_summary.csv
     - phase5_bac_mantel_inference.csv
     - final_environment_driver_summary.csv
     - phase5b_dbRDA_summary.csv
     - phase5b_pair_rankings.csv
     - phase5c_hypothesis_summary.csv
     - final_plant_diversity_summary.csv
     - final_pair_synthesis.csv

## Figure integration checks
- Fig. 2 introduced with coupling hierarchy and Mantel/Procrustes divergence.
- Fig. 3 introduced with environmental dbRDA patterns and pH/geography structure.
- Fig. 4 introduced with plant-diversity hypothesis and pair-level increments.
- Fig. 5 introduced with cross-layer integrated contrast.

## Word count report
- Results word count: 1095 (V13) → 640 (V14)
- Total manuscript word count: 3303 (V13) → 2848 (V14)
