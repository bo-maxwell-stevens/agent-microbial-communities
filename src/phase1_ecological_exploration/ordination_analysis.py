from __future__ import annotations

import logging
import warnings
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
from src.preprocessing import (
    align_samples,
    bray_curtis_distance,
    clr_transform,
    filter_prevalence,
    jaccard_distance,
    to_presence_absence,
    to_relative_abundance,
)

logger = logging.getLogger(__name__)


def _check_skbio_pcoa():
    try:
        from skbio.stats.ordination import pcoa as skbio_pcoa
        try:
            from skbio.stats.distance import DistanceMatrix
        except ImportError:
            from skbio.stats.ordination import DistanceMatrix
        return skbio_pcoa, DistanceMatrix
    except ImportError:
        return None, None


def _check_sklearn_pca():
    try:
        from sklearn.decomposition import PCA as skPCA
        return skPCA
    except ImportError:
        return None


def _check_sklearn_mds():
    try:
        from sklearn.manifold import MDS as skMDS
        return skMDS
    except ImportError:
        return None


def run_pcoa(
    dist_matrix: np.ndarray,
    sample_ids: list,
    n_components: int = 10,
) -> Dict:
    skbio_pcoa_fn, DistanceMatrix = _check_skbio_pcoa()
    result = {"method": "PCoA", "engine": None, "coordinates": None, "eigvals": None, "success": False}

    if skbio_pcoa_fn is not None:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                dist_values = dist_matrix.values if isinstance(dist_matrix, pd.DataFrame) else dist_matrix
                dm = DistanceMatrix(dist_values, ids=sample_ids)
                skbio_result = skbio_pcoa_fn(dm)
            result["coordinates"] = pd.DataFrame(
                skbio_result.samples.values[:, :n_components],
                index=sample_ids,
                columns=[f"PCoA{i+1}" for i in range(min(n_components, skbio_result.samples.shape[1]))],
            )
            ev = skbio_result.eigvals
            if isinstance(ev, pd.Series):
                ev = ev.values
            result["eigvals"] = ev[:n_components].tolist() if len(ev) >= n_components else ev.tolist()
            result["engine"] = "skbio"
            result["success"] = True
            logger.info("PCoA computed via skbio")
            return result
        except Exception as e:
            logger.warning("skbio PCoA failed: %s; falling back to sklearn MDS", e)

    skMDS = _check_sklearn_mds()
    if skMDS is not None:
        try:
            mds = skMDS(n_components=n_components, dissimilarity="precomputed",
                        random_state=42, normalized_stress="auto")
            dist_values = dist_matrix.values if isinstance(dist_matrix, pd.DataFrame) else dist_matrix
            coords = mds.fit_transform(dist_values)
            coords[np.isnan(coords)] = 0.0
            result["coordinates"] = pd.DataFrame(
                coords,
                index=sample_ids,
                columns=[f"MDS{i+1}" for i in range(min(n_components, coords.shape[1]))],
            )
            stress = getattr(mds, "stress_", np.nan)
            result["eigvals"] = [stress] if not np.isnan(stress) else None
            result["engine"] = "sklearn_MDS"
            result["success"] = True
            logger.info("PCoA computed via sklearn MDS fallback")
            return result
        except Exception as e:
            logger.warning("sklearn MDS also failed: %s", e)

    result["engine"] = "none_available"
    logger.error("No PCoA/MDS engine available")
    return result


def run_nmds(
    dist_matrix: np.ndarray,
    sample_ids: list,
    n_components: int = 2,
    n_init: int = 10,
) -> Dict:
    skMDS = _check_sklearn_mds()
    result = {"method": "NMDS", "engine": None, "coordinates": None, "stress": None, "success": False}

    if skMDS is not None:
        try:
            mds = skMDS(n_components=n_components, dissimilarity="precomputed",
                        metric=False, random_state=42, n_init=n_init,
                        normalized_stress="auto")
            dist_values = dist_matrix.values if isinstance(dist_matrix, pd.DataFrame) else dist_matrix
            coords = mds.fit_transform(dist_values)
            coords[np.isnan(coords)] = 0.0
            result["coordinates"] = pd.DataFrame(
                coords,
                index=sample_ids,
                columns=[f"NMDS{i+1}" for i in range(n_components)],
            )
            result["stress"] = float(getattr(mds, "stress_", np.nan))
            result["engine"] = "sklearn_NMDS"
            result["success"] = True
            logger.info("NMDS computed via sklearn (metric=False MDS)")
            return result
        except Exception as e:
            logger.warning("sklearn NMDS failed: %s", e)

    result["engine"] = "none_available"
    logger.error("No NMDS engine available")
    return result


def run_pca(data_matrix: pd.DataFrame, n_components: int = 10) -> Dict:
    skPCA = _check_sklearn_pca()
    result = {"method": "PCA", "engine": None, "coordinates": None,
              "explained_variance_ratio": None, "loadings": None, "success": False}

    if skPCA is not None:
        try:
            vals = data_matrix.values
            centered = vals - np.mean(vals, axis=0)
            pca = skPCA(n_components=min(n_components, data_matrix.shape[1], data_matrix.shape[0]))
            coords = pca.fit_transform(centered)
            result["coordinates"] = pd.DataFrame(
                coords,
                index=data_matrix.index,
                columns=[f"PC{i+1}" for i in range(coords.shape[1])],
            )
            result["explained_variance_ratio"] = pca.explained_variance_ratio_.tolist()
            loadings = pd.DataFrame(
                pca.components_.T,
                index=data_matrix.columns,
                columns=[f"PC{i+1}" for i in range(pca.n_components_)],
            )
            result["loadings"] = loadings
            result["engine"] = "sklearn"
            result["success"] = True
            logger.info("PCA computed via sklearn")
            return result
        except Exception as e:
            logger.warning("sklearn PCA failed: %s", e)
    else:
        try:
            vals = data_matrix.values
            centered = vals - np.mean(vals, axis=0)
            C = (centered.T @ centered) / (centered.shape[0] - 1)
            eigvals, eigvecs = np.linalg.eigh(C)
            idx = np.argsort(eigvals)[::-1]
            eigvals = eigvals[idx]
            eigvecs = eigvecs[:, idx]
            n = min(n_components, len(eigvals))
            coords = centered @ eigvecs[:, :n]
            result["coordinates"] = pd.DataFrame(
                coords, index=data_matrix.index,
                columns=[f"PC{i+1}" for i in range(n)]
            )
            total_var = np.sum(eigvals)
            result["explained_variance_ratio"] = (eigvals[:n] / total_var).tolist()
            result["engine"] = "numpy_eigh"
            result["success"] = True
            logger.info("PCA computed via numpy.linalg.eigh")
            return result
        except Exception as e:
            logger.warning("numpy PCA fallback failed: %s", e)

    result["engine"] = "none_available"
    logger.error("No PCA engine available")
    return result


def run_ordination_strategies(
    otu_table: pd.DataFrame,
    sample_ids: list,
    prevalence_thresholds: list[float] = None,
) -> Dict:
    if prevalence_thresholds is None:
        prevalence_thresholds = [0.01, 0.05, 0.10]

    otu_subset = align_samples(otu_table, sample_ids)
    logger.info("Ordination on %d samples, %d features", otu_subset.shape[0], otu_subset.shape[1])

    results = {}

    bin_df = to_presence_absence(otu_subset)
    j_dist = jaccard_distance(bin_df)
    pcoa_j = run_pcoa(j_dist, list(otu_subset.index))
    results["jaccard_pcoa"] = pcoa_j
    j_dist_close = len(j_dist) < 5
    if not pcoa_j["success"] and not j_dist_close:
        nmds_j = run_nmds(j_dist, list(otu_subset.index))
        results["jaccard_nmds"] = nmds_j
        logger.info("Jaccard: PCoA failed, NMDS attempted")
    elif not pcoa_j["success"]:
        logger.warning("Jaccard: too few samples for NMDS fallback")

    rel_df = to_relative_abundance(otu_subset)
    bc_dist = bray_curtis_distance(rel_df)
    pcoa_bc = run_pcoa(bc_dist, list(otu_subset.index))
    results["bray_curtis_pcoa"] = pcoa_bc
    if not pcoa_bc["success"]:
        nmds_bc = run_nmds(bc_dist, list(otu_subset.index))
        results["bray_curtis_nmds"] = nmds_bc
        logger.info("Bray-Curtis: PCoA failed, NMDS attempted")

    clr_results = {}
    for thresh in prevalence_thresholds:
        filtered, filt_info = filter_prevalence(otu_subset, thresh)
        if filtered.shape[1] < 3:
            logger.warning("CLR thresh %.0f%%: only %d features left, skipping PCA",
                           thresh * 100, filtered.shape[1])
            clr_results[f"clr_{thresh:.2f}"] = {
                "method": "CLR+PCA",
                "threshold_info": filt_info,
                "success": False,
                "reason": f"Too few features ({filtered.shape[1]}) after filtering",
            }
            continue
        try:
            clr_df = clr_transform(filtered)
        except Exception as e:
            logger.warning("CLR transform failed at thresh %.0f%%: %s", thresh * 100, e)
            clr_results[f"clr_{thresh:.2f}"] = {
                "method": "CLR+PCA",
                "threshold_info": filt_info,
                "success": False,
                "reason": f"CLR transform error: {e}",
            }
            continue
        pca_res = run_pca(clr_df)
        pca_res["threshold_info"] = filt_info
        clr_results[f"clr_{thresh:.2f}"] = pca_res
    results["clr_pca"] = clr_results

    return results
