from __future__ import annotations

import logging
import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import pearsonr, spearmanr

logger = logging.getLogger(__name__)


def compute_procrustes(
    coords_a: pd.DataFrame,
    coords_b: pd.DataFrame,
) -> Dict:
    result = {
        "method": "Procrustes",
        "success": False,
        "disparity": None,
        "n_samples": None,
        "n_dimensions": None,
        "correlation": None,
    }
    common_idx = coords_a.index.intersection(coords_b.index)
    if len(common_idx) < 3:
        logger.warning("Procrustes: too few common samples (%d)", len(common_idx))
        return result

    a = coords_a.loc[common_idx].values.copy()
    b = coords_b.loc[common_idx].values.copy()

    n_dims = min(a.shape[1], b.shape[1])
    a = a[:, :n_dims]
    b = b[:, :n_dims]

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            mtx1, mtx2, disparity = procrustes(a, b)
        corr = np.corrcoef(mtx1.ravel(), mtx2.ravel())[0, 1]
        result["disparity"] = float(disparity)
        result["n_samples"] = len(common_idx)
        result["n_dimensions"] = n_dims
        result["correlation"] = float(corr)
        result["success"] = True
        logger.info("Procrustes: disparity=%.4f, correlation=%.4f", disparity, corr)
    except Exception as e:
        logger.warning("Procrustes computation failed: %s", e)
    return result


def procrustes_permutation_test(
    coords_a: pd.DataFrame,
    coords_b: pd.DataFrame,
    n_permutations: int = 999,
    random_state: int = 42,
) -> Dict:
    result = compute_procrustes(coords_a, coords_b)
    if not result["success"]:
        return result

    common_idx = coords_a.index.intersection(coords_b.index)
    a = coords_a.loc[common_idx].values.copy()
    b = coords_b.loc[common_idx].values.copy()
    n_dims = min(a.shape[1], b.shape[1])
    a = a[:, :n_dims]
    b = b[:, :n_dims]

    observed_disparity = result["disparity"]
    rng = np.random.default_rng(random_state)
    null_disparities = []

    for i in range(n_permutations):
        b_shuffled = b.copy()
        rng.shuffle(b_shuffled, axis=0)
        try:
            _, _, d = procrustes(a, b_shuffled)
            null_disparities.append(d)
        except Exception:
            continue

    null_disparities = np.array(null_disparities)
    if len(null_disparities) == 0:
        logger.warning("All Procrustes permutations failed")
        result["p_value"] = None
        result["n_permutations_effective"] = 0
        return result

    p_value = (1 + np.sum(null_disparities <= observed_disparity)) / (1 + len(null_disparities))
    result["p_value"] = float(p_value)
    result["n_permutations"] = n_permutations
    result["n_permutations_effective"] = len(null_disparities)
    result["null_disparity_mean"] = float(np.mean(null_disparities))
    result["null_disparity_std"] = float(np.std(null_disparities))
    logger.info(
        "Procrustes permutation test: p=%.4f (null mean=%.4f, std=%.4f)",
        p_value, np.mean(null_disparities), np.std(null_disparities),
    )
    return result


def compute_correlation_fallback(
    coords_a: pd.DataFrame,
    coords_b: pd.DataFrame,
) -> Dict:
    common_idx = coords_a.index.intersection(coords_b.index)
    result = {
        "method": "Correlation_fallback",
        "success": False,
        "pearson_r": None,
        "spearman_rho": None,
        "n_samples": len(common_idx),
    }
    if len(common_idx) < 3:
        return result

    a = coords_a.loc[common_idx].values
    b = coords_b.loc[common_idx].values

    dist_a = squareform(pdist(a, metric="euclidean"))
    dist_b = squareform(pdist(b, metric="euclidean"))
    triu_idx = np.triu_indices_from(dist_a, k=1)
    va = dist_a[triu_idx]
    vb = dist_b[triu_idx]

    try:
        pr, _ = pearsonr(va, vb)
        sr, _ = spearmanr(va, vb)
        result["pearson_r"] = float(pr)
        result["spearman_rho"] = float(sr)
        result["success"] = True
        logger.info("Correlation fallback: pearson=%.4f, spearman=%.4f", pr, sr)
    except Exception as e:
        logger.warning("Correlation fallback failed: %s", e)
    return result


def _flatten_results(ordination_results: Dict) -> Dict[str, Dict]:
    flat = {}
    for key, value in ordination_results.items():
        if key == "clr_pca" and isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, dict) and "coordinates" in sub_value:
                    flat[sub_key] = sub_value
        elif isinstance(value, dict) and "coordinates" in value:
            flat[key] = value
    return flat


def compare_ordinations(
    ordination_results: Dict[str, Dict],
    method_pairs: List[Tuple[str, str]] = None,
    use_permutation_test: bool = True,
) -> List[Dict]:
    flat = _flatten_results(ordination_results)

    if method_pairs is None:
        strategies = list(flat.keys())
        method_pairs = []
        for i in range(len(strategies)):
            for j in range(i + 1, len(strategies)):
                method_pairs.append((strategies[i], strategies[j]))

    diagnostics = []

    for name_a, name_b in method_pairs:
        res_a = flat.get(name_a, {})
        res_b = flat.get(name_b, {})

        coords_a = res_a.get("coordinates", None)
        coords_b = res_b.get("coordinates", None)

        if coords_a is None or coords_b is None:
            logger.info("Skipping %s vs %s: missing coordinates", name_a, name_b)
            continue

        if use_permutation_test:
            diag = procrustes_permutation_test(coords_a, coords_b)
        else:
            diag = compute_procrustes(coords_a, coords_b)

        if not diag["success"]:
            fallback = compute_correlation_fallback(coords_a, coords_b)
            diag["fallback"] = fallback
            diag["method"] = "Procrustes_failed_fallback_correlation"

        diag["ordination_a"] = name_a
        diag["ordination_b"] = name_b
        diagnostics.append(diag)

    return diagnostics
