"""
Phase 4 Coupling Inference

Adds inferential support to deterministic Phase 2 coupling analysis:
- Mantel permutation p-values (two-sided, label permutation)
- 95% bootstrap confidence intervals for Mantel Spearman
- Procrustes bootstrap stability with 95% confidence intervals

All stochastic procedures are seeded for deterministic reproducibility.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import time

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import rankdata
from sklearn.decomposition import PCA

DATA_DIR = "data"
PHASE2_RESULTS_DIR = "results/phase2_confirmatory_coupling"
RESULTS_DIR = "results/phase4_coupling_inference"
FIG_DIR = f"{RESULTS_DIR}/figures"
COHORT_FILE = f"{PHASE2_RESULTS_DIR}/sample_cohort_used.csv"

SUMMARY_OUT = f"{RESULTS_DIR}/phase4_summary.csv"

PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10
THRESHOLDS = [0.05, 0.10]
BRANCHES = ["presence/absence", "CLR"]
PAIRS = [("AMF", "ITS"), ("AMF", "EUK"), ("EUK", "ITS")]

RANDOM_SEED = 20260601
N_PERMUTATIONS = 999
N_BOOTSTRAPS = 120


def load_otu_table(name: str) -> pd.DataFrame:
    return pd.read_csv(f"{DATA_DIR}/{name}_OTU_table_final.tsv", sep="\t", index_col=0)


def align_samples(table: pd.DataFrame, cohort_sample_ids: list[str]) -> pd.DataFrame:
    aligned = table.reindex(cohort_sample_ids)
    if aligned.isnull().all(axis=1).any():
        missing = aligned.index[aligned.isnull().all(axis=1)].tolist()
        raise ValueError(f"Missing cohort samples in OTU table: {missing[:5]}")
    return aligned


def prevalence_filter_table(table: pd.DataFrame, threshold: float) -> pd.DataFrame:
    table = table.reindex(sorted(table.columns), axis=1)
    prevalence = (table > 0).mean(axis=0)
    keep_cols = prevalence[prevalence >= threshold].index.tolist()
    if not keep_cols:
        keep_cols = prevalence.sort_values(ascending=False).head(1).index.tolist()
    return table.loc[:, keep_cols]


def to_presence_absence(table: pd.DataFrame) -> pd.DataFrame:
    return (table > 0).astype(float)


def to_relative_abundance(table: pd.DataFrame) -> pd.DataFrame:
    row_sums = table.sum(axis=1).replace(0.0, np.nan)
    return table.div(row_sums, axis=0).fillna(0.0)


def clr_transform(rel_table: pd.DataFrame, pseudocount: float = PSEUDOCOUNT) -> pd.DataFrame:
    vals = rel_table.to_numpy(dtype=np.float64) + pseudocount
    gm = np.exp(np.mean(np.log(vals), axis=1, keepdims=True))
    return pd.DataFrame(np.log(vals / gm), index=rel_table.index, columns=rel_table.columns)


def jaccard_distance_matrix(binary_table: pd.DataFrame) -> np.ndarray:
    return squareform(pdist(binary_table.to_numpy(dtype=np.float64), metric="jaccard"))


def euclidean_distance_matrix(table: pd.DataFrame) -> np.ndarray:
    return squareform(pdist(table.to_numpy(dtype=np.float64), metric="euclidean"))


def pcoa_from_distance(distance_matrix: np.ndarray, n_components: int = N_COMPONENTS) -> np.ndarray:
    n = distance_matrix.shape[0]
    d2 = np.square(distance_matrix)
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ d2 @ j

    eigvals, eigvecs = np.linalg.eigh(b)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    pos_mask = eigvals > 0
    eigvals = eigvals[pos_mask]
    eigvecs = eigvecs[:, pos_mask]

    if eigvals.size == 0:
        k = max(1, min(n_components, n - 1))
        return np.zeros((n, k), dtype=np.float64)

    k = min(n_components, n - 1, eigvals.size)
    return eigvecs[:, :k] * np.sqrt(eigvals[:k])


def pca_embedding(table: pd.DataFrame, n_components: int = N_COMPONENTS) -> np.ndarray:
    x = table.to_numpy(dtype=np.float64)
    k = max(1, min(n_components, x.shape[0] - 1 if x.shape[0] > 1 else 1, x.shape[1]))
    model = PCA(n_components=k, svd_solver="full")
    return model.fit_transform(x)


def condensed_upper(distance_matrix: np.ndarray) -> np.ndarray:
    i, j = np.triu_indices(distance_matrix.shape[0], k=1)
    return distance_matrix[i, j]


def spearman_fast(x: np.ndarray, y: np.ndarray) -> float:
    rx = rankdata(x)
    ry = rankdata(y)
    sx = rx.std()
    sy = ry.std()
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return float(np.corrcoef(rx, ry)[0, 1])


def compute_mantel_spearman(distance_x: np.ndarray, distance_y: np.ndarray) -> float:
    return spearman_fast(condensed_upper(distance_x), condensed_upper(distance_y))


def compute_procrustes(embedding_x: np.ndarray, embedding_y: np.ndarray) -> float:
    try:
        _, _, disparity = procrustes(embedding_x, embedding_y)
        return float(disparity)
    except Exception:
        return float("nan")


def prepare_branch_outputs(table: pd.DataFrame, threshold: float, branch: str) -> dict:
    filtered = prevalence_filter_table(table, threshold)

    if branch == "presence/absence":
        transformed = to_presence_absence(filtered)
        distance = jaccard_distance_matrix(transformed)
        embedding = pcoa_from_distance(distance, N_COMPONENTS)
        distance_metric = "jaccard"
        ordination_method = "pcoa"
    elif branch == "CLR":
        rel = to_relative_abundance(filtered)
        transformed = clr_transform(rel, PSEUDOCOUNT)
        distance = euclidean_distance_matrix(transformed)
        embedding = pca_embedding(transformed, N_COMPONENTS)
        distance_metric = "euclidean"
        ordination_method = "pca"
    else:
        raise ValueError(f"Unsupported branch: {branch}")

    return {
        "transformed": transformed,
        "distance": distance,
        "embedding": embedding,
        "distance_metric": distance_metric,
        "ordination_method": ordination_method,
        "n_features": int(filtered.shape[1]),
    }


def bootstrap_metrics(
    table1: pd.DataFrame,
    table2: pd.DataFrame,
    threshold: float,
    branch: str,
    rng: np.random.Generator,
    n_bootstraps: int,
    progress_label: str = "",
) -> tuple[np.ndarray, np.ndarray]:
    n = table1.shape[0]
    mantel_vals = np.empty(n_bootstraps, dtype=np.float64)
    proc_vals = np.empty(n_bootstraps, dtype=np.float64)

    for b in range(n_bootstraps):
        idx = rng.integers(0, n, size=n)
        t1 = table1.iloc[idx].copy()
        t2 = table2.iloc[idx].copy()

        o1 = prepare_branch_outputs(t1, threshold, branch)
        o2 = prepare_branch_outputs(t2, threshold, branch)

        mantel_vals[b] = compute_mantel_spearman(o1["distance"], o2["distance"])
        proc_vals[b] = compute_procrustes(o1["embedding"], o2["embedding"])

        if (b + 1) % 10 == 0 or (b + 1) == n_bootstraps:
            prefix = f"[{progress_label}] " if progress_label else ""
            print(f"{prefix}Bootstrap progress: {b + 1}/{n_bootstraps}")

    return mantel_vals, proc_vals


def mantel_permutation_pvalue(
    distance_x: np.ndarray,
    distance_y: np.ndarray,
    rng: np.random.Generator,
    n_permutations: int,
    progress_label: str = "",
) -> tuple[float, float]:
    obs = compute_mantel_spearman(distance_x, distance_y)
    n = distance_x.shape[0]
    hits = 0
    for i in range(n_permutations):
        perm = rng.permutation(n)
        dy = distance_y[np.ix_(perm, perm)]
        stat = compute_mantel_spearman(distance_x, dy)
        if abs(stat) >= abs(obs):
            hits += 1

        if (i + 1) % 100 == 0 or (i + 1) == n_permutations:
            prefix = f"[{progress_label}] " if progress_label else ""
            print(f"{prefix}Permutation progress: {i + 1}/{n_permutations}")

    p = (hits + 1) / (n_permutations + 1)
    return obs, float(p)


def ci95(x: np.ndarray) -> tuple[float, float]:
    return float(np.nanpercentile(x, 2.5)), float(np.nanpercentile(x, 97.5))


def ensure_dirs() -> None:
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)
    Path(FIG_DIR).mkdir(parents=True, exist_ok=True)


def build_summary(merged: pd.DataFrame) -> pd.DataFrame:
    summary = (
        merged.groupby(["pair", "branch"], as_index=False)
        .agg(
            thresholds_evaluated=("threshold", "nunique"),
            mantel_spearman_mean=("mantel_spearman", "mean"),
            mantel_spearman_min=("mantel_spearman", "min"),
            mantel_spearman_max=("mantel_spearman", "max"),
            mantel_perm_pvalue_conservative=("mantel_perm_pvalue", "max"),
            mantel_ci_lower_conservative=("mantel_ci_lower", "min"),
            mantel_ci_upper_conservative=("mantel_ci_upper", "max"),
            procrustes_fit_mean=("procrustes_fit", "mean"),
            procrustes_fit_best=("procrustes_fit", "min"),
            procrustes_fit_worst=("procrustes_fit", "max"),
            procrustes_ci_lower_conservative=("procrustes_ci_lower", "min"),
            procrustes_ci_upper_conservative=("procrustes_ci_upper", "max"),
            procrustes_bootstrap_sd_mean=("procrustes_bootstrap_sd", "mean"),
        )
    )

    summary["procrustes_similarity_mean"] = 1.0 - summary["procrustes_fit_mean"]
    summary["rank_mantel"] = summary["mantel_spearman_mean"].rank(ascending=False, method="min").astype(int)
    summary["rank_procrustes_similarity"] = summary["procrustes_similarity_mean"].rank(ascending=False, method="min").astype(int)
    summary["rank_overall"] = (
        (summary["rank_mantel"] + summary["rank_procrustes_similarity"]) / 2.0
    )
    summary = summary.sort_values(["rank_overall", "mantel_spearman_mean"], ascending=[True, False]).reset_index(drop=True)
    return summary


def write_checkpoint_outputs(
    mantel_rows: list[dict],
    proc_rows: list[dict],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if mantel_rows:
        mantel_df = pd.DataFrame(mantel_rows).sort_values(["pair", "branch", "threshold"]).reset_index(drop=True)
        mantel_df.to_csv(f"{RESULTS_DIR}/phase4_mantel_inference.csv", index=False)
    else:
        mantel_df = pd.DataFrame()

    if proc_rows:
        proc_df = pd.DataFrame(proc_rows).sort_values(["pair", "branch", "threshold"]).reset_index(drop=True)
        proc_df.to_csv(f"{RESULTS_DIR}/phase4_procrustes_bootstrap.csv", index=False)
    else:
        proc_df = pd.DataFrame()

    if not mantel_df.empty and not proc_df.empty:
        merged = mantel_df.merge(
            proc_df,
            on=["pair", "branch", "threshold", "n_bootstraps", "seed"],
            how="inner",
        )
        summary = build_summary(merged)
        summary.to_csv(f"{RESULTS_DIR}/phase4_summary.csv", index=False)
    else:
        summary = pd.DataFrame()

    return mantel_df, proc_df, summary




def _nonnegative_errorbars(estimate: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    """Return matplotlib-compatible yerr with guaranteed non-negative distances."""
    lower_err = np.maximum(0.0, estimate - lower)
    upper_err = np.maximum(0.0, upper - estimate)
    return np.vstack([lower_err, upper_err])


def make_figures(summary_df: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt

    plot_df = summary_df.copy()
    plot_df["label"] = plot_df["pair"] + " | " + plot_df["branch"]

    # Mantel effect sizes with CI
    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(plot_df))
    y = plot_df["mantel_spearman_mean"].to_numpy()
    lo = plot_df["mantel_ci_lower_conservative"].to_numpy()
    hi = plot_df["mantel_ci_upper_conservative"].to_numpy()
    yerr = _nonnegative_errorbars(y, lo, hi)

    colors = ["#2ca02c" if p < 0.05 else "#7f7f7f" for p in plot_df["mantel_perm_pvalue_conservative"]]
    ax.bar(x, y, color=colors, alpha=0.9)
    ax.errorbar(x, y, yerr=yerr, fmt="none", ecolor="black", capsize=4, linewidth=1)
    ax.axhline(0, color="black", linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["label"], rotation=30, ha="right")
    ax.set_ylabel("Mantel Spearman (mean over thresholds)")
    ax.set_title("Phase 4: Mantel effect sizes with conservative 95% CI")
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/mantel_effect_sizes.png", dpi=180)
    plt.close(fig)

    # Procrustes similarity (1-disparity) with CI
    sim = 1.0 - plot_df["procrustes_fit_mean"].to_numpy()
    sim_lo_raw = 1.0 - plot_df["procrustes_ci_upper_conservative"].to_numpy()
    sim_hi_raw = 1.0 - plot_df["procrustes_ci_lower_conservative"].to_numpy()
    sim_lo = np.minimum(sim_lo_raw, sim_hi_raw)
    sim_hi = np.maximum(sim_lo_raw, sim_hi_raw)
    yerr2 = _nonnegative_errorbars(sim, sim_lo, sim_hi)

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(x, sim, color="#1f77b4", alpha=0.9)
    ax.errorbar(x, sim, yerr=yerr2, fmt="none", ecolor="black", capsize=4, linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(plot_df["label"], rotation=30, ha="right")
    ax.set_ylabel("Procrustes similarity (1 - disparity)")
    ax.set_title("Phase 4: Procrustes effect sizes with conservative 95% CI")
    fig.tight_layout()
    fig.savefig(f"{FIG_DIR}/procrustes_effect_sizes.png", dpi=180)
    plt.close(fig)

    # Combined uncertainty intervals
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

    y_idx = np.arange(len(plot_df))
    axes[0].hlines(y_idx, lo, hi, color="#2ca02c", linewidth=2)
    axes[0].plot(y, y_idx, "o", color="#2ca02c")
    axes[0].axvline(0, color="black", linewidth=1)
    axes[0].set_title("Mantel Spearman intervals")
    axes[0].set_xlabel("Correlation")

    axes[1].hlines(y_idx, sim_lo, sim_hi, color="#1f77b4", linewidth=2)
    axes[1].plot(sim, y_idx, "o", color="#1f77b4")
    axes[1].set_title("Procrustes similarity intervals")
    axes[1].set_xlabel("1 - disparity")

    axes[0].set_yticks(y_idx)
    axes[0].set_yticklabels(plot_df["label"])
    fig.suptitle("Phase 4 uncertainty intervals (conservative aggregation over thresholds)")
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(f"{FIG_DIR}/uncertainty_intervals.png", dpi=180)
    plt.close(fig)


def main() -> None:
    ensure_dirs()

    cohort = pd.read_csv(COHORT_FILE)["Sample_ID"].astype(str).tolist()
    tables = {name: align_samples(load_otu_table(name), cohort) for name in ["AMF", "EUK", "ITS"]}

    base_rng = np.random.default_rng(RANDOM_SEED)

    mantel_rows: list[dict] = []
    proc_rows: list[dict] = []

    total_combinations = len(THRESHOLDS) * len(BRANCHES) * len(PAIRS)
    combo_idx = 0

    for threshold in THRESHOLDS:
        for branch in BRANCHES:
            for name1, name2 in PAIRS:
                combo_idx += 1
                pair = f"{name1}↔{name2}"
                combo_label = f"threshold={threshold}, branch={branch}, pair={pair}"
                print(f"[COMBO {combo_idx}/{total_combinations}] Starting {combo_label}")
                combo_start = time.perf_counter()

                out1 = prepare_branch_outputs(tables[name1], threshold, branch)
                out2 = prepare_branch_outputs(tables[name2], threshold, branch)

                obs_mantel, p_perm = mantel_permutation_pvalue(
                    out1["distance"],
                    out2["distance"],
                    base_rng,
                    N_PERMUTATIONS,
                    progress_label=combo_label,
                )
                obs_proc = compute_procrustes(out1["embedding"], out2["embedding"])

                # independent deterministic child RNG for bootstrap per config
                child_seed = int(base_rng.integers(0, 2**31 - 1))
                child_rng = np.random.default_rng(child_seed)
                mantel_boot, proc_boot = bootstrap_metrics(
                    tables[name1],
                    tables[name2],
                    threshold,
                    branch,
                    child_rng,
                    N_BOOTSTRAPS,
                    progress_label=combo_label,
                )

                m_lo, m_hi = ci95(mantel_boot)
                p_lo, p_hi = ci95(proc_boot)

                mantel_rows.append(
                    {
                        "pair": pair,
                        "branch": branch,
                        "threshold": threshold,
                        "n_samples": len(cohort),
                        "distance_metric": out1["distance_metric"],
                        "ordination_method": out1["ordination_method"],
                        "n_features_1": out1["n_features"],
                        "n_features_2": out2["n_features"],
                        "mantel_spearman": float(obs_mantel),
                        "mantel_perm_pvalue": float(p_perm),
                        "mantel_bootstrap_median": float(np.nanmedian(mantel_boot)),
                        "mantel_bootstrap_sd": float(np.nanstd(mantel_boot, ddof=1)),
                        "mantel_ci_lower": m_lo,
                        "mantel_ci_upper": m_hi,
                        "n_permutations": N_PERMUTATIONS,
                        "n_bootstraps": N_BOOTSTRAPS,
                        "seed": child_seed,
                    }
                )

                proc_rows.append(
                    {
                        "pair": pair,
                        "branch": branch,
                        "threshold": threshold,
                        "procrustes_fit": float(obs_proc),
                        "procrustes_bootstrap_mean": float(np.nanmean(proc_boot)),
                        "procrustes_bootstrap_median": float(np.nanmedian(proc_boot)),
                        "procrustes_bootstrap_sd": float(np.nanstd(proc_boot, ddof=1)),
                        "procrustes_ci_lower": p_lo,
                        "procrustes_ci_upper": p_hi,
                        "n_bootstraps": N_BOOTSTRAPS,
                        "seed": child_seed,
                    }
                )

                write_checkpoint_outputs(mantel_rows, proc_rows)
                elapsed = time.perf_counter() - combo_start
                print(f"[COMBO {combo_idx}/{total_combinations}] Completed {combo_label} in {elapsed:.2f}s")
                print("Checkpoint files updated")

    mantel_df, proc_df, summary = write_checkpoint_outputs(mantel_rows, proc_rows)

    make_figures(summary)

    print("Phase 4 inference complete")
    print(f"Wrote {RESULTS_DIR}/phase4_mantel_inference.csv")
    print(f"Wrote {RESULTS_DIR}/phase4_procrustes_bootstrap.csv")
    print(f"Wrote {RESULTS_DIR}/phase4_summary.csv")
    print(f"Wrote figures to {FIG_DIR}")


def render_figures_from_existing_outputs(summary_csv: str = SUMMARY_OUT) -> None:
    ensure_dirs()
    summary = pd.read_csv(summary_csv)
    make_figures(summary)
    print(f"Figures rendered from existing summary: {summary_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phase 4 coupling inference and figure generation")
    parser.add_argument(
        "--figures-only",
        action="store_true",
        help="Skip inference and render figures from an existing summary CSV.",
    )
    parser.add_argument(
        "--summary-csv",
        default=SUMMARY_OUT,
        help="Summary CSV path used when --figures-only is set.",
    )
    args = parser.parse_args()

    if args.figures_only:
        render_figures_from_existing_outputs(args.summary_csv)
    else:
        main()
