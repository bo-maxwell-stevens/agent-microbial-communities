#!/usr/bin/env python3
"""Phase 1.5 — Conservative ordination and sensitivity diagnostics.

Reuses the microbial_plus_metadata_overlap (84 samples) from Phase 1 cohort.

Outputs (written to RESULTS_DIR):
  - ordination_summary.csv
  - preprocessing_sensitivity_summary.csv
  - prevalence_threshold_summary.csv
  - sample_cohort_used.csv
  - ordination_runtime_metadata.json
  - warnings.log
  - figures/{AMF,BAC,EUK,ITS}_ordination_comparison.png
  - figures/prevalence_sensitivity_summary.png
  - figures/cohort_depth_summary.png
"""

from __future__ import annotations

import argparse
import json
import logging
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.data_loading import load_project_data
from src.phase1_ecological_exploration.dataset_loader import (
    build_input_provenance,
    to_legacy_datasets,
)
from src.phase1_ecological_exploration.ordination_analysis import (
    run_ordination_strategies,
    to_binary,
    to_relative_abundance,
    clr_transform,
    prevalence_filter,
)
from src.phase1_ecological_exploration.preprocessing_sensitivity import (
    compute_prevalence_sensitivity,
    compute_preprocessing_summary,
)
from src.phase1_ecological_exploration.diagnostics import (
    compare_ordinations,
)
from src.phase1_ecological_exploration.plotting import (
    plot_ordination_comparisons,
    plot_prevalence_sensitivity_summary,
    plot_cohort_depth_summary,
)

logger = logging.getLogger("phase1_5")


def _get_git_commit(repo_root: Path) -> Optional[str]:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True, text=True, cwd=repo_root, timeout=10,
        ).stdout.strip()
    except Exception:
        return None


def _check_package_version(pkg_name: str) -> str:
    try:
        mod = __import__(pkg_name)
        return getattr(mod, "__version__", "unknown")
    except ImportError:
        return "not_available"


def _load_cohort_sample_ids(cohort_path: Path) -> List[str]:
    if not cohort_path.exists():
        raise FileNotFoundError(
            f"Required cohort file not found: {cohort_path}. "
            "Run scripts/run_phase1_ecological_exploration.py first."
        )

    with open(cohort_path) as f:
        cohort = json.load(f)

    samples = cohort.get("microbial_plus_metadata_overlap", [])
    if isinstance(samples, dict):
        samples = samples.get("items", [])

    if not isinstance(samples, list) or not all(isinstance(x, str) for x in samples):
        raise ValueError(
            f"Unexpected microbial_plus_metadata_overlap payload in {cohort_path}"
        )

    logger.info("Loaded %d cohort samples from %s", len(samples), cohort_path)
    return samples


def setup_logging(warnings_path: Path) -> logging.Handler:
    warnings_path.parent.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(str(warnings_path), mode="w")
    fh.setLevel(logging.WARNING)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logging.getLogger().addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logging.getLogger().addHandler(sh)
    logging.getLogger().setLevel(logging.DEBUG)
    return fh


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 1.5 conservative ordination and sensitivity diagnostics"
    )
    parser.add_argument(
        "--repo-root",
        type=str,
        default=str(REPO_ROOT),
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default="results/phase1_5_conservative_ordination",
    )
    parser.add_argument(
        "--cohort-file",
        type=str,
        default=str(REPO_ROOT / "results" / "phase1_ecological_exploration" / "cohort_definition.json"),
    )
    parser.add_argument(
        "--prevalence-thresholds",
        type=float,
        nargs="+",
        default=[0.01, 0.05, 0.10],
    )
    parser.add_argument(
        "--sensitivity-thresholds",
        type=float,
        nargs="+",
        default=[0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20],
    )
    return parser.parse_args()


def modality_ordinations(
    modality: str,
    otu_table: pd.DataFrame,
    sample_ids: List[str],
    prevalence_thresholds: List[float],
    results_dir: Path,
) -> Dict:
    common = sorted(set(otu_table.index.astype(str)) & set(sample_ids))
    logger.info("%s: %d overlapping samples of %d cohort samples",
                modality, len(common), len(sample_ids))

    otu_sub = otu_table.loc[otu_table.index.astype(str).isin(common)]
    logger.info("%s: OTU table shape after subset: %s", modality, otu_sub.shape)

    results = run_ordination_strategies(otu_sub, common, prevalence_thresholds)
    results["n_samples_used"] = len(common)
    results["n_features"] = otu_sub.shape[1]

    sensitivity_df = compute_prevalence_sensitivity(otu_sub, common)
    sens_path = results_dir / f"{modality}_prevalence_sensitivity.csv"
    sensitivity_df.to_csv(sens_path, index=False)
    logger.info("Saved %s prevalence sensitivity table", modality)

    results["prevalence_sensitivity"] = sensitivity_df

    return results


def main() -> None:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    data_dir = (repo_root / args.data_dir).resolve()
    results_dir = (repo_root / args.results_dir).resolve()
    cohort_path = Path(args.cohort_file).resolve()
    figures_dir = results_dir / "figures"
    results_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    warnings_path = results_dir / "warnings.log"
    setup_logging(warnings_path)

    logger.info("Phase 1.5 starting at %s", datetime.now(timezone.utc).isoformat())
    logger.info("Results dir: %s", results_dir)
    t_start = time.time()

    logger.info("Loading datasets from %s ...", data_dir)
    project_data = load_project_data(data_dir)
    datasets = to_legacy_datasets(project_data)
    provenance = build_input_provenance(data_dir)

    logger.info("Loading cohort sample IDs ...")
    sample_ids = _load_cohort_sample_ids(cohort_path)

    cohort_used = pd.DataFrame({"sample_id": sorted(sample_ids)})
    cohort_path_out = results_dir / "sample_cohort_used.csv"
    cohort_used.to_csv(cohort_path_out, index=False)
    logger.info("Saved sample cohort (%d samples) to %s", len(sample_ids), cohort_path_out)

    modalities = ["AMF", "BAC", "EUK", "ITS"]
    all_results: Dict[str, Dict] = {}
    all_sensitivity_dfs: Dict[str, pd.DataFrame] = {}
    modality_otu_tables: Dict[str, pd.DataFrame] = {}

    for mod in modalities:
        otu = datasets[mod]["otu"]
        modality_otu_tables[mod] = otu

    logger.info("Running ordinations for all modalities ...")
    for mod in modalities:
        logger.info("=" * 60)
        logger.info("Processing %s ...", mod)
        try:
            mod_results = modality_ordinations(
                mod, datasets[mod]["otu"], sample_ids,
                args.prevalence_thresholds, results_dir,
            )
            all_results[mod] = mod_results
            all_sensitivity_dfs[mod] = mod_results["prevalence_sensitivity"]
        except Exception as e:
            logger.error("Fatal error in %s ordination: %s", mod, e, exc_info=True)
            all_results[mod] = {"error": str(e)}
            all_sensitivity_dfs[mod] = pd.DataFrame()

    logger.info("Computing preprocessing sensitivity summary ...")
    prep_summary = compute_preprocessing_summary(all_results)
    prep_path = results_dir / "preprocessing_sensitivity_summary.csv"
    prep_summary.to_csv(prep_path, index=False)
    logger.info("Saved preprocessing sensitivity summary (%d rows)", len(prep_summary))

    logger.info("Computing prevalence threshold summary ...")
    prev_records = []
    for mod, sens_df in all_sensitivity_dfs.items():
        if sens_df is not None and len(sens_df) > 0:
            for _, row in sens_df.iterrows():
                prev_records.append({
                    "modality": mod,
                    "prevalence_threshold": row.get("prevalence_threshold"),
                    "threshold_label": row.get("threshold_label"),
                    "min_occurrences": row.get("min_occurrences"),
                    "total_features": row.get("total_features"),
                    "features_retained": row.get("features_retained"),
                    "features_removed": row.get("features_removed"),
                    "fraction_retained": row.get("fraction_retained"),
                })
    prev_df = pd.DataFrame(prev_records)
    prev_path = results_dir / "prevalence_threshold_summary.csv"
    prev_df.to_csv(prev_path, index=False)
    logger.info("Saved prevalence threshold summary (%d rows)", len(prev_df))

    logger.info("Computing cross-method stability diagnostics ...")
    diag_records = []
    for mod, mod_results in all_results.items():
        if "error" in mod_results:
            continue
        diags = compare_ordinations(mod_results, use_permutation_test=True)
        for d in diags:
            d["modality"] = mod
            diag_records.append(d)
    diag_df = pd.DataFrame(diag_records) if diag_records else pd.DataFrame()
    diag_path = results_dir / "ordination_stability_diagnostics.csv"
    diag_df.to_csv(diag_path, index=False)
    logger.info("Saved stability diagnostics (%d rows)", len(diag_df))

    logger.info("Generating ordination summary ...")
    ord_summary_records = []
    for mod, mod_results in all_results.items():
        if "error" in mod_results:
            ord_summary_records.append({
                "modality": mod,
                "strategy": "error",
                "n_samples": mod_results.get("n_samples_used", 0),
                "n_features": mod_results.get("n_features", 0),
                "engine": "none",
                "success": False,
            })
            continue
        for strategy_key in ["jaccard_pcoa", "bray_curtis_pcoa",
                              "bray_curtis_nmds", "jaccard_nmds"]:
            strategy_res = mod_results.get(strategy_key, {})
            coords = strategy_res.get("coordinates", None)
            ord_summary_records.append({
                "modality": mod,
                "strategy": strategy_key,
                "n_samples": mod_results.get("n_samples_used", 0),
                "n_features": mod_results.get("n_features", 0),
                "engine": strategy_res.get("engine", "none"),
                "success": strategy_res.get("success", False),
                "n_dimensions": coords.shape[1] if coords is not None else 0,
            })
        for clr_key, clr_res in mod_results.get("clr_pca", {}).items():
            thresh_info = clr_res.get("threshold_info", {})
            coords = clr_res.get("coordinates", None)
            ord_summary_records.append({
                "modality": mod,
                "strategy": f"CLR_PCA_{thresh_info.get('threshold_label', clr_key)}",
                "n_samples": mod_results.get("n_samples_used", 0),
                "n_features_retained": thresh_info.get("features_after", None),
                "engine": clr_res.get("engine", "none"),
                "success": clr_res.get("success", False),
                "n_dimensions": coords.shape[1] if coords is not None else 0,
            })
    ord_summary = pd.DataFrame(ord_summary_records)
    ord_summary_path = results_dir / "ordination_summary.csv"
    ord_summary.to_csv(ord_summary_path, index=False)
    logger.info("Saved ordination summary (%d rows)", len(ord_summary))

    logger.info("Generating figures ...")
    try:
        plot_ordination_comparisons(all_results, figures_dir)
        logger.info("Ordination comparison figures saved")
    except Exception as e:
        logger.error("Failed to generate ordination comparison figures: %s", e, exc_info=True)

    try:
        combined_sens = {mod: df for mod, df in all_sensitivity_dfs.items()
                         if df is not None and len(df) > 0}
        if combined_sens:
            plot_prevalence_sensitivity_summary(
                combined_sens,
                figures_dir / "prevalence_sensitivity_summary.png",
            )
            logger.info("Prevalence sensitivity summary figure saved")
    except Exception as e:
        logger.error("Failed to generate prevalence sensitivity figure: %s", e, exc_info=True)

    try:
        plot_cohort_depth_summary(
            cohort_used, modality_otu_tables,
            figures_dir / "cohort_depth_summary.png",
        )
        logger.info("Cohort depth summary figure saved")
    except Exception as e:
        logger.error("Failed to generate cohort depth figure: %s", e, exc_info=True)

    elapsed = time.time() - t_start
    logger.info("All analyses complete in %.1f seconds", elapsed)

    logger.info("Generating runtime metadata ...")
    git_commit = _get_git_commit(repo_root)

    input_hashes = {}
    for mod_key, prov_dict in provenance.items():
        input_hashes[mod_key] = {}
        for sub_key, sub_prov in prov_dict.items():
            if sub_prov:
                input_hashes[mod_key][sub_key] = {
                    "sha256": sub_prov.get("sha256", None),
                    "size_bytes": sub_prov.get("size_bytes", None),
                }

    method_availability = {
        "skbio_pcoa": _check_package_version("skbio") != "not_available",
        "sklearn_pca": _check_package_version("sklearn") != "not_available",
        "sklearn_mds": _check_package_version("sklearn") != "not_available",
        "scipy_procrustes": _check_package_version("scipy") != "not_available",
    }

    strategies_summary = {}
    for mod in modalities:
        if mod in all_results:
            strategies_summary[mod] = {}
            for strat_key in ["jaccard_pcoa", "bray_curtis_pcoa",
                              "bray_curtis_nmds", "jaccard_nmds"]:
                res = all_results[mod].get(strat_key, {})
                strategies_summary[mod][strat_key] = {
                    "engine": res.get("engine", "not_run"),
                    "success": res.get("success", False),
                }
            for clr_key, clr_res in all_results[mod].get("clr_pca", {}).items():
                strategies_summary[mod][clr_key] = {
                    "engine": clr_res.get("engine", "not_run"),
                    "success": clr_res.get("success", False),
                }

    metadata = {
        "pipeline": "phase1_5_conservative_ordination",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit,
        "python_version": sys.version,
        "platform": platform.platform(),
        "command_line": sys.argv,
        "elapsed_seconds": round(elapsed, 2),
        "cohort": {
            "source": str(cohort_path) if cohort_path.exists() else "reconstructed",
            "n_samples": len(sample_ids),
        },
        "parameters": {
            "prevalence_thresholds": args.prevalence_thresholds,
            "sensitivity_thresholds": args.sensitivity_thresholds,
        },
        "package_versions": {
            "numpy": _check_package_version("numpy"),
            "pandas": _check_package_version("pandas"),
            "scipy": _check_package_version("scipy"),
            "sklearn": _check_package_version("sklearn"),
            "skbio": _check_package_version("skbio"),
            "matplotlib": _check_package_version("matplotlib"),
        },
        "method_availability": method_availability,
        "input_provenance": input_hashes,
        "strategies_executed": strategies_summary,
    }

    meta_path = results_dir / "ordination_runtime_metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    logger.info("Saved runtime metadata to %s", meta_path)

    logger.info("Phase 1.5 complete.")


if __name__ == "__main__":
    main()
