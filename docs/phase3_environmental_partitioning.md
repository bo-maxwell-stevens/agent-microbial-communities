# Phase 3 Environmental Partitioning

## Objective
The Phase 3 workflow examines environmental and microbial associations using Mantel-style tests and residual coupling.

## Workflow Enhancements
1. **Improved Stability**:
   - Ridge regression addresses multicollinearity and singular matrices.
   - Missing values handled via mean imputation (`SimpleImputer`).
   - Additional stabilization using `np.nan_to_num`.
2. **Key Outputs**:
   - Residual Mantel Test Correlation: `-0.24135511154752032`
   - P-value: `5.141972430385509e-53`

## Output Files
- **Environmental Distance Results**: `results/phase3_environmental_partitioning/environmental_variable_inventory.csv`
- **Residual Mantel Outputs**: `results/phase3_environmental_partitioning/residual_mantel_results.txt`

## Exclusion Logic
Environmental predictors exclude microbial and taxonomic columns matching patterns or prefixes:
- Prefixes: `Bac_`, `Euk_`, `ITS_`, `AMF_`, `VTX`, `VT`, `OTU`, `ASV`
- Identifiers: `taxonomy`, `taxon`, `phylum`, `class`, `order`, `family`, `genus`, `species`

Legitimate environmental metadata are preserved (e.g., site and climate variables).

## Notes
- Warning for skipped features: Some features lack observed values and were skipped during imputation (e.g., Bac_Deinococcota).
- These warnings do not affect the overall integrity of the results.