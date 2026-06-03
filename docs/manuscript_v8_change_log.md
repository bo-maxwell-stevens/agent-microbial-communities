# Manuscript V8 change log

## Scope
Targeted Figure 1 replacement only. No rerun analyses, no rerun HPC jobs, no modification of scientific result files, and no new hypotheses.

## Changes made
1. Removed the old workflow-style Figure 1 assets.
2. Replaced Figure 1 with a new global cohort/environmental-context figure using standard naming format (`Figure1_*`) consistent with other main figures.
3. Updated Panel A to use a world basemap under the sample coordinates.
4. Updated Panel C to include only alpha, dark, and pool (removed compl).
5. Regenerated Figure 1 source data, validation summary, and caption with matching `Figure1_*` naming.
6. Updated manuscript v8 text for the revised Figure 1 Panel C description.
7. Regenerated `manuscript/manuscript_v8.docx` from `manuscript/manuscript_v8.md`.

## Files created/updated
- `figures/main/Figure1_global_cohort_environmental_context.png`
- `figures/main/Figure1_global_cohort_environmental_context.svg`
- `figures/source_data/Figure1_global_cohort_environmental_context_source_data.csv`
- `figures/source_data/Figure1_global_cohort_environmental_context_validation_summary.csv`
- `figures/captions/Figure1_global_cohort_environmental_context.md`
- `scripts/figures/create_figure1_global_context.py`
- `manuscript/manuscript_v8.md`
- `manuscript/manuscript_v8.docx`
- `docs/manuscript_v8.md`
- `docs/manuscript_v8_change_log.md`

## Files removed
- `figures/main/Figure1_study_overview_workflow.png`
- `figures/main/Figure1_study_overview_workflow.svg`
- `figures/source_data/Figure1_workflow_overview.csv`
- `figures/captions/Figure1_study_overview_workflow.md`
- `figures/main/figure1_global_context.png`
- `figures/main/figure1_global_context.svg`
- `figures/source_data/figure1_global_context_source_data.csv`
- `figures/source_data/figure1_validation_summary.csv`
- `figures/captions/figure1_caption.md`
