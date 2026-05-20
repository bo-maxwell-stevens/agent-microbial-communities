from src.phase1_ecological_exploration.dataset_loader import load_all_datasets
from src.phase1_ecological_exploration.cohort_builder import build_cohorts
from src.phase1_ecological_exploration.overlap_analysis import compute_overlap_summary
from src.phase1_ecological_exploration.plans_reporting import (
    generate_normalization_plan,
    generate_analysis_plan,
    generate_runtime_metadata,
)
from src.phase1_ecological_exploration.ordination_analysis import (
    run_ordination_strategies,
    to_binary,
    to_relative_abundance,
    clr_transform,
    prevalence_filter,
    jaccard_distance_matrix,
    bray_curtis_distance_matrix,
    run_pcoa,
    run_nmds,
    run_pca,
)
from src.phase1_ecological_exploration.preprocessing_sensitivity import (
    compute_prevalence_sensitivity,
    compute_preprocessing_summary,
)
from src.phase1_ecological_exploration.diagnostics import (
    compute_procrustes,
    procrustes_permutation_test,
    compute_correlation_fallback,
    compare_ordinations,
)
from src.phase1_ecological_exploration.plotting import (
    plot_ordination_comparisons,
    plot_prevalence_sensitivity_summary,
    plot_cohort_depth_summary,
)

__all__ = [
    "load_all_datasets",
    "build_cohorts",
    "compute_overlap_summary",
    "generate_normalization_plan",
    "generate_analysis_plan",
    "generate_runtime_metadata",
    "run_ordination_strategies",
    "to_binary",
    "to_relative_abundance",
    "clr_transform",
    "prevalence_filter",
    "jaccard_distance_matrix",
    "bray_curtis_distance_matrix",
    "run_pcoa",
    "run_nmds",
    "run_pca",
    "compute_prevalence_sensitivity",
    "compute_preprocessing_summary",
    "compute_procrustes",
    "procrustes_permutation_test",
    "compute_correlation_fallback",
    "compare_ordinations",
    "plot_ordination_comparisons",
    "plot_prevalence_sensitivity_summary",
    "plot_cohort_depth_summary",
]
