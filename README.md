# Agent Microbial Communities

Fresh agent-oriented workspace for bacterial, AMF, ITS, and eukaryotic community analysis.

Raw data are stored locally in `data/` and are intentionally excluded from GitHub.

## Project overview

This repository supports integrated microbial community analyses across multiple marker datasets and associated ecological metadata.

- Main goals:
  - Harmonize sample IDs across datasets (AMF, BAC, EUK, ITS, metadata)
  - Run sequencing-depth and prevalence QC
  - Build reproducible, script-first ecological analysis workflows
- Reproducibility constraints:
  - Never modify raw input files in `data/`
  - Write derived outputs to `results/` and narrative summaries to `docs/`

## Input datasets (`data/`)

The following raw inputs are used by the workflow.

- `Final_data_with_diversity_prefixed.csv`
  - Ecological/sample-level metadata table (99 rows × 103 columns)
  - Includes canonical sample identifiers and diversity/environment variables used for downstream integration

- `AMF_OTU_table_final.tsv`
  - Arbuscular mycorrhizal fungi abundance table (120 rows × 387 columns)
  - Row-wise samples, with one sample-ID column plus AMF feature abundance columns

- `AMF_feature_metadata.tsv`
  - AMF feature annotation table (386 rows × 1 column)
  - Reference metadata for AMF features in the AMF abundance matrix

- `BAC_OTU_table_final.tsv`
  - Bacterial abundance table (140 rows × 291,700 columns)
  - Row-wise samples, with one sample-ID column plus bacterial feature abundance columns

- `BAC_feature_metadata.tsv`
  - Bacterial feature annotation table (291,699 rows × 2 columns)
  - Reference metadata for bacterial OTUs/features

- `EUK_OTU_table_final.tsv`
  - Eukaryotic abundance table (135 rows × 58,206 columns)
  - Row-wise samples, with one sample-ID column plus eukaryotic feature abundance columns

- `EUK_feature_metadata.tsv`
  - Eukaryotic feature annotation table (58,205 rows × 2 columns)
  - Reference metadata for eukaryotic OTUs/features

## Phase 2 Virtual Environment Requirement
Some scripts, such as `scripts/analysis/phase2_visualize_coupling.py` and `scripts/analysis/phase2_validate_outputs.py`, rely on the project's Python virtual environment for dependencies like `seaborn`, `matplotlib`, and `pandas`. To run these scripts:

```bash
cd /srv/hermes_projects/agent_microbial_communities
source venv/bin/activate
python3 scripts/analysis/phase2_validate_outputs.py
python3 scripts/analysis/phase2_visualize_coupling.py
```

Ensure the virtual environment is activated before executing these scripts for proper functionality.

If pip resolves to a different Python interpreter on your system, prefer uv pip or python -m pip to avoid installing packages into the wrong environment.

## Additional utility scripts
- `scripts/figures/regenerate_manuscript_figures.py` — Rebuilds manuscript figure set from existing analysis outputs.
- `scripts/literature/run_darkdivnet_literature_search.py` — Runs the DarkDivNet-focused literature retrieval workflow.
- `scripts/literature/summarize_darkdivnet_context.py` — Summarizes retrieved DarkDivNet literature context into project-ready notes.

