"""
Phase 5B Environmental Drivers

Resumable HPC-oriented dbRDA-style workflow for approved Phase 5B predictors.

Modes:
- --write-manifest: write 8-row pair×branch combo manifest.
- --single-combo --combo-index N: run exactly one combo and write one checkpoint CSV.
- --combine-checkpoints: combine all checkpoint CSVs into final outputs.
- (no mode flags): run full serial workflow locally.

Policy constraints:
- Primary predictors: pH_KCl, N_pct, bio12now.100, alpha, compl
- Sensitivity extension only: + lat, lon
- Exclusions enforced: PC1..PC4, beta.perc, compl.perc, pool, dark, gamma
- N_pct and C_pct cannot be used together.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

DATA_DIR = Path("data")
COHORT_FILE = Path("results/phase2_confirmatory_coupling/sample_cohort_used.csv")
DEFAULT_OUTPUT_DIR = Path("results/phase5b_environmental_drivers")

DEFAULT_PAIRS = ["BAC↔ITS", "AMF↔ITS", "EUK↔ITS", "AMF↔EUK"]
DEFAULT_BRANCHES = ["presence/absence", "CLR"]
DEFAULT_THRESHOLD = 0.05
DEFAULT_PERMUTATIONS = 499
BASE_RANDOM_SEED = 20260602

PRIMARY_PREDICTORS = ["pH_KCl", "N_pct", "bio12now.100", "alpha", "compl"]
GEOGRAPHY_PREDICTORS = ["lat", "lon"]

FORBIDDEN_PREDICTORS = {
    "PC1", "PC2", "PC3", "PC4",
    "beta.perc", "compl.perc",
    "pool", "dark", "gamma",
}

PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10


def output_paths(output_dir: Path) -> dict[str, Path]:
    fig_dir = output_dir / "figures"
    ckpt_dir = output_dir / "checkpoints"
    return {
        "output_dir": output_dir,
        "fig_dir": fig_dir,
        "checkpoints_dir": ckpt_dir,
        "combo_manifest": output_dir / "phase5b_combo_manifest.csv",
        "summary": output_dir / "phase5b_dbRDA_summary.csv",
        "ranking": output_dir / "phase5b_predictor_ranking.csv",
        "pair_rankings": output_dir / "phase5b_pair_rankings.csv",
        "manifest": output_dir / "phase5b_manifest.csv",
        "metadata": output_dir / "phase5b_run_metadata.json",
        "fig_combo_adj_r2": fig_dir / "phase5b_combo_adjusted_r2.png",
        "fig_pair_rankings": fig_dir / "phase5b_pair_rankings.png",
    }


def ensure_dirs(paths: dict[str, Path]) -> None:
    paths["output_dir"].mkdir(parents=True, exist_ok=True)
    paths["fig_dir"].mkdir(parents=True, exist_ok=True)
    paths["checkpoints_dir"].mkdir(parents=True, exist_ok=True)


def normalize_pair_label(pair_label: str) -> str:
    return pair_label.replace("↔️", "↔").strip()


def parse_pair(pair_str: str) -> tuple[str, str]:
    pair_str = normalize_pair_label(pair_str)
    parts = pair_str.split("↔")
    if len(parts) != 2:
        raise ValueError(f"Pair must look like DOMAIN↔DOMAIN, got: {pair_str}")
    return parts[0].strip(), parts[1].strip()


def build_combo_manifest(threshold: float = DEFAULT_THRESHOLD) -> pd.DataFrame:
    rows = []
    combo_index = 0
    for pair in DEFAULT_PAIRS:
        d1, d2 = parse_pair(pair)
        for branch in DEFAULT_BRANCHES:
            rows.append(
                {
                    "combo_index": int(combo_index),
                    "pair": pair,
                    "domain_1": d1,
                    "domain_2": d2,
                    "branch": branch,
                    "threshold": float(threshold),
                }
            )
            combo_index += 1
    return pd.DataFrame(rows)


def write_combo_manifest(paths: dict[str, Path], threshold: float = DEFAULT_THRESHOLD) -> pd.DataFrame:
    manifest = build_combo_manifest(threshold=threshold)
    manifest.to_csv(paths["combo_manifest"], index=False)
    print(f"Wrote combo manifest: {paths['combo_manifest']} ({len(manifest)} rows)")
    return manifest


def validate_predictor_policy(predictors: Iterable[str]) -> None:
    predictors = list(predictors)
    forbidden = sorted(set(predictors).intersection(FORBIDDEN_PREDICTORS))
    if forbidden:
        raise ValueError(f"Forbidden predictors present: {forbidden}")
    if "N_pct" in predictors and "C_pct" in predictors:
        raise ValueError("Policy violation: cannot include both N_pct and C_pct")


def load_otu_table(domain: str) -> pd.DataFrame:
    path = DATA_DIR / f"{domain}_OTU_table_final.tsv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="\t", index_col=0)


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
    out = np.log(vals / gm)
    return pd.DataFrame(out, index=rel_table.index, columns=rel_table.columns)


def pca_table(table: pd.DataFrame, n_components: int = N_COMPONENTS) -> pd.DataFrame:
    vals = table.to_numpy(dtype=np.float64)
    n_comp = min(n_components, vals.shape[0] - 1, vals.shape[1])
    if n_comp < 1:
        n_comp = 1
    vals = vals - vals.mean(axis=0, keepdims=True)
    u, s, _ = np.linalg.svd(vals, full_matrices=False)
    coords = u[:, :n_comp] * s[:n_comp]
    cols = [f"PC{i+1}" for i in range(coords.shape[1])]
    return pd.DataFrame(coords, index=table.index, columns=cols)


def branch_distance(table: pd.DataFrame, branch: str) -> np.ndarray:
    if branch == "presence/absence":
        binary = to_presence_absence(table)
        return pdist(binary.to_numpy(dtype=np.float64), metric="jaccard")
    if branch == "CLR":
        rel = to_relative_abundance(table)
        clr = clr_transform(rel)
        reduced = pca_table(clr)
        return pdist(reduced.to_numpy(dtype=np.float64), metric="euclidean")
    raise ValueError(f"Unsupported branch: {branch}")


def combined_pair_distance(table_a: pd.DataFrame, table_b: pd.DataFrame, branch: str) -> np.ndarray:
    d_a = branch_distance(table_a, branch)
    d_b = branch_distance(table_b, branch)
    D_a = squareform(d_a)
    D_b = squareform(d_b)
    D = 0.5 * (D_a + D_b)
    return squareform(D, checks=False)


def pcoa_coords(distance_condensed: np.ndarray, max_axes: int = 12) -> np.ndarray:
    D = squareform(distance_condensed)
    n = D.shape[0]
    J = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * J @ (D ** 2) @ J
    eigvals, eigvecs = np.linalg.eigh(B)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    pos = eigvals > 1e-10
    eigvals = eigvals[pos]
    eigvecs = eigvecs[:, pos]
    if eigvals.size == 0:
        return np.zeros((n, 1), dtype=float)
    k = min(max_axes, eigvals.size)
    return eigvecs[:, :k] * np.sqrt(eigvals[:k])


def fit_multivariate_r2(Y: np.ndarray, X: np.ndarray) -> tuple[float, float, float]:
    n = Y.shape[0]
    p = X.shape[1]
    X1 = np.column_stack([np.ones(n), X])
    coef, *_ = np.linalg.lstsq(X1, Y, rcond=None)
    Y_hat = X1 @ coef

    sse = float(((Y - Y_hat) ** 2).sum())
    y_centered = Y - Y.mean(axis=0, keepdims=True)
    sst = float((y_centered ** 2).sum())
    if sst <= 0:
        return 0.0, 0.0, 0.0

    r2 = max(0.0, min(1.0, 1.0 - sse / sst))
    if n - p - 1 > 0:
        adj_r2 = 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1)
    else:
        adj_r2 = np.nan

    if p > 0 and (n - p - 1) > 0 and r2 < 1.0:
        pseudo_f = (r2 / p) / ((1.0 - r2) / (n - p - 1))
    elif r2 >= 1.0:
        pseudo_f = np.inf
    else:
        pseudo_f = np.nan
    return r2, adj_r2, pseudo_f


def permutation_pvalue(Y: np.ndarray, X: np.ndarray, n_perm: int, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    _, _, f_obs = fit_multivariate_r2(Y, X)
    if n_perm <= 0:
        return 1.0, f_obs

    count = 0
    n = X.shape[0]
    for _ in range(n_perm):
        idx = rng.permutation(n)
        _, _, f_perm = fit_multivariate_r2(Y, X[idx, :])
        if np.isfinite(f_obs) and np.isfinite(f_perm) and f_perm >= f_obs:
            count += 1
        elif np.isinf(f_obs) and np.isinf(f_perm):
            count += 1
    p = (count + 1) / (n_perm + 1)
    return p, f_obs


def rank_predictors(Y: np.ndarray, X_df: pd.DataFrame) -> pd.DataFrame:
    full_r2, full_adj_r2, _ = fit_multivariate_r2(Y, X_df.to_numpy(dtype=float))
    rows = []
    for pred in X_df.columns:
        reduced_cols = [c for c in X_df.columns if c != pred]
        if reduced_cols:
            r2_red, adj_r2_red, _ = fit_multivariate_r2(Y, X_df[reduced_cols].to_numpy(dtype=float))
        else:
            r2_red, adj_r2_red = 0.0, 0.0
        rows.append(
            {
                "predictor": pred,
                "full_r2": full_r2,
                "reduced_r2": r2_red,
                "delta_r2": full_r2 - r2_red,
                "full_adj_r2": full_adj_r2,
                "reduced_adj_r2": adj_r2_red,
                "delta_adj_r2": full_adj_r2 - adj_r2_red,
            }
        )
    out = pd.DataFrame(rows)
    return out.sort_values("delta_r2", ascending=False).reset_index(drop=True)


def load_metadata(sample_ids: list[str], predictors: list[str]) -> pd.DataFrame:
    meta = pd.read_csv(DATA_DIR / "Final_data_with_diversity_prefixed.csv", low_memory=False)
    if "canonical" not in meta.columns:
        raise ValueError("Expected 'canonical' in metadata")
    meta = meta.set_index("canonical")

    missing_predictors = [c for c in predictors if c not in meta.columns]
    if missing_predictors:
        raise ValueError(f"Missing predictors in metadata: {missing_predictors}")

    X = meta.reindex(sample_ids)[predictors].apply(pd.to_numeric, errors="coerce")
    X = X.dropna(axis=0)
    if X.empty:
        raise ValueError("No samples left after predictor NA filtering")
    return X


def combo_seed(combo_index: int) -> int:
    return int(BASE_RANDOM_SEED + combo_index * 10007)


def run_pair_branch(
    pair_label: str,
    branch: str,
    threshold: float,
    predictors: list[str],
    permutations: int,
    seed: int,
) -> tuple[dict, pd.DataFrame]:
    d1, d2 = parse_pair(pair_label)

    cohort = pd.read_csv(COHORT_FILE)
    sample_ids = cohort["Sample_ID"].astype(str).tolist()

    t1 = load_otu_table(d1).reindex(sample_ids)
    t2 = load_otu_table(d2).reindex(sample_ids)
    if t1.isnull().all(axis=1).any() or t2.isnull().all(axis=1).any():
        raise ValueError(f"Missing cohort samples for pair {pair_label}")

    t1 = prevalence_filter_table(t1, threshold)
    t2 = prevalence_filter_table(t2, threshold)

    X = load_metadata(sample_ids, predictors)
    common_ids = X.index.tolist()
    t1 = t1.reindex(common_ids)
    t2 = t2.reindex(common_ids)

    d_combined = combined_pair_distance(t1, t2, branch)
    Y = pcoa_coords(d_combined)

    X_arr = X.to_numpy(dtype=float)
    r2, adj_r2, _ = fit_multivariate_r2(Y, X_arr)
    p_perm, pseudo_f_obs = permutation_pvalue(Y, X_arr, permutations, seed)
    ranking = rank_predictors(Y, X)

    summary = {
        "pair": pair_label,
        "branch": branch,
        "threshold": float(threshold),
        "n_samples": int(len(common_ids)),
        "n_features_domain1": int(t1.shape[1]),
        "n_features_domain2": int(t2.shape[1]),
        "n_predictors": int(len(predictors)),
        "predictor_set": ",".join(predictors),
        "r2": float(r2),
        "adjusted_r2": float(adj_r2),
        "pseudo_f": float(pseudo_f_obs),
        "permutation_p": float(p_perm),
        "permutations": int(permutations),
    }
    ranking.insert(0, "branch", branch)
    ranking.insert(0, "pair", pair_label)
    return summary, ranking


def checkpoint_path(paths: dict[str, Path], combo_index: int) -> Path:
    return paths["checkpoints_dir"] / f"combo_{combo_index}.csv"


def combo_to_checkpoint_rows(
    combo_index: int,
    pair: str,
    branch: str,
    threshold: float,
    permutations: int,
) -> pd.DataFrame:
    seed = combo_seed(combo_index)

    validate_predictor_policy(PRIMARY_PREDICTORS)
    sensitivity_predictors = list(PRIMARY_PREDICTORS) + list(GEOGRAPHY_PREDICTORS)
    validate_predictor_policy(sensitivity_predictors)

    all_rows: list[dict] = []
    models = [
        ("primary", list(PRIMARY_PREDICTORS), seed),
        ("geography_sensitivity", sensitivity_predictors, seed + 1),
    ]

    for model_type, predictors, model_seed in models:
        summary, ranking = run_pair_branch(
            pair_label=pair,
            branch=branch,
            threshold=threshold,
            predictors=predictors,
            permutations=permutations,
            seed=model_seed,
        )

        summary_row = {
            "record_type": "summary",
            "combo_index": int(combo_index),
            "pair": pair,
            "branch": branch,
            "threshold": float(threshold),
            "model_type": model_type,
            "seed": int(model_seed),
            **summary,
            "predictor": "",
            "full_r2": np.nan,
            "reduced_r2": np.nan,
            "delta_r2": np.nan,
            "full_adj_r2": np.nan,
            "reduced_adj_r2": np.nan,
            "delta_adj_r2": np.nan,
        }
        all_rows.append(summary_row)

        for _, rr in ranking.iterrows():
            all_rows.append(
                {
                    "record_type": "predictor_ranking",
                    "combo_index": int(combo_index),
                    "pair": pair,
                    "branch": branch,
                    "threshold": float(threshold),
                    "model_type": model_type,
                    "seed": int(model_seed),
                    **summary,
                    "predictor": str(rr["predictor"]),
                    "full_r2": float(rr["full_r2"]),
                    "reduced_r2": float(rr["reduced_r2"]),
                    "delta_r2": float(rr["delta_r2"]),
                    "full_adj_r2": float(rr["full_adj_r2"]),
                    "reduced_adj_r2": float(rr["reduced_adj_r2"]),
                    "delta_adj_r2": float(rr["delta_adj_r2"]),
                }
            )

    return pd.DataFrame(all_rows)


def write_single_checkpoint(paths: dict[str, Path], combo_index: int, rows_df: pd.DataFrame, overwrite: bool = False) -> Path:
    ckpt = checkpoint_path(paths, combo_index)
    if ckpt.exists() and not overwrite:
        raise FileExistsError(
            f"Checkpoint exists and overwrite is disabled: {ckpt}. Delete it to recompute."
        )
    rows_df.to_csv(ckpt, index=False)
    print(f"Wrote checkpoint: {ckpt} ({len(rows_df)} rows)")
    return ckpt


def run_single_combo(paths: dict[str, Path], combo_index: int, threshold: float, permutations: int) -> Path:
    manifest = build_combo_manifest(threshold=threshold)
    if combo_index < 0 or combo_index >= len(manifest):
        raise IndexError(f"combo_index out of range: {combo_index}; expected 0..{len(manifest)-1}")

    combo = manifest.loc[manifest["combo_index"] == combo_index].iloc[0]
    pair = normalize_pair_label(str(combo["pair"]))
    branch = str(combo["branch"])
    threshold = float(combo["threshold"])

    print(f"Running single combo index={combo_index}, pair={pair}, branch={branch}, threshold={threshold}")
    start = time.time()
    rows_df = combo_to_checkpoint_rows(
        combo_index=combo_index,
        pair=pair,
        branch=branch,
        threshold=threshold,
        permutations=permutations,
    )
    ckpt = write_single_checkpoint(paths, combo_index, rows_df, overwrite=False)
    elapsed = time.time() - start
    print(f"Single combo runtime_seconds={elapsed:.3f}")
    return ckpt


def split_combined_outputs(combined: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary_df = (
        combined[combined["record_type"] == "summary"]
        .copy()
        .sort_values(["pair", "branch", "model_type"])
        .reset_index(drop=True)
    )

    ranking_df = (
        combined[combined["record_type"] == "predictor_ranking"]
        .copy()
        .sort_values(["pair", "branch", "model_type", "delta_r2"], ascending=[True, True, True, False])
        .reset_index(drop=True)
    )

    pair_rankings = (
        summary_df.groupby(["pair", "model_type"], as_index=False)
        .agg(
            mean_adjusted_r2=("adjusted_r2", "mean"),
            min_permutation_p=("permutation_p", "min"),
            max_permutation_p=("permutation_p", "max"),
            mean_r2=("r2", "mean"),
        )
        .sort_values(["model_type", "mean_adjusted_r2"], ascending=[True, False])
        .reset_index(drop=True)
    )
    pair_rankings["rank_within_model"] = pair_rankings.groupby("model_type")["mean_adjusted_r2"].rank(
        ascending=False, method="min"
    ).astype(int)

    return summary_df, ranking_df, pair_rankings


def make_figures(summary_df: pd.DataFrame, pair_rankings: pd.DataFrame, paths: dict[str, Path]) -> None:
    import matplotlib.pyplot as plt

    if summary_df.empty:
        raise ValueError("Cannot render figures: summary_df is empty")

    s = summary_df.copy()
    s["label"] = s["pair"] + " | " + s["branch"]

    fig, ax = plt.subplots(figsize=(12, 5))
    x = np.arange(len(s))
    colors = ["#1f77b4" if mt == "primary" else "#ff7f0e" for mt in s["model_type"]]
    ax.bar(x, s["adjusted_r2"], color=colors, alpha=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(s["label"], rotation=30, ha="right")
    ax.set_ylabel("Adjusted R²")
    ax.set_title("Phase 5B: Combo-level adjusted R²")
    fig.tight_layout()
    fig.savefig(paths["fig_combo_adj_r2"], dpi=180)
    plt.close(fig)

    pr = pair_rankings.copy()
    pr["label"] = pr["pair"] + " | " + pr["model_type"]
    fig, ax = plt.subplots(figsize=(10, 5))
    x2 = np.arange(len(pr))
    ax.bar(x2, pr["mean_adjusted_r2"], color="#2ca02c", alpha=0.9)
    ax.set_xticks(x2)
    ax.set_xticklabels(pr["label"], rotation=30, ha="right")
    ax.set_ylabel("Mean adjusted R²")
    ax.set_title("Phase 5B: Pair rankings")
    fig.tight_layout()
    fig.savefig(paths["fig_pair_rankings"], dpi=180)
    plt.close(fig)

    print(f"Wrote figures: {paths['fig_combo_adj_r2']}, {paths['fig_pair_rankings']}")


def combine_checkpoints(paths: dict[str, Path], threshold: float, render_figures: bool = True) -> None:
    ckpts = sorted(paths["checkpoints_dir"].glob("combo_*.csv"))
    if not ckpts:
        raise FileNotFoundError(f"No checkpoints found in {paths['checkpoints_dir']}")

    manifest = build_combo_manifest(threshold=threshold)
    expected = set(manifest["combo_index"].astype(int).tolist())

    frames = [pd.read_csv(p) for p in ckpts]
    combined = pd.concat(frames, ignore_index=True)

    if "combo_index" not in combined.columns or "record_type" not in combined.columns:
        raise ValueError("Checkpoint schema invalid: expected combo_index and record_type columns")

    seen = set(combined["combo_index"].astype(int).tolist())
    missing = sorted(expected - seen)
    if missing:
        raise RuntimeError(
            f"Missing checkpoint combos: {missing} (missing {len(missing)} of {len(expected)}). "
            "Run remaining single-combo jobs first."
        )

    summary_df, ranking_df, pair_rankings = split_combined_outputs(combined)

    summary_df.to_csv(paths["summary"], index=False)
    ranking_df.to_csv(paths["ranking"], index=False)
    pair_rankings.to_csv(paths["pair_rankings"], index=False)
    manifest.to_csv(paths["manifest"], index=False)

    run_meta = {
        "analysis": "phase5b_environmental_drivers",
        "generated_at_epoch": time.time(),
        "n_checkpoints": len(ckpts),
        "n_summary_rows": int(len(summary_df)),
        "n_ranking_rows": int(len(ranking_df)),
        "n_pair_rankings_rows": int(len(pair_rankings)),
        "expected_combos": int(len(expected)),
        "permutations_present": sorted({int(x) for x in summary_df["permutations"].dropna().tolist()}),
        "output_files": {
            "summary": str(paths["summary"]),
            "ranking": str(paths["ranking"]),
            "pair_rankings": str(paths["pair_rankings"]),
            "manifest": str(paths["manifest"]),
        },
    }
    paths["metadata"].write_text(json.dumps(run_meta, indent=2))

    if render_figures:
        make_figures(summary_df, pair_rankings, paths)

    print(f"Wrote {paths['summary']}")
    print(f"Wrote {paths['ranking']}")
    print(f"Wrote {paths['pair_rankings']}")
    print(f"Wrote {paths['manifest']}")
    print(f"Wrote {paths['metadata']}")


def run_full_serial(paths: dict[str, Path], threshold: float, permutations: int) -> None:
    manifest = build_combo_manifest(threshold=threshold)
    rows = []
    start_all = time.time()
    for _, combo in manifest.iterrows():
        combo_index = int(combo["combo_index"])
        pair = str(combo["pair"])
        branch = str(combo["branch"])
        t = float(combo["threshold"])
        print(f"[FULL] combo_index={combo_index}, pair={pair}, branch={branch}, threshold={t}")
        rows.append(
            combo_to_checkpoint_rows(
                combo_index=combo_index,
                pair=pair,
                branch=branch,
                threshold=t,
                permutations=permutations,
            )
        )
    elapsed = time.time() - start_all
    combined = pd.concat(rows, ignore_index=True)

    summary_df, ranking_df, pair_rankings = split_combined_outputs(combined)
    summary_df.to_csv(paths["summary"], index=False)
    ranking_df.to_csv(paths["ranking"], index=False)
    pair_rankings.to_csv(paths["pair_rankings"], index=False)
    manifest.to_csv(paths["manifest"], index=False)

    run_meta = {
        "analysis": "phase5b_environmental_drivers",
        "mode": "full_serial",
        "runtime_seconds": elapsed,
        "expected_combos": int(len(manifest)),
        "permutations": int(permutations),
    }
    paths["metadata"].write_text(json.dumps(run_meta, indent=2))
    make_figures(summary_df, pair_rankings, paths)

    print("PHASE5B_DONE")
    print(f"runtime_seconds={elapsed:.3f}")


def render_figures_from_existing_outputs(paths: dict[str, Path]) -> None:
    summary_df = pd.read_csv(paths["summary"])
    pair_rankings = pd.read_csv(paths["pair_rankings"])
    make_figures(summary_df, pair_rankings, paths)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 5B environmental-driver dbRDA-style workflow")
    parser.add_argument("--write-manifest", action="store_true", help="Write 8-row combo manifest and exit if no other mode is selected.")
    parser.add_argument("--single-combo", action="store_true", help="Run one combo (pair+branch) and write one checkpoint.")
    parser.add_argument("--combo-index", type=int, default=None, help="0-based combo index used with --single-combo.")
    parser.add_argument("--combine-checkpoints", action="store_true", help="Combine all combo checkpoints into final outputs.")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory for manifest/checkpoints/final outputs.")
    parser.add_argument("--figures-only", action="store_true", help="Render figures from existing combined outputs only.")
    parser.add_argument("--permutations", type=int, default=DEFAULT_PERMUTATIONS, help="Permutation count (default 499).")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Prevalence threshold used in combo manifest.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = output_paths(Path(args.output_dir))
    ensure_dirs(paths)

    did_anything = False

    if args.write_manifest:
        write_combo_manifest(paths, threshold=args.threshold)
        did_anything = True

    if args.figures_only:
        render_figures_from_existing_outputs(paths)
        did_anything = True

    if args.single_combo:
        if args.combo_index is None:
            raise ValueError("--single-combo requires --combo-index")
        run_single_combo(
            paths=paths,
            combo_index=args.combo_index,
            threshold=args.threshold,
            permutations=args.permutations,
        )
        did_anything = True

    if args.combine_checkpoints:
        combine_checkpoints(paths, threshold=args.threshold, render_figures=True)
        did_anything = True

    if not did_anything:
        run_full_serial(paths, threshold=args.threshold, permutations=args.permutations)


if __name__ == "__main__":
    main()
