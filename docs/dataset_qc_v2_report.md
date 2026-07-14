# Dataset QC v2 Report

- Generated: 2026-07-14T10:25:29.873981+00:00
- Git commit: `f3e7d8fd699c392decf6a244cbb9e0720e247e8c`
- Python: `3.12.3 (main, Jun 19 2026, 12:46:00) [GCC 13.3.0]`
- pandas: `3.0.3`

## 1) Sample harmonization audit

- Canonical union sample count: **143**
- Duplicate sample detection records (within tables): **0**
- Pairwise overlap matrix: `results/dataset_qc_v2/pairwise_overlap_matrix.csv`
- Canonical inventory: `results/dataset_qc_v2/canonical_sample_inventory.csv`
- Missing sample summary vs META: `results/dataset_qc_v2/missing_sample_summary.csv`
- Missing sample details vs META: `results/dataset_qc_v2/missing_sample_details.csv`

## 2) Sequencing depth and prevalence QC

- Zero-library sample records: **0**
- Library size summaries: `results/dataset_qc_v2/library_size_summary.csv`
- Taxon prevalence distributions: `results/dataset_qc_v2/taxon_prevalence_distribution.csv`
- Suggested filtering thresholds: `results/dataset_qc_v2/suggested_filtering_thresholds.csv`
- Richness summaries: `results/dataset_qc_v2/richness_summary.csv`

## 3) Reproducibility metadata

- Reproducibility metadata JSON: `results/dataset_qc_v2/reproducibility_metadata.json`
- Input file sizes: `results/dataset_qc_v2/input_file_sizes.csv`
- Parse warnings/errors: `results/dataset_qc_v2/parse_warnings_errors.csv`

## Parse diagnostics

Total warnings/errors: **1**

- WARNING [AMF] `/srv/hermes_projects/agent_microbial_communities/data/AMF_feature_metadata.tsv` — AMF feature metadata IDs has invalid IDs at row positions: 386
