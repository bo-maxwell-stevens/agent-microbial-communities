"""
Run Phase 2 Confirmatory Coupling Analysis

Branch-specific confirmatory coupling:
- presence/absence: prevalence filter -> binary -> Jaccard -> deterministic PCoA
- CLR: prevalence filter -> remove zero-library samples -> relative abundance -> CLR -> Euclidean -> deterministic PCA

Mantel Spearman is computed directly on branch-specific full distance matrices
(not reduced ordination embeddings).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.coupling_metrics import mantel_spearman, procrustes_disparity
from src.preprocessing import (
    align_samples,
    clr_transform,
    euclidean_distance,
    filter_prevalence,
    jaccard_distance,
    to_presence_absence,
    to_relative_abundance,
)

# Paths
DATA_DIR = "data"
RESULTS_DIR = "results/phase2_confirmatory_coupling"
COHORT_FILE = f"{RESULTS_DIR}/sample_cohort_used.csv"

CLR_PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10
PREVALENCE_THRESHOLDS = (0.05, 0.10)
BRANCHES = ["presence/absence", "CLR"]
PAIRS = [("EUK", "ITS"), ("AMF", "ITS"), ("AMF", "EUK")]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Phase 2 confirmatory coupling analysis")
    parser.add_argument("--data-dir", default=DATA_DIR, help="Input data directory")
    parser.add_argument("--results-dir", default=RESULTS_DIR, help="Output results directory")
    parser.add_argument("--cohort-file", default=COHORT_FILE, help="Cohort CSV path")
    return parser.parse_args()


def load_otu_table(name: str, data_dir: str = DATA_DIR) -> pd.DataFrame:
    path = f"{data_dir}/{name}_OTU_table_final.tsv"
    return pd.read_csv(path, sep="\t", index_col=0)


def _sorted_features(table: pd.DataFrame) -> pd.DataFrame:
    return table.reindex(sorted(table.columns), axis=1)


def _prevalence_filter_required(
    aligned: pd.DataFrame,
    *,
    threshold: float,
    modality: str,
) -> tuple[pd.DataFrame, dict]:
    filtered, info = filter_prevalence(aligned, threshold)
    if filtered.shape[1] == 0:
        raise ValueError(
            "No features passed prevalence filter: "
            f"modality={modality}, threshold={threshold}, "
            f"n_samples={info['n_samples']}, min_occurrences={info['min_occurrences']}"
        )
    return filtered, info


def pcoa_from_distance(distance_matrix: np.ndarray, sample_ids: list[str], n_components: int = N_COMPONENTS) -> pd.DataFrame:
    # Deterministic classical PCoA via eigendecomposition of doubly-centered matrix
    n = distance_matrix.shape[0]
    if n < 2:
        raise ValueError("Need at least 2 samples for PCoA")

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
        # Degenerate case: return zeros but deterministic shape
        k = min(n_components, n - 1)
        return pd.DataFrame(np.zeros((n, max(1, k))), index=sample_ids)

    k = min(n_components, n - 1, eigvals.size)
    coords = eigvecs[:, :k] * np.sqrt(eigvals[:k])
    return pd.DataFrame(coords, index=sample_ids)


def pca_embedding(table: pd.DataFrame, sample_ids: list[str], n_components: int = N_COMPONENTS) -> pd.DataFrame:
    x = table.to_numpy(dtype=np.float64)
    if x.shape[1] == 0:
        raise ValueError("No features available for PCA")
    k = max(1, min(n_components, x.shape[0] - 1 if x.shape[0] > 1 else 1, x.shape[1]))
    pca = PCA(n_components=k, svd_solver="full")
    emb = pca.fit_transform(x)
    return pd.DataFrame(emb, index=sample_ids)


def prepare_branch_modality(
    table: pd.DataFrame,
    cohort: list[str],
    threshold: float,
    branch: str,
    modality: str,
) -> dict:
    aligned = align_samples(table, cohort)
    aligned = _sorted_features(aligned)
    filtered, _ = _prevalence_filter_required(aligned, threshold=threshold, modality=modality)

    excluded_zero_library_samples: list[str] = []
    if branch == "presence/absence":
        transformed = to_presence_absence(filtered)
        distance_metric = "jaccard"
        ordination_method = "pcoa"
    elif branch == "CLR":
        library_sizes = filtered.sum(axis=1)
        zero_mask = library_sizes == 0
        excluded_zero_library_samples = filtered.index[zero_mask].astype(str).tolist()
        filtered_for_clr = filtered.loc[~zero_mask]
        rel = to_relative_abundance(filtered_for_clr)
        transformed = clr_transform(rel, pseudocount=CLR_PSEUDOCOUNT)
        distance_metric = "euclidean"
        ordination_method = "pca"
    else:
        raise ValueError(f"Unsupported branch: {branch}")

    return {
        "modality": modality,
        "threshold": float(threshold),
        "branch": branch,
        "transformed": transformed,
        "distance_metric": distance_metric,
        "ordination_method": ordination_method,
        "n_features": int(filtered.shape[1]),
        "excluded_zero_library_samples": excluded_zero_library_samples,
    }


def run_pair(
    out1: dict,
    out2: dict,
    cohort: list[str],
    name1: str,
    name2: str,
) -> dict:
    idx1 = set(out1["transformed"].index.astype(str))
    idx2 = set(out2["transformed"].index.astype(str))
    pair_samples = [sid for sid in cohort if sid in idx1 and sid in idx2]

    t1 = out1["transformed"].loc[pair_samples]
    t2 = out2["transformed"].loc[pair_samples]

    if out1["branch"] == "presence/absence":
        d1_df = jaccard_distance(t1)
        d2_df = jaccard_distance(t2)
        d1 = d1_df.to_numpy(dtype=np.float64)
        d2 = d2_df.to_numpy(dtype=np.float64)
        emb1 = pcoa_from_distance(d1, pair_samples, N_COMPONENTS)
        emb2 = pcoa_from_distance(d2, pair_samples, N_COMPONENTS)
    else:
        d1_df = euclidean_distance(t1)
        d2_df = euclidean_distance(t2)
        d1 = d1_df.to_numpy(dtype=np.float64)
        d2 = d2_df.to_numpy(dtype=np.float64)
        emb1 = pca_embedding(t1, pair_samples, N_COMPONENTS)
        emb2 = pca_embedding(t2, pair_samples, N_COMPONENTS)

    procrustes_fit = procrustes_disparity(emb1, emb2)
    mantel_spearman_value = mantel_spearman(d1_df, d2_df)

    return {
        "pair": f"{name1}↔{name2}",
        "branch": out1["branch"],
        "threshold": out1["threshold"],
        "procrustes_fit": procrustes_fit,
        "mantel_spearman": mantel_spearman_value,
        "distance_metric": out1["distance_metric"],
        "ordination_method": out1["ordination_method"],
        "n_features_1": out1["n_features"],
        "n_features_2": out2["n_features"],
        "n_samples": int(len(pair_samples)),
        "excluded_zero_library_samples_a": ";".join(out1["excluded_zero_library_samples"]),
        "excluded_zero_library_samples_b": ";".join(out2["excluded_zero_library_samples"]),
    }


def main() -> None:
    args = parse_args()

    data_dir = args.data_dir
    results_dir = args.results_dir
    cohort_file = args.cohort_file

    print("Running Phase 2 confirmatory coupling analysis...")
    Path(results_dir).mkdir(parents=True, exist_ok=True)

    cohort = pd.read_csv(cohort_file)["Sample_ID"].astype(str).tolist()
    tables = {name: load_otu_table(name, data_dir) for name in ["AMF", "EUK", "ITS"]}

    results: list[dict] = []
    for threshold in PREVALENCE_THRESHOLDS:
        for branch in BRANCHES:
            per_modality = {
                name: prepare_branch_modality(tables[name], cohort, threshold, branch, modality=name)
                for name in ["AMF", "EUK", "ITS"]
            }
            for name1, name2 in PAIRS:
                results.append(run_pair(per_modality[name1], per_modality[name2], cohort, name1, name2))

    out_path = Path(results_dir) / "phase2_coupling_summary.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"Phase 2 analysis completed: {out_path}")


if __name__ == "__main__":
    main()
