#!/usr/bin/env python3
"""Phase 5D synthesis: integrate completed Phase 2/4/5/5B/5C outputs.

This script is intentionally read-from-results-only and does not rerun prior analyses.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
RESULTS_ROOT = REPO_ROOT / "results"
OUT_DIR = RESULTS_ROOT / "phase5d_synthesis"
OUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class Inputs:
    phase5_bac_summary: pd.DataFrame
    phase5b_db_rda: pd.DataFrame
    phase5b_predictor: pd.DataFrame
    phase5c_model_comparison: pd.DataFrame
    phase5c_hypothesis_summary: pd.DataFrame


def read_csv(rel_path: str) -> pd.DataFrame:
    path = REPO_ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return pd.read_csv(path)


def load_inputs() -> Inputs:
    return Inputs(
        phase5_bac_summary=read_csv("results/phase5_bac_integration/phase5_bac_coupling_summary.csv"),
        phase5b_db_rda=read_csv("results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv"),
        phase5b_predictor=read_csv("results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv"),
        phase5c_model_comparison=read_csv("results/phase5c_plant_diversity/phase5c_model_comparison.csv"),
        phase5c_hypothesis_summary=read_csv("results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv"),
    )


def ci_string(lower: float, upper: float) -> str:
    if pd.isna(lower) or pd.isna(upper):
        return ""
    return f"[{lower:.3f}, {upper:.3f}]"


def build_final_coupling_rankings(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Mantel"] = out["mantel_spearman_mean"]
    out["Mantel p"] = out["mantel_perm_pvalue_conservative"]
    out["Mantel CI if available"] = out.apply(
        lambda r: ci_string(r["mantel_ci_lower_conservative"], r["mantel_ci_upper_conservative"]),
        axis=1,
    )
    out["Procrustes similarity"] = out["procrustes_similarity_mean"]
    out["Procrustes CI if available"] = out.apply(
        lambda r: ci_string(r["procrustes_ci_lower_conservative"], r["procrustes_ci_upper_conservative"]),
        axis=1,
    )
    out["BAC-inclusive flag"] = out["pair"].str.contains("BAC")
    out["AMF-centered flag"] = out["pair"].str.contains("AMF")
    out["coupling_strength"] = (out["Mantel"] + out["Procrustes similarity"]) / 2.0

    out = out[
        [
            "pair",
            "branch",
            "Mantel",
            "Mantel p",
            "Mantel CI if available",
            "Procrustes similarity",
            "Procrustes CI if available",
            "BAC-inclusive flag",
            "AMF-centered flag",
            "coupling_strength",
        ]
    ].sort_values(["coupling_strength", "Mantel"], ascending=[False, False])

    out.to_csv(OUT_DIR / "final_coupling_rankings.csv", index=False)
    return out


def _summary_row(summary_df: pd.DataFrame, pair: str, branch: str, model_type: str) -> pd.Series | None:
    m = summary_df[
        (summary_df["pair"] == pair)
        & (summary_df["branch"] == branch)
        & (summary_df["record_type"] == "summary")
        & (summary_df["model_type"] == model_type)
    ]
    if m.empty:
        return None
    return m.iloc[0]


def _top_predictor(pred_df: pd.DataFrame, pair: str, branch: str, model_type: str) -> Tuple[str, float]:
    m = pred_df[
        (pred_df["pair"] == pair)
        & (pred_df["branch"] == branch)
        & (pred_df["record_type"] == "predictor_ranking")
        & (pred_df["model_type"] == model_type)
    ]
    if m.empty:
        return "", np.nan
    top = m.sort_values("delta_adj_r2", ascending=False).iloc[0]
    return str(top["predictor"]), float(top["delta_adj_r2"])


def _ph_contribution(pred_df: pd.DataFrame, pair: str, branch: str, model_type: str) -> float:
    m = pred_df[
        (pred_df["pair"] == pair)
        & (pred_df["branch"] == branch)
        & (pred_df["record_type"] == "predictor_ranking")
        & (pred_df["model_type"] == model_type)
        & (pred_df["predictor"] == "pH_KCl")
    ]
    if m.empty:
        return np.nan
    return float(m.iloc[0]["delta_adj_r2"])


def build_environment_summary(summary_df: pd.DataFrame, pred_df: pd.DataFrame) -> pd.DataFrame:
    combos = (
        summary_df[summary_df["record_type"] == "summary"][["pair", "branch"]]
        .drop_duplicates()
        .sort_values(["pair", "branch"])
    )

    rows = []
    for _, combo in combos.iterrows():
        pair, branch = combo["pair"], combo["branch"]
        primary = _summary_row(summary_df, pair, branch, "primary")
        geo = _summary_row(summary_df, pair, branch, "geography_sensitivity")

        primary_adj = float(primary["adjusted_r2"]) if primary is not None else np.nan
        geo_adj = float(geo["adjusted_r2"]) if geo is not None else np.nan
        geo_delta = geo_adj - primary_adj if (pd.notna(primary_adj) and pd.notna(geo_adj)) else np.nan

        best_model_type = "primary"
        best_adj = primary_adj
        if pd.notna(geo_adj) and (pd.isna(primary_adj) or geo_adj > primary_adj):
            best_model_type = "geography_sensitivity"
            best_adj = geo_adj

        top_pred, _ = _top_predictor(pred_df, pair, branch, best_model_type)
        ph_contrib = _ph_contribution(pred_df, pair, branch, best_model_type)

        rows.append(
            {
                "pair": pair,
                "branch": branch,
                "dbRDA adjusted R²": best_adj,
                "best environmental model": best_model_type,
                "top predictor": top_pred,
                "pH contribution": ph_contrib,
                "geography sensitivity delta": geo_delta,
            }
        )

    out = pd.DataFrame(rows).sort_values(["dbRDA adjusted R²", "pair", "branch"], ascending=[False, True, True])
    out.to_csv(OUT_DIR / "final_environment_driver_summary.csv", index=False)
    return out


def _hyp_delta(df: pd.DataFrame, pair: str, branch: str, hypothesis_id: str) -> float:
    m = df[
        (df["pair"] == pair)
        & (df["branch"] == branch)
        & (df["record_type"] == "model_summary")
        & (df["model_scope"] == "primary")
        & (df["hypothesis_id"] == hypothesis_id)
    ]
    if m.empty:
        return np.nan
    return float(m.iloc[0]["delta_adjusted_r2_vs_base"])


def build_plant_diversity_summary(model_df: pd.DataFrame) -> pd.DataFrame:
    base = model_df[
        (model_df["record_type"] == "model_summary")
        & (model_df["model_scope"] == "primary")
        & (model_df["hypothesis_id"].isin(list("ABCDEFG")))
    ].copy()

    rows = []
    for (pair, branch), g in base.groupby(["pair", "branch"], sort=True):
        non_base = g[g["hypothesis_id"] != "A"]
        best = non_base.sort_values("delta_adjusted_r2_vs_base", ascending=False).iloc[0]
        rows.append(
            {
                "pair": pair,
                "branch": branch,
                "best plant hypothesis": f"{best['hypothesis_id']}:{best['hypothesis_name']}",
                "delta adjusted R² vs abiotic base": float(best["delta_adjusted_r2_vs_base"]),
                "alpha effect": _hyp_delta(base, pair, branch, "B"),
                "pool effect": _hyp_delta(base, pair, branch, "D"),
                "dark effect": _hyp_delta(base, pair, branch, "C"),
                "compl effect": _hyp_delta(base, pair, branch, "E"),
            }
        )

    out = pd.DataFrame(rows).sort_values(
        ["delta adjusted R² vs abiotic base", "pair", "branch"], ascending=[False, True, True]
    )
    out.to_csv(OUT_DIR / "final_plant_diversity_summary.csv", index=False)
    return out


def classify_interpretation(coupling_strength: float, env_adj: float, plant_delta: float) -> str:
    if coupling_strength >= 0.50 and env_adj >= 0.20 and plant_delta >= 0.01:
        return "strongly coupled/environment structured + plant associated"
    if coupling_strength >= 0.50 and env_adj >= 0.20:
        return "strongly coupled/environment structured"
    if coupling_strength >= 0.50 and plant_delta >= 0.01:
        return "strongly coupled/plant associated"
    if env_adj >= 0.20 and plant_delta < 0.005:
        return "coupled but mostly abiotic"
    if plant_delta >= 0.01:
        return "weakly coupled but plant associated"
    return "weakly plant associated"


def build_pair_synthesis(
    coupling_df: pd.DataFrame,
    env_df: pd.DataFrame,
    plant_df: pd.DataFrame,
) -> pd.DataFrame:
    merged = coupling_df.merge(env_df, on=["pair", "branch"], how="inner").merge(
        plant_df, on=["pair", "branch"], how="inner"
    )

    out = pd.DataFrame(
        {
            "pair": merged["pair"],
            "branch": merged["branch"],
            "coupling strength": merged["coupling_strength"],
            "environmental explained variation": merged["dbRDA adjusted R²"],
            "plant-diversity added variation": merged["delta adjusted R² vs abiotic base"],
        }
    )
    out["interpretation label"] = out.apply(
        lambda r: classify_interpretation(
            float(r["coupling strength"]),
            float(r["environmental explained variation"]),
            float(r["plant-diversity added variation"]),
        ),
        axis=1,
    )
    out = out.sort_values(["coupling strength", "environmental explained variation"], ascending=[False, False])
    out.to_csv(OUT_DIR / "final_pair_synthesis.csv", index=False)
    return out


def make_coupling_network(coupling_df: pd.DataFrame) -> None:
    domain_pos: Dict[str, Tuple[float, float]] = {
        "BAC": (-1.0, 0.0),
        "ITS": (0.0, 1.0),
        "AMF": (1.0, 0.0),
        "EUK": (0.0, -1.0),
    }

    pair_best = (
        coupling_df.sort_values("coupling_strength", ascending=False)
        .groupby("pair", as_index=False)
        .first()[["pair", "branch", "coupling_strength"]]
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_title("Final coupling network (best branch per pair)")

    for name, (x, y) in domain_pos.items():
        ax.scatter(x, y, s=800, color="#f0f4ff", edgecolor="#304070", linewidth=1.5, zorder=3)
        ax.text(x, y, name, ha="center", va="center", fontsize=11, fontweight="bold", zorder=4)

    for _, row in pair_best.iterrows():
        left, right = row["pair"].split("↔")
        (x1, y1), (x2, y2) = domain_pos[left], domain_pos[right]
        strength = float(row["coupling_strength"])
        color = "#5b8def"
        if "BAC" in row["pair"]:
            color = "#d95f02"
        elif "AMF" in row["pair"]:
            color = "#1b9e77"
        lw = 1.0 + 8.0 * strength
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, alpha=0.6, zorder=2)
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        ax.text(mx, my, f"{row['branch']}\n{strength:.3f}", fontsize=8, ha="center", va="center")

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "final_coupling_network.png", dpi=200)
    plt.close(fig)


def make_driver_heatmap(pred_df: pd.DataFrame) -> None:
    primary = pred_df[
        (pred_df["record_type"] == "predictor_ranking")
        & (pred_df["model_type"] == "primary")
        & (pred_df["predictor"].isin(["pH_KCl", "N_pct", "bio12now.100", "alpha", "compl"]))
    ].copy()
    primary["pair_branch"] = primary["pair"] + " | " + primary["branch"]

    heat = (
        primary.pivot_table(
            index="pair_branch",
            columns="predictor",
            values="delta_adj_r2",
            aggfunc="mean",
        )
        .fillna(0.0)
        .sort_index()
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    im = ax.imshow(heat.values, aspect="auto", cmap="viridis")
    ax.set_title("Environmental driver contributions (primary model, delta adj R2)")
    ax.set_yticks(np.arange(len(heat.index)))
    ax.set_yticklabels(heat.index)
    ax.set_xticks(np.arange(len(heat.columns)))
    ax.set_xticklabels(heat.columns, rotation=30, ha="right")

    for i in range(heat.shape[0]):
        for j in range(heat.shape[1]):
            ax.text(j, i, f"{heat.values[i, j]:.3f}", ha="center", va="center", fontsize=7, color="white")

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("delta adjusted R2")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "final_driver_heatmap.png", dpi=200)
    plt.close(fig)


def make_plant_hypothesis_comparison(hyp_df: pd.DataFrame) -> None:
    hs = hyp_df[hyp_df["summary_type"] == "hypothesis_mean"].copy()
    hs = hs.sort_values("overall_rank")

    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["#2c7fb8" if h == "B" else "#7fcdbb" for h in hs["hypothesis_id"]]
    ax.bar(hs["hypothesis_id"], hs["mean_delta_adjusted_r2"], color=colors)
    ax.set_title("Plant hypothesis comparison (mean delta adj R2 vs abiotic base)")
    ax.set_xlabel("Hypothesis ID")
    ax.set_ylabel("Mean delta adjusted R2")

    for x, y in zip(hs["hypothesis_id"], hs["mean_delta_adjusted_r2"]):
        ax.text(x, y + 0.0005, f"{y:.3f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "final_plant_hypothesis_comparison.png", dpi=200)
    plt.close(fig)


def draw_box(ax, xy: Tuple[float, float], text: str, w: float = 0.25, h: float = 0.12) -> None:
    x, y = xy
    box = plt.Rectangle((x, y), w, h, facecolor="#eef4ff", edgecolor="#39568C", linewidth=1.5)
    ax.add_patch(box)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)


def make_flowchart() -> None:
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.axis("off")

    boxes = [
        ((0.02, 0.40), "Phase 2 plus 4\nCoupling inference"),
        ((0.24, 0.40), "Phase 5\nBAC integration"),
        ((0.46, 0.40), "Phase 5B\nEnvironmental drivers"),
        ((0.68, 0.40), "Phase 5C\nPlant hypotheses"),
        ((0.90 - 0.25, 0.40), "Phase 5D\nFinal synthesis"),
    ]

    for xy, text in boxes:
        draw_box(ax, xy, text)

    for i in range(len(boxes) - 1):
        x1 = boxes[i][0][0] + 0.25
        y1 = boxes[i][0][1] + 0.06
        x2 = boxes[i + 1][0][0]
        y2 = boxes[i + 1][0][1] + 0.06
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", lw=1.8, color="#39568C"))

    ax.text(0.5, 0.2, "No new statistics run: synthesis-only integration of completed outputs", ha="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "final_analysis_flowchart.png", dpi=200)
    plt.close(fig)


def main() -> None:
    inputs = load_inputs()

    coupling = build_final_coupling_rankings(inputs.phase5_bac_summary)
    env = build_environment_summary(inputs.phase5b_db_rda, inputs.phase5b_predictor)
    plant = build_plant_diversity_summary(inputs.phase5c_model_comparison)
    synthesis = build_pair_synthesis(coupling, env, plant)

    make_coupling_network(coupling)
    make_driver_heatmap(inputs.phase5b_predictor)
    make_plant_hypothesis_comparison(inputs.phase5c_hypothesis_summary)
    make_flowchart()

    print("WROTE", OUT_DIR / "final_coupling_rankings.csv", f"rows={len(coupling)}")
    print("WROTE", OUT_DIR / "final_environment_driver_summary.csv", f"rows={len(env)}")
    print("WROTE", OUT_DIR / "final_plant_diversity_summary.csv", f"rows={len(plant)}")
    print("WROTE", OUT_DIR / "final_pair_synthesis.csv", f"rows={len(synthesis)}")
    print("WROTE", OUT_DIR / "final_coupling_network.png")
    print("WROTE", OUT_DIR / "final_driver_heatmap.png")
    print("WROTE", OUT_DIR / "final_plant_hypothesis_comparison.png")
    print("WROTE", OUT_DIR / "final_analysis_flowchart.png")


if __name__ == "__main__":
    main()
