# FIGURE PACKAGE REPORT

## Scope
- Figure package generated from existing Phase 2, 5A, 5B, 5C, and 5D result tables only.
- No new analyses, no HPC jobs, no edits to scientific result files.

## Main figures
- Figure1_study_overview_workflow: figures/main/Figure1_study_overview_workflow.png | figures/main/Figure1_study_overview_workflow.svg (3600x2100 px at 300 dpi)
- Figure2_cross_domain_coupling_hierarchy: figures/main/Figure2_cross_domain_coupling_hierarchy.png | figures/main/Figure2_cross_domain_coupling_hierarchy.svg (3600x1740 px at 300 dpi)
- Figure3_environmental_driver_analysis: figures/main/Figure3_environmental_driver_analysis.png | figures/main/Figure3_environmental_driver_analysis.svg (3900x1740 px at 300 dpi)
- Figure4_plant_diversity_hypothesis_comparison: figures/main/Figure4_plant_diversity_hypothesis_comparison.png | figures/main/Figure4_plant_diversity_hypothesis_comparison.svg (3600x1740 px at 300 dpi)
- Figure5_integrated_ecological_synthesis_network: figures/main/Figure5_integrated_ecological_synthesis_network.png | figures/main/Figure5_integrated_ecological_synthesis_network.svg (2850x1950 px at 300 dpi)

## Supplemental figures
- FigureS1_mantel_only_visualization: figures/supplemental/FigureS1_mantel_only_visualization.png | figures/supplemental/FigureS1_mantel_only_visualization.svg (2700x1650 px at 300 dpi)
- FigureS2_procrustes_only_visualization: figures/supplemental/FigureS2_procrustes_only_visualization.png | figures/supplemental/FigureS2_procrustes_only_visualization.svg (2700x1650 px at 300 dpi)
- FigureS3_geography_sensitivity_comparison: figures/supplemental/FigureS3_geography_sensitivity_comparison.png | figures/supplemental/FigureS3_geography_sensitivity_comparison.svg (3000x1740 px at 300 dpi)

## Source result tables used
- results/phase2_confirmatory_coupling/phase2_coupling_summary.csv
- results/phase2_confirmatory_coupling/sample_cohort_used.csv
- results/phase5_bac_integration/phase5_bac_coupling_summary.csv
- results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv
- results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv
- results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv
- results/phase5c_plant_diversity/phase5c_model_comparison.csv
- results/phase5d_synthesis/final_coupling_rankings.csv
- results/phase5d_synthesis/final_environment_driver_summary.csv
- results/phase5d_synthesis/final_pair_synthesis.csv
- results/phase5d_synthesis/final_plant_diversity_summary.csv

## Source-data CSV exports
- figures/source_data/Figure1_workflow_overview.csv
- figures/source_data/Figure2_coupling_hierarchy.csv
- figures/source_data/Figure3_environmental_dbrda_summary.csv
- figures/source_data/Figure3_predictor_importance_heatmap.csv
- figures/source_data/Figure4_hypothesis_models_A_to_G.csv
- figures/source_data/Figure4_hypothesis_summary_A_to_G.csv
- figures/source_data/Figure5_integrated_synthesis_network_edges.csv
- figures/source_data/FigureS1_mantel_only.csv
- figures/source_data/FigureS2_procrustes_only.csv
- figures/source_data/FigureS3_geography_sensitivity_comparison.csv

## Caption files
- figures/captions/Figure1_study_overview_workflow.md
- figures/captions/Figure2_cross_domain_coupling_hierarchy.md
- figures/captions/Figure3_environmental_driver_analysis.md
- figures/captions/Figure4_plant_diversity_hypothesis_comparison.md
- figures/captions/Figure5_integrated_ecological_synthesis_network.md
- figures/captions/FigureS1_mantel_only_visualization.md
- figures/captions/FigureS2_procrustes_only_visualization.md
- figures/captions/FigureS3_geography_sensitivity_comparison.md

## Figure interpretation and placement
- Figure 1 (Main): workflow context and data lineage for manuscript figures.
- Figure 2 (Main): hierarchical cross-domain coupling and Mantel–Procrustes concordance.
- Figure 3 (Main): environmental explained variation with predictor-importance heatmap.
- Figure 4 (Main): A–G plant-diversity hypothesis comparison across pairings.
- Figure 5 (Main): integrated ecological synthesis network from Phase 5D summaries.
- Figure S1 (Supplement): Mantel-only detail view with confidence intervals.
- Figure S2 (Supplement): Procrustes-only detail view with confidence intervals.
- Figure S3 (Supplement): geography sensitivity vs primary dbRDA comparison.

## Validation
- All PNG files valid signature: **True**
- All SVG files XML-parseable: **True**
- Source-data CSV count: **10**
- Caption markdown count: **8**

Validation detail:
- Figure1_study_overview_workflow: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- Figure2_cross_domain_coupling_hierarchy: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- Figure3_environmental_driver_analysis: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- Figure4_plant_diversity_hypothesis_comparison: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- Figure5_integrated_ecological_synthesis_network: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- FigureS1_mantel_only_visualization: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- FigureS2_procrustes_only_visualization: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True
- FigureS3_geography_sensitivity_comparison: png_exists=True, svg_exists=True, png_signature_valid=True, svg_xml_valid=True

## Repository hygiene checks
- `git diff --check`: clean (no whitespace/conflict-marker issues reported).
- `git status --short`:
  - `?? figures/`

## Required artifact presence checks
- Figure PNG files found: 8 (5 main + 3 supplemental)
- Figure SVG files found: 8 (5 main + 3 supplemental)
- Source-data CSV files found: 10
- Caption markdown files found: 8
