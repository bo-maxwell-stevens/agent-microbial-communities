# Agent Instructions

This repository is for agent-assisted microbial community analysis.

Rules:
- Do not commit `data/`.
- Do not delete or overwrite raw files in `data/`.
- Code, configs, documentation, tests, reports, and prompts may be created or modified.
- Prefer reproducible scripts over one-off notebooks.
- Write outputs to `results/`.
- Summarize major workflow changes in `docs/`.

Local data files expected:
- data/AMF_OTU_table_final.tsv
- data/AMF_feature_metadata.tsv
- data/BAC_OTU_table_final.tsv
- data/BAC_feature_metadata.tsv
- data/EUK_OTU_table_final.tsv
- data/EUK_feature_metadata.tsv
- data/ITS_OTU_table_final.tsv
- data/ITS_feature_metadata.tsv
- data/Final_data_with_diversity_prefixed.csv
