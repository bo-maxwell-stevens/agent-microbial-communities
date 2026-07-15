"""Shared cross-kingdom coupling metrics."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.stats import spearmanr


def _validate_labelled_square_distance(distance_df: pd.DataFrame) -> None:
    """Validate that a distance matrix is square and consistently labelled."""
    if distance_df.ndim != 2:
        raise ValueError("Distance matrix must be 2-dimensional")

    n_rows, n_cols = distance_df.shape
    if n_rows != n_cols:
        raise ValueError(f"Distance matrix must be square, got shape={distance_df.shape}")

    if not distance_df.index.equals(distance_df.columns):
        raise ValueError("Distance matrix row and column labels must match in identical order")


def condense_distance_matrix(distance_df: pd.DataFrame) -> np.ndarray:
    """Return deterministic upper-triangle values from a labelled square distance matrix."""
    _validate_labelled_square_distance(distance_df)

    values = distance_df.to_numpy(dtype=np.float64)
    tri_i, tri_j = np.triu_indices(values.shape[0], k=1)
    return values[tri_i, tri_j]


def procrustes_disparity(embedding_x: pd.DataFrame, embedding_y: pd.DataFrame) -> float:
    """Compute Procrustes disparity used by Phase 2 coupling summaries."""
    x = embedding_x.to_numpy(dtype=np.float64)
    y = embedding_y.to_numpy(dtype=np.float64)

    if x.shape[0] != y.shape[0]:
        raise ValueError(
            f"Procrustes inputs must have same number of samples, got {x.shape[0]} and {y.shape[0]}"
        )
    if x.shape[1] != y.shape[1]:
        raise ValueError(
            f"Procrustes inputs must have same number of columns, got {x.shape[1]} and {y.shape[1]}"
        )

    _, _, disparity = procrustes(x, y)
    return float(disparity)


def mantel_spearman(distance_x: pd.DataFrame, distance_y: pd.DataFrame) -> float:
    """Spearman correlation between condensed upper triangles of paired distance matrices.

    Behavior for constant/undefined vectors is explicit: returns NaN (matching scipy.stats.spearmanr).
    """
    _validate_labelled_square_distance(distance_x)
    _validate_labelled_square_distance(distance_y)

    if not distance_x.index.equals(distance_y.index):
        raise ValueError("Mantel Spearman requires identical sample ordering in both distance matrices")

    vec_x = condense_distance_matrix(distance_x)
    vec_y = condense_distance_matrix(distance_y)

    r, _ = spearmanr(vec_x, vec_y)
    if not np.isfinite(r):
        return float("nan")
    return float(r)
