"""
Phase 5A BAC Integration

Extends deterministic Phase 2 + Phase 4 coupling framework to include BAC as a fourth domain:
- Mantel permutation p-values (two-sided, label permutation)
- 95% bootstrap confidence intervals for Mantel Spearman
- Procrustes bootstrap stability with 95% confidence intervals

All stochastic procedures are seeded for deterministic reproducibility.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import rankdata
from sklearn.decomposition import PCA

DATA_DIR = "data"
PHASE2_RESULTS_DIR = "results/phase2_confirmatory_coupling"
RESULTS_DIR = "results/phase5_bac_integration"
COHORT_FILE = f"{PHASE2_RESULTS_DIR}/sample_cohort_used.csv"

PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10
THRESHOLDS = [0.05]
BRANCHES = ["presence/absence", "CLR"]
PAIRS = [
    ("BAC", "AMF"),
    ("BAC", "ITS"),
    ("BAC", "EUK"),
    ("AMF", "ITS"),
    ("AMF", "EUK"),
    ("EUK", "ITS"),
]

RANDOM_SEED = 20260601
N_PERMUTATIONS = 999
N_BOOTSTRAPS = 120
DEFAULT_CLR_DISTANCE_STRATEGY = "direct_aitchison"
VALID_CLR_DISTANCE_STRATEGIES = ("direct_aitchison", "pca10")


def output_paths(output_dir: Path) -> dict[str, Path]:
    fig_dir = output_dir / "figures"
    checkpoints_dir = output_dir / "checkpoints"
    return {
        "output_dir": output_dir,
        "fig_dir": fig_dir,
        "checkpoints_dir": checkpoints_dir,
        "manifest": output_dir / "phase5_combo_manifest.csv",
        "summary": output_dir / "phase5_bac_coupling_summary.csv",
        "mantel": output_dir / "phase5_bac_mantel_inference.csv",
        "procrustes": output_dir / "phase5_bac_procrustes_bootstrap.csv",
        "rank": output_dir / "phase5_bac_rank_summary.csv",
        "fig_mantel": fig_dir / "mantel_effect_sizes.png",
        "fig_procrustes": fig_dir / "procrustes_effect_sizes.png",
        "fig_rankings": fig_dir / "domain_pair_rankings.png",
    }


def ensure_dirs(paths: dict[str, Path]) -> None:
    paths["output_dir"].mkdir(parents=True, exist_ok=True)
    paths["fig_dir"].mkdir(parents=True, exist_ok=True)
    paths["checkpoints_dir"].mkdir(parents=True, exist_ok=True)


def build_combo_manifest() -> pd.DataFrame:
    rows = []
    combo_index = 0
    for name1, name2 in PAIRS:
        pair = f"{name1}↔{name2}"
        for branch in BRANCHES:
            for threshold in THRESHOLDS:
                rows.append(
                    {
                        "combo_index": combo_index,
                        "pair": pair,
                        "domain_1": name1,
                        "domain_2": name2,
                        "branch": branch,
                        "threshold": float(threshold),
                    }
                )
                combo_index += 1
    return pd.DataFrame(rows)


def write_manifest(paths: dict[str, Path]) -> pd.DataFrame:
    manifest = build_combo_manifest()
    manifest.to_csv(paths["manifest"], index=False)
    print(f"Wrote combo manifest: {paths['manifest']} ({len(manifest)} rows)")
    return manifest


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


def prepare_branch_outputs(
    table: pd.DataFrame,
    threshold: float,
    branch: str,
    clr_distance_strategy: str = DEFAULT_CLR_DISTANCE_STRATEGY,
) -> dict:
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
        if clr_distance_strategy == "direct_aitchison":
            distance = euclidean_distance_matrix(transformed)
            embedding = pca_embedding(transformed, N_COMPONENTS)
            distance_metric = "euclidean"
            ordination_method = "pca"
        elif clr_distance_strategy == "pca10":
            reduced = pca_embedding(transformed, N_COMPONENTS)
            distance = euclidean_distance_matrix(pd.DataFrame(reduced, index=transformed.index))
            embedding = reduced
            distance_metric = "euclidean_pca10"
            ordination_method = "pca10"
        else:
            raise ValueError(f"Unsupported CLR distance strategy: {clr_distance_strategy}")
    else:
        raise ValueError(f"Unsupported branch: {branch}")

    return {
        "transformed": transformed,
        "distance": distance,
        "embedding": embedding,
        "distance_metric": distance_metric,
        "ordination_method": ordination_method,
        "n_features": int(filtered.shape[1]),
        "clr_distance_strategy": clr_distance_strategy if branch == "CLR" else "jaccard_presence_absence",
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


def _nonnegative_errorbars(estimate: np.ndarray, lower: np.ndarray, upper: np.ndarray) -> np.ndarray:
    lower_err = np.maximum(0.0, estimate - lower)
    upper_err = np.maximum(0.0, upper - estimate)
    return np.vstack([lower_err, upper_err])


def make_figures(summary_df: pd.DataFrame, paths: dict[str, Path]) -> None:
    import matplotlib.pyplot as plt

    plot_df = summary_df.copy()
    plot_df["label"] = plot_df["pair"] + " | " + plot_df["branch"]

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
    ax.set_title("Phase 5A: Mantel effect sizes with conservative 95% CI")
    fig.tight_layout()
    fig.savefig(paths["fig_mantel"], dpi=180)
    plt.close(fig)

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
    ax.set_title("Phase 5A: Procrustes effect sizes with conservative 95% CI")
    fig.tight_layout()
    fig.savefig(paths["fig_procrustes"], dpi=180)
    plt.close(fig)

    rank_df = plot_df.sort_values(["rank_overall", "mantel_spearman_mean"], ascending=[True, False]).reset_index(drop=True)
    rank_df["overall_score"] = rank_df["rank_overall"].astype(float)
    fig, ax = plt.subplots(figsize=(11, 5))
    x2 = np.arange(len(rank_df))
    ax.bar(x2, rank_df["overall_score"], color="#9467bd", alpha=0.9)
    ax.set_xticks(x2)
    ax.set_xticklabels(rank_df["label"], rotation=30, ha="right")
    ax.set_ylabel("Overall rank (lower is stronger)")
    ax.set_title("Phase 5A: Domain-pair rankings (Mantel + Procrustes)")
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(paths["fig_rankings"], dpi=180)
    plt.close(fig)


def load_tables() -> tuple[list[str], dict[str, pd.DataFrame]]:
    cohort = pd.read_csv(COHORT_FILE)["Sample_ID"].astype(str).tolist()
    tables = {name: align_samples(load_otu_table(name), cohort) for name in ["AMF", "BAC", "EUK", "ITS"]}

    for domain, table in tables.items():
        missing_rows = table.index[table.isnull().all(axis=1)].tolist()
        if missing_rows:
            raise ValueError(f"Domain {domain} missing cohort samples: {missing_rows[:5]}")
    return cohort, tables


def combo_seed(combo_index: int) -> int:
    return int(RANDOM_SEED + combo_index * 10007)


def compute_combo_result(
    combo_index: int,
    pair: str,
    domain_1: str,
    domain_2: str,
    branch: str,
    threshold: float,
    cohort: list[str],
    tables: dict[str, pd.DataFrame],
    clr_distance_strategy: str,
) -> dict:
    combo_label = f"combo={combo_index}, pair={pair}, branch={branch}, threshold={threshold}"
    print(f"[START] {combo_label}")

    seed = combo_seed(combo_index)
    perm_rng = np.random.default_rng(seed)
    boot_rng = np.random.default_rng(seed + 1)

    out1 = prepare_branch_outputs(tables[domain_1], threshold, branch, clr_distance_strategy=clr_distance_strategy)
    out2 = prepare_branch_outputs(tables[domain_2], threshold, branch, clr_distance_strategy=clr_distance_strategy)

    obs_mantel, p_perm = mantel_permutation_pvalue(
        out1["distance"],
        out2["distance"],
        perm_rng,
        N_PERMUTATIONS,
        progress_label=combo_label,
    )
    obs_proc = compute_procrustes(out1["embedding"], out2["embedding"])

    mantel_boot, proc_boot = bootstrap_metrics(
        tables[domain_1],
        tables[domain_2],
        threshold,
        branch,
        boot_rng,
        N_BOOTSTRAPS,
        progress_label=combo_label,
    )

    m_lo, m_hi = ci95(mantel_boot)
    p_lo, p_hi = ci95(proc_boot)

    row = {
        "combo_index": int(combo_index),
        "pair": pair,
        "domain_1": domain_1,
        "domain_2": domain_2,
        "branch": branch,
        "threshold": float(threshold),
        "n_samples": int(len(cohort)),
        "distance_metric": out1["distance_metric"],
        "ordination_method": out1["ordination_method"],
        "n_features_1": int(out1["n_features"]),
        "n_features_2": int(out2["n_features"]),
        "clr_distance_strategy": out1["clr_distance_strategy"],
        "mantel_spearman": float(obs_mantel),
        "mantel_perm_pvalue": float(p_perm),
        "mantel_bootstrap_median": float(np.nanmedian(mantel_boot)),
        "mantel_bootstrap_sd": float(np.nanstd(mantel_boot, ddof=1)),
        "mantel_ci_lower": float(m_lo),
        "mantel_ci_upper": float(m_hi),
        "procrustes_fit": float(obs_proc),
        "procrustes_bootstrap_mean": float(np.nanmean(proc_boot)),
        "procrustes_bootstrap_median": float(np.nanmedian(proc_boot)),
        "procrustes_bootstrap_sd": float(np.nanstd(proc_boot, ddof=1)),
        "procrustes_ci_lower": float(p_lo),
        "procrustes_ci_upper": float(p_hi),
        "n_permutations": int(N_PERMUTATIONS),
        "n_bootstraps": int(N_BOOTSTRAPS),
        "seed": int(seed),
    }
    print(f"[DONE] {combo_label}")
    return row


def checkpoint_path(paths: dict[str, Path], combo_index: int) -> Path:
    return paths["checkpoints_dir"] / f"combo_{combo_index}.csv"


def write_single_checkpoint(paths: dict[str, Path], row: dict, overwrite: bool = False) -> Path:
    ckpt = checkpoint_path(paths, int(row["combo_index"]))
    if ckpt.exists() and not overwrite:
        raise FileExistsError(
            f"Checkpoint already exists and overwrite is disabled: {ckpt}. "
            "Delete it first if you want to recompute this combo."
        )
    pd.DataFrame([row]).to_csv(ckpt, index=False)
    print(f"Wrote checkpoint: {ckpt}")
    return ckpt


def split_outputs(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    mantel_cols = [
        "pair", "branch", "threshold", "n_samples", "distance_metric", "ordination_method", "clr_distance_strategy",
        "n_features_1", "n_features_2", "mantel_spearman", "mantel_perm_pvalue",
        "mantel_bootstrap_median", "mantel_bootstrap_sd", "mantel_ci_lower", "mantel_ci_upper",
        "n_permutations", "n_bootstraps", "seed",
    ]
    proc_cols = [
        "pair", "branch", "threshold", "procrustes_fit", "procrustes_bootstrap_mean",
        "procrustes_bootstrap_median", "procrustes_bootstrap_sd", "procrustes_ci_lower",
        "procrustes_ci_upper", "n_bootstraps", "seed",
    ]
    mantel_df = df[mantel_cols].sort_values(["pair", "branch", "threshold"]).reset_index(drop=True)
    proc_df = df[proc_cols].sort_values(["pair", "branch", "threshold"]).reset_index(drop=True)

    merged = mantel_df.merge(
        proc_df,
        on=["pair", "branch", "threshold", "n_bootstraps", "seed"],
        how="inner",
    )
    summary = build_summary(merged)
    rank_summary = summary[
        [
            "pair",
            "branch",
            "rank_mantel",
            "rank_procrustes_similarity",
            "rank_overall",
            "mantel_spearman_mean",
            "procrustes_similarity_mean",
        ]
    ].sort_values(["rank_overall", "mantel_spearman_mean"], ascending=[True, False]).reset_index(drop=True)

    return mantel_df, proc_df, summary, rank_summary


def write_final_outputs(paths: dict[str, Path], df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    mantel_df, proc_df, summary, rank_summary = split_outputs(df)

    mantel_df.to_csv(paths["mantel"], index=False)
    proc_df.to_csv(paths["procrustes"], index=False)
    summary.to_csv(paths["summary"], index=False)
    rank_summary.to_csv(paths["rank"], index=False)
    make_figures(summary, paths)

    print(f"Wrote {paths['mantel']}")
    print(f"Wrote {paths['procrustes']}")
    print(f"Wrote {paths['summary']}")
    print(f"Wrote {paths['rank']}")
    print(f"Wrote figures to {paths['fig_dir']}")
    return mantel_df, proc_df, summary, rank_summary


def combine_checkpoints(paths: dict[str, Path]) -> None:
    ckpts = sorted(paths["checkpoints_dir"].glob("combo_*.csv"))
    if not ckpts:
        raise FileNotFoundError(f"No checkpoint files found in {paths['checkpoints_dir']}")

    frames = [pd.read_csv(p) for p in ckpts]
    combined = pd.concat(frames, ignore_index=True)

    if "combo_index" not in combined.columns:
        raise ValueError("Checkpoint files are missing combo_index column")

    if paths["manifest"].exists():
        manifest = pd.read_csv(paths["manifest"])
        expected = set(manifest["combo_index"].astype(int).tolist())
        seen = set(combined["combo_index"].astype(int).tolist())
        missing = sorted(expected - seen)
        if missing:
            raise RuntimeError(
                f"Missing checkpoint combos: {missing[:10]}"
                + (" ..." if len(missing) > 10 else "")
                + f" (missing {len(missing)} of {len(expected)})"
            )

    if combined["combo_index"].duplicated().any():
        dupes = combined.loc[combined["combo_index"].duplicated(), "combo_index"].astype(int).tolist()
        raise RuntimeError(f"Duplicate combo_index rows detected in checkpoints: {dupes[:10]}")

    write_final_outputs(paths, combined)


def run_single_combo(paths: dict[str, Path], combo_index: int, clr_distance_strategy: str) -> Path:
    manifest = build_combo_manifest()
    if combo_index < 0 or combo_index >= len(manifest):
        raise IndexError(f"combo_index out of range: {combo_index}; expected 0..{len(manifest)-1}")

    cohort, tables = load_tables()
    combo = manifest.loc[manifest["combo_index"] == combo_index].iloc[0]

    row = compute_combo_result(
        combo_index=int(combo["combo_index"]),
        pair=str(combo["pair"]),
        domain_1=str(combo["domain_1"]),
        domain_2=str(combo["domain_2"]),
        branch=str(combo["branch"]),
        threshold=float(combo["threshold"]),
        cohort=cohort,
        tables=tables,
        clr_distance_strategy=clr_distance_strategy,
    )
    return write_single_checkpoint(paths, row, overwrite=False)


def run_full_serial(paths: dict[str, Path], clr_distance_strategy: str) -> None:
    manifest = build_combo_manifest()
    cohort, tables = load_tables()

    rows = []
    total = len(manifest)
    for i, combo in manifest.iterrows():
        combo_index = int(combo["combo_index"])
        start = time.perf_counter()
        print(f"[COMBO {i+1}/{total}] index={combo_index}")
        rows.append(
            compute_combo_result(
                combo_index=combo_index,
                pair=str(combo["pair"]),
                domain_1=str(combo["domain_1"]),
                domain_2=str(combo["domain_2"]),
                branch=str(combo["branch"]),
                threshold=float(combo["threshold"]),
                cohort=cohort,
                tables=tables,
                clr_distance_strategy=clr_distance_strategy,
            )
        )
        elapsed = time.perf_counter() - start
        print(f"[COMBO {i+1}/{total}] Completed in {elapsed:.2f}s")

    write_final_outputs(paths, pd.DataFrame(rows))


def render_figures_from_existing_outputs(summary_csv: Path, paths: dict[str, Path]) -> None:
    ensure_dirs(paths)
    summary = pd.read_csv(summary_csv)
    make_figures(summary, paths)
    print(f"Figures rendered from existing summary: {summary_csv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 5A BAC coupling inference and HPC checkpoint workflow")
    parser.add_argument("--write-manifest", action="store_true", help="Write combo manifest CSV and exit if no other mode is selected.")
    parser.add_argument("--single-combo", action="store_true", help="Run a single combo and write one checkpoint file.")
    parser.add_argument("--combo-index", type=int, default=None, help="Manifest combo index (0-based) for --single-combo.")
    parser.add_argument("--combine-checkpoints", action="store_true", help="Combine checkpoint files into final CSV outputs and figures.")
    parser.add_argument("--output-dir", default=RESULTS_DIR, help="Output directory for manifests, checkpoints, final CSVs, and figures.")
    parser.add_argument("--figures-only", action="store_true", help="Skip inference and render figures from an existing summary CSV.")
    parser.add_argument("--summary-csv", default=None, help="Summary CSV path used when --figures-only is set.")
    parser.add_argument("--clr-distance-strategy", choices=VALID_CLR_DISTANCE_STRATEGIES, default=DEFAULT_CLR_DISTANCE_STRATEGY, help="CLR branch distance strategy: direct_aitchison (default) or pca10 sensitivity.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = output_paths(Path(args.output_dir))
    ensure_dirs(paths)

    did_anything = False

    if args.write_manifest:
        write_manifest(paths)
        did_anything = True

    if args.figures_only:
        summary_csv = Path(args.summary_csv) if args.summary_csv else paths["summary"]
        render_figures_from_existing_outputs(summary_csv, paths)
        did_anything = True

    if args.single_combo:
        if args.combo_index is None:
            raise ValueError("--single-combo requires --combo-index")
        run_single_combo(paths, args.combo_index, clr_distance_strategy=args.clr_distance_strategy)
        did_anything = True

    if args.combine_checkpoints:
        combine_checkpoints(paths)
        did_anything = True

    if not did_anything:
        run_full_serial(paths, clr_distance_strategy=args.clr_distance_strategy)


if __name__ == "__main__":
    main()
