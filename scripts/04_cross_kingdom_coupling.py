"""
Run Phase 2 Confirmatory Coupling Analysis

Branch-specific confirmatory coupling:
- presence/absence: prevalence filter -> binary -> Jaccard -> deterministic PCoA
- CLR: prevalence filter -> relative abundance -> CLR -> Euclidean -> deterministic PCA

Mantel Spearman is computed directly on branch-specific full distance matrices
(not reduced ordination embeddings).
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr
from sklearn.decomposition import PCA

# Paths
DATA_DIR = "data"
RESULTS_DIR = "results/phase2_confirmatory_coupling"
COHORT_FILE = f"{RESULTS_DIR}/sample_cohort_used.csv"

PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10
THRESHOLDS = [0.05, 0.10]
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


def align_samples(table: pd.DataFrame, cohort_sample_ids: list[str]) -> pd.DataFrame:
    aligned = table.reindex(cohort_sample_ids)
    if aligned.isnull().any().any():
        missing_rows = aligned.index[aligned.isnull().all(axis=1)].tolist()
        if missing_rows:
            raise ValueError(f"Missing cohort samples in OTU table: {missing_rows[:5]}...")
    return aligned


def prevalence_filter_table(table: pd.DataFrame, threshold: float) -> pd.DataFrame:
    # Sort columns before any transform for deterministic behavior
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
    rel = table.div(row_sums, axis=0).fillna(0.0)
    return rel


def clr_transform(rel_table: pd.DataFrame, pseudocount: float = PSEUDOCOUNT) -> pd.DataFrame:
    vals = rel_table.to_numpy(dtype=np.float64) + pseudocount
    gm = np.exp(np.mean(np.log(vals), axis=1, keepdims=True))
    clr_vals = np.log(vals / gm)
    return pd.DataFrame(clr_vals, index=rel_table.index, columns=rel_table.columns)


def jaccard_distance_matrix(binary_table: pd.DataFrame) -> np.ndarray:
    return squareform(pdist(binary_table.to_numpy(dtype=np.float64), metric="jaccard"))


def euclidean_distance_matrix(table: pd.DataFrame) -> np.ndarray:
    return squareform(pdist(table.to_numpy(dtype=np.float64), metric="euclidean"))


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


def condensed_upper(distance_matrix: np.ndarray) -> np.ndarray:
    idx = np.triu_indices(distance_matrix.shape[0], k=1)
    return distance_matrix[idx]


def compute_procrustes(embedding_x: pd.DataFrame, embedding_y: pd.DataFrame) -> float:
    x = embedding_x.to_numpy(dtype=np.float64)
    y = embedding_y.to_numpy(dtype=np.float64)
    _, _, disparity = procrustes(x, y)
    return float(disparity)


def compute_mantel_spearman(distance_x: np.ndarray, distance_y: np.ndarray) -> float:
    vx = condensed_upper(distance_x)
    vy = condensed_upper(distance_y)
    r, _ = spearmanr(vx, vy)
    return float(r)


def prepare_branch_outputs(table: pd.DataFrame, cohort: list[str], threshold: float, branch: str):
    aligned = align_samples(table, cohort)
    filtered = prevalence_filter_table(aligned, threshold)

    if branch == "presence/absence":
        transformed = to_presence_absence(filtered)
        distance = jaccard_distance_matrix(transformed)
        embedding = pcoa_from_distance(distance, cohort, N_COMPONENTS)
        distance_metric = "jaccard"
        ordination_method = "pcoa"
    elif branch == "CLR":
        rel = to_relative_abundance(filtered)
        transformed = clr_transform(rel, PSEUDOCOUNT)
        distance = euclidean_distance_matrix(transformed)
        embedding = pca_embedding(transformed, cohort, N_COMPONENTS)
        distance_metric = "euclidean"
        ordination_method = "pca"
    else:
        raise ValueError(f"Unsupported branch: {branch}")

    return {
        "embedding": embedding,
        "distance": distance,
        "distance_metric": distance_metric,
        "ordination_method": ordination_method,
        "n_features": int(filtered.shape[1]),
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
    for threshold in THRESHOLDS:
        for branch in BRANCHES:
            for name1, name2 in PAIRS:
                out1 = prepare_branch_outputs(tables[name1], cohort, threshold, branch)
                out2 = prepare_branch_outputs(tables[name2], cohort, threshold, branch)

                procrustes_fit = compute_procrustes(out1["embedding"], out2["embedding"])
                mantel_spearman = compute_mantel_spearman(out1["distance"], out2["distance"])

                results.append(
                    {
                        "pair": f"{name1}↔{name2}",
                        "branch": branch,
                        "threshold": threshold,
                        "procrustes_fit": procrustes_fit,
                        "mantel_spearman": mantel_spearman,
                        "distance_metric": out1["distance_metric"],
                        "ordination_method": out1["ordination_method"],
                        "n_features_1": out1["n_features"],
                        "n_features_2": out2["n_features"],
                    }
                )

    out_path = Path(results_dir) / "phase2_coupling_summary.csv"
    pd.DataFrame(results).to_csv(out_path, index=False)
    print(f"Phase 2 analysis completed: {out_path}")


if __name__ == "__main__":
    main()
