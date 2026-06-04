"""
Phase 5C Plant Diversity Hypotheses

Hypothesis-driven dbRDA-style workflow evaluating DarkDivNet biodiversity metrics
against cross-domain microbial coupling, beyond abiotic baseline drivers.

Primary hypothesis model set (A-G):
A: abiotic_base
B: abiotic_base + alpha
C: abiotic_base + dark
D: abiotic_base + pool
E: abiotic_base + compl
F: abiotic_base + alpha + dark
G: abiotic_base + pool + compl

Geography remains sensitivity-only (+lat,+lon); all primary inference should use
model_scope=primary.

Modes:
- --write-manifest
- --single-combo --combo-index N
- --combine-checkpoints
- (no mode flags): full serial run
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
DEFAULT_OUTPUT_DIR = Path("results/phase5c_plant_diversity")

DEFAULT_PAIRS = ["BAC↔ITS", "AMF↔ITS", "EUK↔ITS", "AMF↔EUK"]
DEFAULT_BRANCHES = ["presence/absence", "CLR"]
DEFAULT_THRESHOLD = 0.05
DEFAULT_PERMUTATIONS = 999
DEFAULT_CLR_DISTANCE_STRATEGY = "direct_aitchison"
VALID_CLR_DISTANCE_STRATEGIES = ("direct_aitchison", "pca10")
BASE_RANDOM_SEED = 20260603

ABIOTIC_BASE = ["pH_KCl", "N_pct", "bio12now.100"]
GEOGRAPHY_SENSITIVITY = ["lat", "lon"]

HYPOTHESIS_MODELS: dict[str, dict] = {
    "A": {
        "hypothesis_name": "abiotic_base",
        "predictors": ABIOTIC_BASE,
    },
    "B": {
        "hypothesis_name": "abiotic_plus_alpha",
        "predictors": ABIOTIC_BASE + ["alpha"],
    },
    "C": {
        "hypothesis_name": "abiotic_plus_dark",
        "predictors": ABIOTIC_BASE + ["dark"],
    },
    "D": {
        "hypothesis_name": "abiotic_plus_pool",
        "predictors": ABIOTIC_BASE + ["pool"],
    },
    "E": {
        "hypothesis_name": "abiotic_plus_compl",
        "predictors": ABIOTIC_BASE + ["compl"],
    },
    "F": {
        "hypothesis_name": "abiotic_plus_alpha_dark",
        "predictors": ABIOTIC_BASE + ["alpha", "dark"],
    },
    "G": {
        "hypothesis_name": "abiotic_plus_pool_compl",
        "predictors": ABIOTIC_BASE + ["pool", "compl"],
    },
}

# Explicit exclusions for this phase
FORBIDDEN_PREDICTORS = {
    "PC1", "PC2", "PC3", "PC4",
    "beta", "beta.perc", "compl.perc", "gamma",
}

PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10


def output_paths(output_dir: Path) -> dict[str, Path]:
    fig_dir = output_dir
    ckpt_dir = output_dir / "checkpoints"
    return {
        "output_dir": output_dir,
        "fig_dir": fig_dir,
        "checkpoints_dir": ckpt_dir,
        "combo_manifest": output_dir / "phase5c_combo_manifest.csv",
        "model_comparison": output_dir / "phase5c_model_comparison.csv",
        "predictor_effects": output_dir / "phase5c_predictor_effects.csv",
        "pair_rankings": output_dir / "phase5c_pair_rankings.csv",
        "hypothesis_summary": output_dir / "phase5c_hypothesis_summary.csv",
        "manifest": output_dir / "phase5c_manifest.csv",
        "metadata": output_dir / "phase5c_run_metadata.json",
        "fig_model_delta": fig_dir / "phase5c_model_delta_adj_r2.png",
        "fig_hypothesis_rankings": fig_dir / "phase5c_hypothesis_rankings.png",
        "fig_pair_comparisons": fig_dir / "phase5c_pair_comparisons.png",
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


def build_combo_manifest(
    threshold: float = DEFAULT_THRESHOLD,
    pair_filter: str | None = None,
    branch_filter: str | None = None,
) -> pd.DataFrame:
    rows = []
    combo_index = 0
    for pair in DEFAULT_PAIRS:
        if pair_filter and normalize_pair_label(pair_filter) != normalize_pair_label(pair):
            continue
        d1, d2 = parse_pair(pair)
        for branch in DEFAULT_BRANCHES:
            if branch_filter and branch_filter != branch:
                continue
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


def write_combo_manifest(
    paths: dict[str, Path],
    threshold: float = DEFAULT_THRESHOLD,
    pair_filter: str | None = None,
    branch_filter: str | None = None,
) -> pd.DataFrame:
    manifest = build_combo_manifest(threshold=threshold, pair_filter=pair_filter, branch_filter=branch_filter)
    manifest.to_csv(paths["combo_manifest"], index=False)
    print(f"Wrote combo manifest: {paths['combo_manifest']} ({len(manifest)} rows)")
    return manifest


def validate_predictor_policy(predictors: Iterable[str], model_scope: str, model_id: str) -> None:
    predictors = list(predictors)
    forbidden = sorted(set(predictors).intersection(FORBIDDEN_PREDICTORS))
    if forbidden:
        raise ValueError(f"Forbidden predictors present in model {model_id}/{model_scope}: {forbidden}")
    if "N_pct" in predictors and "C_pct" in predictors:
        raise ValueError("Policy violation: cannot include both N_pct and C_pct")

    # Structural dependency guard (primary only): do not place all 4 together.
    structural_set = {"alpha", "dark", "pool", "compl"}
    if model_scope == "primary" and structural_set.issubset(set(predictors)):
        raise ValueError(
            f"Policy violation in model {model_id}: alpha,dark,pool,compl cannot be in a single primary model"
        )


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


def branch_distance(table: pd.DataFrame, branch: str, clr_distance_strategy: str = DEFAULT_CLR_DISTANCE_STRATEGY) -> np.ndarray:
    if branch == "presence/absence":
        binary = to_presence_absence(table)
        return pdist(binary.to_numpy(dtype=np.float64), metric="jaccard")
    if branch == "CLR":
        rel = to_relative_abundance(table)
        clr = clr_transform(rel)
        if clr_distance_strategy == "direct_aitchison":
            return pdist(clr.to_numpy(dtype=np.float64), metric="euclidean")
        if clr_distance_strategy == "pca10":
            reduced = pca_table(clr)
            return pdist(reduced.to_numpy(dtype=np.float64), metric="euclidean")
        raise ValueError(f"Unsupported CLR distance strategy: {clr_distance_strategy}")
    raise ValueError(f"Unsupported branch: {branch}")


def combined_pair_distance(table_a: pd.DataFrame, table_b: pd.DataFrame, branch: str, clr_distance_strategy: str = DEFAULT_CLR_DISTANCE_STRATEGY) -> np.ndarray:
    d_a = branch_distance(table_a, branch, clr_distance_strategy=clr_distance_strategy)
    d_b = branch_distance(table_b, branch, clr_distance_strategy=clr_distance_strategy)
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
    return out.sort_values("delta_adj_r2", ascending=False).reset_index(drop=True)


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
    return int(BASE_RANDOM_SEED + combo_index * 20011)


def prepare_pair_branch_context(pair_label: str, branch: str, threshold: float, clr_distance_strategy: str) -> dict:
    d1, d2 = parse_pair(pair_label)

    cohort = pd.read_csv(COHORT_FILE)
    sample_ids = cohort["Sample_ID"].astype(str).tolist()

    t1 = load_otu_table(d1).reindex(sample_ids)
    t2 = load_otu_table(d2).reindex(sample_ids)
    if t1.isnull().all(axis=1).any() or t2.isnull().all(axis=1).any():
        raise ValueError(f"Missing cohort samples for pair {pair_label}")

    t1 = prevalence_filter_table(t1, threshold)
    t2 = prevalence_filter_table(t2, threshold)

    # Compute microbial coupling response once per pair×branch combo.
    d_combined = combined_pair_distance(t1, t2, branch, clr_distance_strategy=clr_distance_strategy)
    Y_full = pcoa_coords(d_combined)

    meta = pd.read_csv(DATA_DIR / "Final_data_with_diversity_prefixed.csv", low_memory=False)
    if "canonical" not in meta.columns:
        raise ValueError("Expected 'canonical' in metadata")
    meta = meta.set_index("canonical")

    return {
        "pair": pair_label,
        "branch": branch,
        "threshold": float(threshold),
        "sample_ids": sample_ids,
        "t1": t1,
        "t2": t2,
        "Y_full": Y_full,
        "clr_distance_strategy": clr_distance_strategy if branch == "CLR" else "jaccard_presence_absence",
        "meta": meta,
    }


def evaluate_predictor_set(
    context: dict,
    predictors: list[str],
    permutations: int,
    seed: int,
    clr_distance_strategy: str = DEFAULT_CLR_DISTANCE_STRATEGY,
) -> tuple[dict, pd.DataFrame]:
    meta = context["meta"]
    sample_ids = context["sample_ids"]

    missing_predictors = [c for c in predictors if c not in meta.columns]
    if missing_predictors:
        raise ValueError(f"Missing predictors in metadata: {missing_predictors}")

    X = meta.reindex(sample_ids)[predictors].apply(pd.to_numeric, errors="coerce")
    X = X.dropna(axis=0)
    if X.empty:
        raise ValueError("No samples left after predictor NA filtering")

    common_ids = X.index.tolist()
    # Align Y rows to common_ids using original cohort order
    id_to_idx = {sid: i for i, sid in enumerate(sample_ids)}
    row_idx = [id_to_idx[sid] for sid in common_ids]
    Y = context["Y_full"][row_idx, :]

    # Feature counts after metadata intersection
    t1 = context["t1"].reindex(common_ids)
    t2 = context["t2"].reindex(common_ids)

    X_arr = X.to_numpy(dtype=float)
    r2, adj_r2, _ = fit_multivariate_r2(Y, X_arr)
    p_perm, pseudo_f_obs = permutation_pvalue(Y, X_arr, permutations, seed)
    predictor_effects = rank_predictors(Y, X)

    summary = {
        "pair": context["pair"],
        "branch": context["branch"],
        "threshold": float(context["threshold"]),
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
        "clr_distance_strategy": clr_distance_strategy,
    }

    predictor_effects.insert(0, "branch", context["branch"])
    predictor_effects.insert(0, "pair", context["pair"])
    return summary, predictor_effects


def checkpoint_path(paths: dict[str, Path], combo_index: int) -> Path:
    return paths["checkpoints_dir"] / f"combo_{combo_index}.csv"


def combo_to_checkpoint_rows(
    combo_index: int,
    pair: str,
    branch: str,
    threshold: float,
    permutations: int,
    include_geography_sensitivity: bool,
    clr_distance_strategy: str,
) -> pd.DataFrame:
    seed0 = combo_seed(combo_index)

    # Expensive microbial response calculation done once per combo.
    context = prepare_pair_branch_context(pair_label=pair, branch=branch, threshold=threshold, clr_distance_strategy=clr_distance_strategy)

    scopes = ["primary"]
    if include_geography_sensitivity:
        scopes.append("geography_sensitivity")

    all_rows: list[dict] = []

    for scope_i, model_scope in enumerate(scopes):
        for model_j, (model_id, model_spec) in enumerate(HYPOTHESIS_MODELS.items()):
            predictors = list(model_spec["predictors"])
            if model_scope == "geography_sensitivity":
                predictors = predictors + GEOGRAPHY_SENSITIVITY

            validate_predictor_policy(predictors, model_scope=model_scope, model_id=model_id)
            model_seed = int(seed0 + scope_i * 1000 + model_j)

            summary, effects = evaluate_predictor_set(
                context=context,
                predictors=predictors,
                permutations=permutations,
                seed=model_seed,
                clr_distance_strategy=clr_distance_strategy,
            )

            summary_row = {
                "record_type": "model_summary",
                "combo_index": int(combo_index),
                "pair": pair,
                "branch": branch,
                "threshold": float(threshold),
                "model_scope": model_scope,
                "hypothesis_id": model_id,
                "hypothesis_name": model_spec["hypothesis_name"],
                "seed": model_seed,
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

            for _, erow in effects.iterrows():
                all_rows.append(
                    {
                        "record_type": "predictor_effect",
                        "combo_index": int(combo_index),
                        "pair": pair,
                        "branch": branch,
                        "threshold": float(threshold),
                        "model_scope": model_scope,
                        "hypothesis_id": model_id,
                        "hypothesis_name": model_spec["hypothesis_name"],
                        "seed": model_seed,
                        **summary,
                        "predictor": str(erow["predictor"]),
                        "full_r2": float(erow["full_r2"]),
                        "reduced_r2": float(erow["reduced_r2"]),
                        "delta_r2": float(erow["delta_r2"]),
                        "full_adj_r2": float(erow["full_adj_r2"]),
                        "reduced_adj_r2": float(erow["reduced_adj_r2"]),
                        "delta_adj_r2": float(erow["delta_adj_r2"]),
                    }
                )

    out = pd.DataFrame(all_rows)
    # Derive baseline deltas per combo/scope relative to model A
    if not out.empty:
        summary_mask = out["record_type"] == "model_summary"
        summary_df = out.loc[summary_mask].copy()
        base = summary_df.loc[summary_df["hypothesis_id"] == "A", ["combo_index", "model_scope", "adjusted_r2"]]
        base = base.rename(columns={"adjusted_r2": "baseline_adjusted_r2"})

        out = out.merge(base, on=["combo_index", "model_scope"], how="left")
        out["delta_adjusted_r2_vs_base"] = out["adjusted_r2"] - out["baseline_adjusted_r2"]

    return out


def write_single_checkpoint(paths: dict[str, Path], combo_index: int, rows_df: pd.DataFrame, overwrite: bool = False) -> Path:
    ckpt = checkpoint_path(paths, combo_index)
    if ckpt.exists() and not overwrite:
        raise FileExistsError(
            f"Checkpoint exists and overwrite is disabled: {ckpt}. Delete it to recompute."
        )
    rows_df.to_csv(ckpt, index=False)
    print(f"Wrote checkpoint: {ckpt} ({len(rows_df)} rows)")
    return ckpt


def run_single_combo(
    paths: dict[str, Path],
    combo_index: int,
    threshold: float,
    permutations: int,
    include_geography_sensitivity: bool,
    clr_distance_strategy: str = DEFAULT_CLR_DISTANCE_STRATEGY,
    pair_filter: str | None = None,
    branch_filter: str | None = None,
) -> Path:
    manifest = build_combo_manifest(threshold=threshold, pair_filter=pair_filter, branch_filter=branch_filter)
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
        include_geography_sensitivity=include_geography_sensitivity,
        clr_distance_strategy=clr_distance_strategy,
    )
    ckpt = write_single_checkpoint(paths, combo_index, rows_df, overwrite=False)
    elapsed = time.time() - start
    print(f"Single combo runtime_seconds={elapsed:.3f}")
    return ckpt


def split_outputs(combined: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    model_comparison = (
        combined[combined["record_type"] == "model_summary"]
        .copy()
        .sort_values(["pair", "branch", "model_scope", "hypothesis_id"])
        .reset_index(drop=True)
    )

    predictor_effects = (
        combined[combined["record_type"] == "predictor_effect"]
        .copy()
        .sort_values(["pair", "branch", "model_scope", "hypothesis_id", "delta_adj_r2"], ascending=[True, True, True, True, False])
        .reset_index(drop=True)
    )

    # Best hypothesis per pair×branch (within scope)
    best_per_pair_branch = (
        model_comparison.sort_values(
            ["pair", "branch", "model_scope", "delta_adjusted_r2_vs_base", "adjusted_r2"],
            ascending=[True, True, True, False, False],
        )
        .groupby(["pair", "branch", "model_scope"], as_index=False)
        .head(1)
        .copy()
    )
    best_per_pair_branch["rank_type"] = "best_per_pair_branch"

    # Mean by pair and hypothesis
    mean_pair_hyp = (
        model_comparison.groupby(["pair", "model_scope", "hypothesis_id", "hypothesis_name"], as_index=False)
        .agg(
            mean_delta_adjusted_r2=("delta_adjusted_r2_vs_base", "mean"),
            mean_adjusted_r2=("adjusted_r2", "mean"),
            mean_r2=("r2", "mean"),
            min_permutation_p=("permutation_p", "min"),
            max_permutation_p=("permutation_p", "max"),
        )
        .sort_values(["pair", "model_scope", "mean_delta_adjusted_r2"], ascending=[True, True, False])
        .reset_index(drop=True)
    )
    mean_pair_hyp["rank_type"] = "mean_by_pair_hypothesis"

    pair_rankings = pd.concat([best_per_pair_branch, mean_pair_hyp], ignore_index=True, sort=False)

    primary = model_comparison[model_comparison["model_scope"] == "primary"].copy()
    if primary.empty:
        hypothesis_summary = pd.DataFrame(columns=[
            "summary_type", "hypothesis_id", "hypothesis_name", "mean_delta_adjusted_r2", "mean_adjusted_r2",
            "mean_r2", "n_models", "n_significant", "prop_significant", "overall_rank"
        ])
    else:
        hypothesis_summary = (
            primary.groupby(["hypothesis_id", "hypothesis_name"], as_index=False)
            .agg(
                mean_delta_adjusted_r2=("delta_adjusted_r2_vs_base", "mean"),
                mean_adjusted_r2=("adjusted_r2", "mean"),
                mean_r2=("r2", "mean"),
                n_models=("pair", "count"),
                n_significant=("permutation_p", lambda s: int((s < 0.05).sum())),
            )
            .sort_values("mean_delta_adjusted_r2", ascending=False)
            .reset_index(drop=True)
        )
        hypothesis_summary["prop_significant"] = hypothesis_summary["n_significant"] / hypothesis_summary["n_models"]
        hypothesis_summary["overall_rank"] = np.arange(1, len(hypothesis_summary) + 1)
        hypothesis_summary["summary_type"] = "hypothesis_mean"

        # Explicit hypothesis contrasts requested
        means = dict(zip(hypothesis_summary["hypothesis_id"], hypothesis_summary["mean_delta_adjusted_r2"]))
        contrast_rows = []

        def add_contrast(name: str, lhs: str, rhs: str) -> None:
            if lhs in means and rhs in means:
                contrast_rows.append({
                    "summary_type": "contrast",
                    "hypothesis_id": f"{lhs}_vs_{rhs}",
                    "hypothesis_name": name,
                    "mean_delta_adjusted_r2": float(means[lhs] - means[rhs]),
                    "mean_adjusted_r2": np.nan,
                    "mean_r2": np.nan,
                    "n_models": np.nan,
                    "n_significant": np.nan,
                    "prop_significant": np.nan,
                    "overall_rank": np.nan,
                })

        add_contrast("dark_vs_alpha", "C", "B")
        add_contrast("pool_vs_alpha", "D", "B")
        add_contrast("compl_vs_alpha", "E", "B")
        add_contrast("alpha+dark_vs_alpha", "F", "B")
        add_contrast("pool+compl_vs_pool", "G", "D")

        if contrast_rows:
            hypothesis_summary = pd.concat([hypothesis_summary, pd.DataFrame(contrast_rows)], ignore_index=True)

    return model_comparison, predictor_effects, pair_rankings, hypothesis_summary


def make_figures(
    model_comparison: pd.DataFrame,
    hypothesis_summary: pd.DataFrame,
    pair_rankings: pd.DataFrame,
    paths: dict[str, Path],
) -> None:
    import matplotlib.pyplot as plt

    primary = model_comparison[model_comparison["model_scope"] == "primary"].copy()
    if primary.empty:
        raise ValueError("No primary model rows available for figure generation")

    # Figure 1: delta adj R2 by hypothesis across pair×branch
    m = primary.copy()
    m["label"] = m["pair"] + " | " + m["branch"]
    labels = list(dict.fromkeys(m["label"].tolist()))
    hypothesis_ids = list(HYPOTHESIS_MODELS.keys())

    width = 0.11
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, hid in enumerate(hypothesis_ids):
        vals = []
        for lbl in labels:
            sub = m[(m["label"] == lbl) & (m["hypothesis_id"] == hid)]
            vals.append(float(sub["delta_adjusted_r2_vs_base"].iloc[0]) if not sub.empty else np.nan)
        ax.bar(x + (i - 3) * width, vals, width=width, label=hid)

    ax.axhline(0.0, color="black", linewidth=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Δ adjusted R² vs abiotic_base")
    ax.set_title("Phase 5C: Hypothesis model deltas by pair × branch")
    ax.legend(title="Hypothesis", ncol=4)
    fig.tight_layout()
    fig.savefig(paths["fig_model_delta"], dpi=180)
    plt.close(fig)

    # Figure 2: overall hypothesis ranking
    hs = hypothesis_summary[hypothesis_summary["summary_type"] == "hypothesis_mean"].copy()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(hs["hypothesis_id"], hs["mean_delta_adjusted_r2"], color="#2ca02c", alpha=0.9)
    ax.axhline(0.0, color="black", linewidth=0.9)
    ax.set_xlabel("Hypothesis model")
    ax.set_ylabel("Mean Δ adjusted R²")
    ax.set_title("Phase 5C: Mean hypothesis gains over abiotic_base")
    fig.tight_layout()
    fig.savefig(paths["fig_hypothesis_rankings"], dpi=180)
    plt.close(fig)

    # Figure 3: best hypothesis per pair×branch
    best = pair_rankings[pair_rankings["rank_type"] == "best_per_pair_branch"].copy()
    best["label"] = best["pair"] + " | " + best["branch"]

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(best))
    ax.bar(x, best["delta_adjusted_r2_vs_base"], color="#1f77b4", alpha=0.9)
    for i, hid in enumerate(best["hypothesis_id"].tolist()):
        ax.text(i, best["delta_adjusted_r2_vs_base"].iloc[i], hid, ha="center", va="bottom", fontsize=9)
    ax.axhline(0.0, color="black", linewidth=0.9)
    ax.set_ylabel("Best-model Δ adjusted R²")
    ax.set_title("Phase 5C: Best hypothesis by pair × branch")
    ax.set_xticks(x)
    ax.set_xticklabels(best["label"], rotation=30, ha="right")
    fig.tight_layout()
    fig.savefig(paths["fig_pair_comparisons"], dpi=180)
    plt.close(fig)

    print(
        f"Wrote figures: {paths['fig_model_delta']}, {paths['fig_hypothesis_rankings']}, {paths['fig_pair_comparisons']}"
    )


def combine_checkpoints(
    paths: dict[str, Path],
    threshold: float,
    include_geography_sensitivity: bool,
    render_figures: bool = True,
    pair_filter: str | None = None,
    branch_filter: str | None = None,
) -> None:
    ckpts = sorted(paths["checkpoints_dir"].glob("combo_*.csv"))
    if not ckpts:
        raise FileNotFoundError(f"No checkpoints found in {paths['checkpoints_dir']}")

    manifest = build_combo_manifest(threshold=threshold, pair_filter=pair_filter, branch_filter=branch_filter)
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

    model_comparison, predictor_effects, pair_rankings, hypothesis_summary = split_outputs(combined)

    model_comparison.to_csv(paths["model_comparison"], index=False)
    predictor_effects.to_csv(paths["predictor_effects"], index=False)
    pair_rankings.to_csv(paths["pair_rankings"], index=False)
    hypothesis_summary.to_csv(paths["hypothesis_summary"], index=False)
    manifest.to_csv(paths["manifest"], index=False)

    run_meta = {
        "analysis": "phase5c_plant_diversity_hypotheses",
        "generated_at_epoch": time.time(),
        "n_checkpoints": len(ckpts),
        "n_model_comparison_rows": int(len(model_comparison)),
        "n_predictor_effect_rows": int(len(predictor_effects)),
        "n_pair_rankings_rows": int(len(pair_rankings)),
        "n_hypothesis_summary_rows": int(len(hypothesis_summary)),
        "expected_combos": int(len(expected)),
        "permutations_present": sorted({int(x) for x in model_comparison["permutations"].dropna().tolist()}),
        "include_geography_sensitivity": bool(include_geography_sensitivity),
        "model_count_primary": len(HYPOTHESIS_MODELS),
        "model_count_total_scopes": len(HYPOTHESIS_MODELS) * (2 if include_geography_sensitivity else 1),
        "output_files": {
            "model_comparison": str(paths["model_comparison"]),
            "predictor_effects": str(paths["predictor_effects"]),
            "pair_rankings": str(paths["pair_rankings"]),
            "hypothesis_summary": str(paths["hypothesis_summary"]),
            "manifest": str(paths["manifest"]),
        },
    }
    paths["metadata"].write_text(json.dumps(run_meta, indent=2))

    if render_figures:
        make_figures(model_comparison, hypothesis_summary, pair_rankings, paths)

    print(f"Wrote {paths['model_comparison']}")
    print(f"Wrote {paths['predictor_effects']}")
    print(f"Wrote {paths['pair_rankings']}")
    print(f"Wrote {paths['hypothesis_summary']}")
    print(f"Wrote {paths['manifest']}")
    print(f"Wrote {paths['metadata']}")


def run_full_serial(
    paths: dict[str, Path],
    threshold: float,
    permutations: int,
    include_geography_sensitivity: bool,
    clr_distance_strategy: str,
    pair_filter: str | None = None,
    branch_filter: str | None = None,
) -> None:
    manifest = build_combo_manifest(threshold=threshold, pair_filter=pair_filter, branch_filter=branch_filter)
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
                include_geography_sensitivity=include_geography_sensitivity,
                clr_distance_strategy=clr_distance_strategy,
            )
        )

    elapsed = time.time() - start_all
    combined = pd.concat(rows, ignore_index=True)
    model_comparison, predictor_effects, pair_rankings, hypothesis_summary = split_outputs(combined)

    model_comparison.to_csv(paths["model_comparison"], index=False)
    predictor_effects.to_csv(paths["predictor_effects"], index=False)
    pair_rankings.to_csv(paths["pair_rankings"], index=False)
    hypothesis_summary.to_csv(paths["hypothesis_summary"], index=False)
    manifest.to_csv(paths["manifest"], index=False)

    run_meta = {
        "analysis": "phase5c_plant_diversity_hypotheses",
        "mode": "full_serial",
        "runtime_seconds": elapsed,
        "expected_combos": int(len(manifest)),
        "permutations": int(permutations),
        "clr_distance_strategy": clr_distance_strategy,
        "include_geography_sensitivity": bool(include_geography_sensitivity),
        "model_count_primary": len(HYPOTHESIS_MODELS),
        "model_count_total_scopes": len(HYPOTHESIS_MODELS) * (2 if include_geography_sensitivity else 1),
    }
    paths["metadata"].write_text(json.dumps(run_meta, indent=2))
    make_figures(model_comparison, hypothesis_summary, pair_rankings, paths)

    print("PHASE5C_DONE")
    print(f"runtime_seconds={elapsed:.3f}")


def render_figures_from_existing_outputs(paths: dict[str, Path]) -> None:
    model_comparison = pd.read_csv(paths["model_comparison"])
    hypothesis_summary = pd.read_csv(paths["hypothesis_summary"])
    pair_rankings = pd.read_csv(paths["pair_rankings"])
    make_figures(model_comparison, hypothesis_summary, pair_rankings, paths)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase 5C plant-diversity hypothesis dbRDA-style workflow")
    parser.add_argument("--write-manifest", action="store_true", help="Write combo manifest and exit if no other mode selected.")
    parser.add_argument("--single-combo", action="store_true", help="Run one combo and write one checkpoint.")
    parser.add_argument("--combo-index", type=int, default=None, help="0-based combo index used with --single-combo")
    parser.add_argument("--combine-checkpoints", action="store_true", help="Combine all combo checkpoints into final outputs")
    parser.add_argument("--figures-only", action="store_true", help="Render figures from existing combined outputs only")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="Output directory")
    parser.add_argument("--permutations", type=int, default=DEFAULT_PERMUTATIONS, help="Permutation count (default 999)")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD, help="Prevalence threshold")
    parser.add_argument("--single-pair", type=str, default=None, help="Optional filter, e.g. BAC↔ITS")
    parser.add_argument("--single-branch", type=str, default=None, help="Optional filter: presence/absence or CLR")
    parser.add_argument("--clr-distance-strategy", choices=VALID_CLR_DISTANCE_STRATEGIES, default=DEFAULT_CLR_DISTANCE_STRATEGY, help="CLR branch distance strategy: direct_aitchison (default) or pca10 sensitivity.")
    parser.add_argument(
        "--include-geography-sensitivity",
        action="store_true",
        help="Also evaluate +latitude+longitude sensitivity models for each hypothesis.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = output_paths(Path(args.output_dir))
    ensure_dirs(paths)

    did_anything = False

    if args.write_manifest:
        write_combo_manifest(
            paths,
            threshold=args.threshold,
            pair_filter=args.single_pair,
            branch_filter=args.single_branch,
        )
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
            include_geography_sensitivity=args.include_geography_sensitivity,
            clr_distance_strategy=args.clr_distance_strategy,
            pair_filter=args.single_pair,
            branch_filter=args.single_branch,
        )
        did_anything = True

    if args.combine_checkpoints:
        combine_checkpoints(
            paths=paths,
            threshold=args.threshold,
            include_geography_sensitivity=args.include_geography_sensitivity,
            render_figures=True,
            pair_filter=args.single_pair,
            branch_filter=args.single_branch,
        )
        did_anything = True

    if not did_anything:
        run_full_serial(
            paths=paths,
            threshold=args.threshold,
            permutations=args.permutations,
            include_geography_sensitivity=args.include_geography_sensitivity,
            clr_distance_strategy=args.clr_distance_strategy,
            pair_filter=args.single_pair,
            branch_filter=args.single_branch,
        )


if __name__ == "__main__":
    main()
