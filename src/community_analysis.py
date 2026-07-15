"""Shared community-analysis helpers for Phase 5 workflows."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

DATA_DIR = Path("data")
PSEUDOCOUNT = 1e-6
N_COMPONENTS = 10
DEFAULT_CLR_DISTANCE_STRATEGY = "direct_aitchison"


def load_otu_table(domain: str) -> pd.DataFrame:
    path = DATA_DIR / f"{domain}_OTU_table_final.tsv"
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, sep="	", index_col=0)


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
