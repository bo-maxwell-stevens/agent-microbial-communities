# Project Overview

This repository contains multi-marker microbial community inputs and analysis workflows.

## Sequencing primers and read setups

- AMF: `WANDA/AML2`
- 16S (2x250): `515F (GTGYCAGCMGCCGCGGTAA)` / `926R (CCGYCAATTYMTTTRAGTTT)`
- General 18S (2x250): `Euk575F (ASCYGYGGTAAYWCCAGC)` / `Euk895R (TCHNHGNATTTCACCNCT)`
- ITS (PacBio, amplicon ~780 bp): `ITS9mun (TGTACACACCGCCCGTCG)` / `ITS4ngsUni (TCCTSCGCTTATTGATATGC)`
- trnL (2x150): `trnLg (GGGCAATCCTGAGCCAA)` / `trnLh (CCATTGAGTCTCTGCACCTATC)`

## Study metadata coverage

The `Final_data_with_diversity_prefixed.csv` table includes plant diversity metrics, soil chemistry, human footprint, climate covariates, and coordinates for integration with marker tables.

## Input files in `data/`

- `AMF_OTU_table_final.tsv`
  - Description: AMF abundance matrix (sample-by-feature) for arbuscular mycorrhizal fungi.
  - Shape: 120 data rows × 387 columns
  - Size: 187.85 KB
- `AMF_feature_metadata.tsv`
  - Description: Feature annotation for AMF abundance columns.
  - Shape: 386 data rows × 1 columns
  - Size: 3.24 KB
- `BAC_OTU_table_final.tsv`
  - Description: Bacterial abundance matrix (sample-by-feature) for 16S-derived taxa.
  - Shape: 140 data rows × 291700 columns
  - Size: 80.61 MB
- `BAC_feature_metadata.tsv`
  - Description: Feature annotation for BAC abundance columns.
  - Shape: 291699 data rows × 2 columns
  - Size: 27.91 MB
- `EUK_OTU_table_final.tsv`
  - Description: General eukaryotic abundance matrix (sample-by-feature) from 18S data.
  - Shape: 135 data rows × 58206 columns
  - Size: 15.51 MB
- `EUK_feature_metadata.tsv`
  - Description: Feature annotation for EUK abundance columns.
  - Shape: 58205 data rows × 2 columns
  - Size: 8.53 MB
- `Final_data_with_diversity_prefixed.csv`
  - Description: Canonical study metadata table with sample-level ecological and environmental variables used for cross-dataset integration.
  - Shape: 99 data rows × 103 columns
  - Size: 79.13 KB
- `ITS_OTU_table_final.tsv`
  - Description: ITS fungal abundance matrix (sample-by-feature).
  - Shape: 139 data rows × 26286 columns
  - Size: 7.36 MB
- `ITS_feature_metadata.tsv`
  - Description: Feature annotation for ITS abundance columns (taxonomic/SH metadata).
  - Shape: 26285 data rows × 19 columns
  - Size: 5.93 MB

## Reproducibility notes

- Raw inputs in `data/` are treated as read-only and are not modified by workflows.
- Derived outputs should be written to `results/` and narrative reports to `docs/`.
- Last updated: 2026-05-19 12:30 UTC
