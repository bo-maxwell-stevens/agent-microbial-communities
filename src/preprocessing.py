from __future__ import annotations

from typing import Any, Dict, Iterable, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform


def _coerce_sample_ids(sample_ids: pd.Index | Sequence[str]) -> pd.Index:
    idx = pd.Index(sample_ids)
    if idx.has_duplicates:
        dupes = idx[idx.duplicated()].tolist()
        raise ValueError(f"Duplicate requested sample IDs in cohort: {dupes[:10]}")
    return idx


def _validate_dataframe(
    table: pd.DataFrame,
    *,
    require_nonnegative: bool,
    allow_missing: bool = False,
) -> None:
    if not isinstance(table, pd.DataFrame):
        raise TypeError("Expected pandas DataFrame")
    if table.index.has_duplicates:
        dupes = table.index[table.index.duplicated()].tolist()
        raise ValueError(f"Duplicate sample IDs in table index: {dupes[:10]}")
    if table.columns.has_duplicates:
        dupes = table.columns[table.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate feature IDs in table columns: {dupes[:10]}")

    values = table.to_numpy()
    if np.issubdtype(values.dtype, np.number) is False:
        raise TypeError("Table contains non-numeric abundance values")
    if not allow_missing and np.isnan(values).any():
        raise ValueError("Table contains missing abundance values (NaN)")
    if require_nonnegative and np.nanmin(values) < 0:
        raise ValueError("Table contains negative abundance values")


def align_samples(table: pd.DataFrame, sample_ids: pd.Index | list[str]) -> pd.DataFrame:
    """Align a table to an explicit ordered cohort without silent intersection."""
    cohort = _coerce_sample_ids(sample_ids)
    if table.index.has_duplicates:
        dupes = table.index[table.index.duplicated()].tolist()
        raise ValueError(f"Duplicate sample IDs in table index: {dupes[:10]}")

    missing = cohort.difference(table.index)
    if len(missing) > 0:
        raise ValueError(f"Requested samples are missing from table: {missing.tolist()[:10]}")

    out = table.loc[cohort]
    return out


def filter_prevalence(df: pd.DataFrame, threshold: float) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    _validate_dataframe(df, require_nonnegative=True, allow_missing=False)
    if not (0 <= threshold <= 1):
        raise ValueError(f"threshold must be in [0,1], got {threshold}")

    n_samples = df.shape[0]
    min_occurrences = max(1, int(np.ceil(threshold * n_samples)))
    present = (df > 0).sum(axis=0)
    mask = present.values >= min_occurrences
    filtered = df.iloc[:, mask]

    info = {
        "threshold": float(threshold),
        "threshold_label": f"{threshold*100:.0f}%",
        "features_before": int(df.shape[1]),
        "features_after": int(filtered.shape[1]),
        "features_removed": int(df.shape[1] - filtered.shape[1]),
        "min_occurrences": int(min_occurrences),
        "n_samples": int(n_samples),
    }
    return filtered, info


def to_presence_absence(df: pd.DataFrame) -> pd.DataFrame:
    _validate_dataframe(df, require_nonnegative=True, allow_missing=False)
    return (df > 0).astype(np.float64)


def to_relative_abundance(df: pd.DataFrame) -> pd.DataFrame:
    _validate_dataframe(df, require_nonnegative=True, allow_missing=False)
    row_sums = df.sum(axis=1)
    zero_rows = row_sums[row_sums == 0]
    if len(zero_rows) > 0:
        raise ValueError(
            "Cannot compute relative abundance with zero library size for samples: "
            f"{zero_rows.index.tolist()[:10]}"
        )
    return df.div(row_sums, axis=0)


def hellinger_transform(df: pd.DataFrame) -> pd.DataFrame:
    return np.sqrt(to_relative_abundance(df))


def clr_transform(df: pd.DataFrame, pseudocount: float = 0.5) -> pd.DataFrame:
    """CLR transform with explicit additive pseudocount (default matches existing Phase 1.5 behavior)."""
    _validate_dataframe(df, require_nonnegative=True, allow_missing=False)
    if pseudocount <= 0:
        raise ValueError("pseudocount must be > 0")

    vals = df.to_numpy(dtype=np.float64) + pseudocount
    gm = np.exp(np.mean(np.log(vals), axis=1, keepdims=True))
    clr_vals = np.log(vals / gm)
    return pd.DataFrame(clr_vals, index=df.index, columns=df.columns)


def _pairwise_distance(table: pd.DataFrame, metric: str) -> pd.DataFrame:
    if not isinstance(table, pd.DataFrame):
        raise TypeError("Expected pandas DataFrame")
    if table.index.has_duplicates:
        dupes = table.index[table.index.duplicated()].tolist()
        raise ValueError(f"Duplicate sample IDs in table index: {dupes[:10]}")
    if table.columns.has_duplicates:
        dupes = table.columns[table.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate feature IDs in table columns: {dupes[:10]}")
    vals = table.to_numpy()
    if np.issubdtype(vals.dtype, np.number) is False:
        raise TypeError("Distance input contains non-numeric values")
    if np.isnan(vals).any():
        raise ValueError("Distance input contains NaN values")

    dist = pdist(vals, metric=metric)
    dm = squareform(dist)
    return pd.DataFrame(dm, index=table.index, columns=table.index)


def bray_curtis_distance(relabund_df: pd.DataFrame) -> pd.DataFrame:
    _validate_dataframe(relabund_df, require_nonnegative=True, allow_missing=False)
    return _pairwise_distance(relabund_df, metric="braycurtis")


def jaccard_distance(binary_df: pd.DataFrame) -> pd.DataFrame:
    _validate_dataframe(binary_df, require_nonnegative=True, allow_missing=False)
    vals = binary_df.to_numpy()
    uniq = set(np.unique(vals).tolist())
    if not uniq.issubset({0.0, 1.0}):
        raise ValueError("Jaccard distance expects binary matrix with values in {0,1}")
    return _pairwise_distance(binary_df, metric="jaccard")


def euclidean_distance(df: pd.DataFrame) -> pd.DataFrame:
    _validate_dataframe(df, require_nonnegative=False, allow_missing=False)
    return _pairwise_distance(df, metric="euclidean")
