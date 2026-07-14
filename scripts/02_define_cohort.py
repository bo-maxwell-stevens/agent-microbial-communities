#!/usr/bin/env python3
"""Phase 1 Ecological Exploration — cross-kingdom cohort definition and planning.

Outputs (written to RESULTS_DIR):
  - cohort_definition.json
  - dataset_overlap_summary.csv
  - normalization_plan.md
  - analysis_plan.md
  - runtime_metadata.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.data_loading import build_sample_manifest, load_project_data
from src.phase1_ecological_exploration.cohort_builder import (
    build_cohorts,
    write_cohort_definition,
)
from src.phase1_ecological_exploration.dataset_loader import (
    build_input_provenance,
    to_legacy_datasets,
)
from src.phase1_ecological_exploration.overlap_analysis import (
    compute_overlap_summary,
    write_overlap_summary,
)
from src.phase1_ecological_exploration.plans_reporting import (
    generate_analysis_plan,
    generate_normalization_plan,
    generate_runtime_metadata,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 1 ecological exploration — cohort definition and planning"
    )
    parser.add_argument(
        "--repo-root",
        type=str,
        default=str(REPO_ROOT),
        help="Repository root directory (default: auto-detect)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Path to data directory (relative to repo-root)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results/phase1_ecological_exploration",
        help="Output directory for results (relative to repo-root)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    data_dir = (repo_root / args.data_dir).resolve()
    results_dir = (repo_root / args.results_dir).resolve()
    results_dir.mkdir(parents=True, exist_ok=True)

    print(f"[phase1] Loading datasets from {data_dir} ...")
    project_data = load_project_data(data_dir)
    sample_manifest = build_sample_manifest(project_data)

    datasets = to_legacy_datasets(project_data)
    provenance = build_input_provenance(data_dir)

    print("[phase1] Building cohort definition ...")
    cohort_info = build_cohorts(
        communities=project_data.communities,
        metadata=project_data.metadata,
        sample_manifest=sample_manifest,
    )

    cohort_path = results_dir / "cohort_definition.json"
    write_cohort_definition(cohort_info, cohort_path)
    print(f"  -> {cohort_path}")

    print("[phase1] Computing dataset overlap summary ...")
    overlap_df = compute_overlap_summary(
        communities=project_data.communities,
        sample_manifest=sample_manifest,
    )
    overlap_path = results_dir / "dataset_overlap_summary.csv"
    write_overlap_summary(overlap_df, overlap_path)
    print(f"  -> {overlap_path}")

    print("[phase1] Generating normalization plan ...")
    norm_path = results_dir / "normalization_plan.md"
    generate_normalization_plan(datasets, cohort_info, norm_path)
    print(f"  -> {norm_path}")

    print("[phase1] Generating analysis plan ...")
    analysis_path = results_dir / "analysis_plan.md"
    generate_analysis_plan(cohort_info, overlap_df, analysis_path)
    print(f"  -> {analysis_path}")

    print("[phase1] Generating runtime metadata ...")
    meta_path = results_dir / "runtime_metadata.json"
    generate_runtime_metadata(
        datasets,
        provenance,
        cohort_info,
        repo_root,
        meta_path,
        argv=sys.argv,
    )
    print(f"  -> {meta_path}")

    print("[phase1] Done.")


if __name__ == "__main__":
    main()
