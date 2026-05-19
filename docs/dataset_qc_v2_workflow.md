# Dataset QC v2 Workflow

This workflow is implemented in `scripts/dataset_qc_v2.py` and run via:

```bash
./scripts/run_dataset_qc_v2.sh
```

## Scope

The workflow audits and summarizes five modalities:

- AMF
- BAC
- EUK
- ITS
- META (`Final_data_with_diversity_prefixed.csv`)

## Outputs

All machine-readable outputs are written to:

- `results/dataset_qc_v2/`

Primary markdown report:

- `docs/dataset_qc_v2_report.md`

## Harmonization audit outputs

- `pairwise_overlap_matrix.csv`
- `duplicate_sample_detection.csv`
- `missing_sample_summary.csv`
- `canonical_sample_inventory.csv`

## Sequencing depth and prevalence QC outputs

- `library_sizes_per_sample.csv`
- `library_size_summary.csv`
- `zero_library_samples.csv`
- `taxon_prevalence_distribution.csv`
- `taxon_prevalence_summary.csv`
- `suggested_filtering_thresholds.csv`
- `richness_per_sample.csv`
- `richness_summary.csv`

## Reproducibility metadata outputs

- `reproducibility_metadata.json`
- `reproducibility_metadata.csv`
- `input_file_sizes.csv`
- `parse_warnings_errors.csv`

## Notes

- Raw inputs are read-only and expected under `data/`.
- This workflow does not modify raw data.
- Empty/missing inputs are captured as parse warnings/errors and reflected in outputs.
