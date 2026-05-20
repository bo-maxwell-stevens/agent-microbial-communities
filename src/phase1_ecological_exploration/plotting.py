from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _ordination_scatter(ax, coords, title, color="steelblue", alpha=0.7, s=30):
    if coords is None or coords.shape[1] < 2:
        ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(title)
        return
    ax.scatter(coords.iloc[:, 0], coords.iloc[:, 1], c=color, alpha=alpha, s=s, edgecolors="none")
    ax.set_xlabel(coords.columns[0])
    ax.set_ylabel(coords.columns[1])
    ax.set_title(title)
    ax.axhline(0, color="grey", lw=0.5, ls="--")
    ax.axvline(0, color="grey", lw=0.5, ls="--")


def _get_coords(result: dict) -> Optional[pd.DataFrame]:
    return result.get("coordinates", None)


def plot_modality_ordination_comparison(
    modality: str,
    ordination_results: Dict,
    output_path: Path,
):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    jac = ordination_results.get("jaccard_pcoa", {})
    bc = ordination_results.get("bray_curtis_pcoa", {})
    if not bc.get("success", False):
        bc = ordination_results.get("bray_curtis_nmds", {})

    clr_keys = [k for k in ordination_results.get("clr_pca", {}).keys()]
    clr_key = sorted(clr_keys)[1] if len(clr_keys) >= 2 else (clr_keys[0] if clr_keys else None)
    clr_res = ordination_results.get("clr_pca", {}).get(clr_key, {}) if clr_key else {}

    _ordination_scatter(axes[0], _get_coords(jac), f"{modality}: Jaccard PCoA", color="coral")
    _ordination_scatter(axes[1], _get_coords(bc), f"{modality}: Bray-Curtis PCoA/NMDS", color="seagreen")
    _ordination_scatter(axes[2], _get_coords(clr_res), f"{modality}: CLR PCA (5% prevalence)", color="purple")

    for ax in axes:
        ax.set_box_aspect(1)

    plt.tight_layout()
    fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved %s", output_path)


def plot_ordination_comparisons(
    all_results: Dict[str, Dict],
    output_dir: Path,
):
    output_dir.mkdir(parents=True, exist_ok=True)
    for modality, mod_results in all_results.items():
        path = output_dir / f"{modality}_ordination_comparison.png"
        plot_modality_ordination_comparison(modality, mod_results, path)


def plot_prevalence_sensitivity_summary(
    sensitivity_dfs: Dict[str, pd.DataFrame],
    output_path: Path,
):
    n_mod = len(sensitivity_dfs)
    fig, axes = plt.subplots(1, n_mod, figsize=(6 * n_mod, 5), squeeze=False)
    axes = axes[0]

    for idx, (modality, df) in enumerate(sensitivity_dfs.items()):
        ax = axes[idx]
        thresh_pct = df["prevalence_threshold"].values * 100
        retained = df["features_retained"].values
        ax.plot(thresh_pct, retained, "o-", color="steelblue", markersize=5)
        ax.set_xlabel("Prevalence threshold (%)")
        ax.set_ylabel("Features retained")
        ax.set_title(f"{modality}")
        ax.grid(True, alpha=0.3)
        ax.set_xlim(left=0)

    plt.tight_layout()
    fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved %s", output_path)


def plot_cohort_depth_summary(
    sample_cohort: pd.DataFrame,
    modality_otu_tables: Dict[str, pd.DataFrame],
    output_path: Path,
):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    modalities = ["AMF", "BAC", "EUK", "ITS"]

    for idx, mod in enumerate(modalities):
        ax = axes[idx]
        if mod in modality_otu_tables:
            otu = modality_otu_tables[mod]
            common = otu.index.intersection(sample_cohort["sample_id"])
            depths = otu.loc[common].sum(axis=1)
            depths = depths.replace(0, np.nan).dropna()
            ax.hist(depths, bins=30, color="steelblue", edgecolor="white", alpha=0.8)
            ax.set_xlabel("Sequencing depth")
            ax.set_ylabel("Sample count")
            ax.set_title(f"{mod} (n={len(depths)})")
        else:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(mod)
        ax.set_box_aspect(1)

    plt.tight_layout()
    fig.savefig(str(output_path), dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Saved %s", output_path)
