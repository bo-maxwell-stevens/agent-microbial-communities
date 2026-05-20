from __future__ import annotations

import logging
from typing import Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def compute_prevalence_sensitivity(
    otu_table: pd.DataFrame,
    sample_ids: list,
    thresholds: List[float] = None,
) -> Dict:
    if thresholds is None:
        thresholds = [0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.10, 0.15, 0.20]

    otu_subset = otu_table.loc[otu_table.index.isin(sample_ids)]
    n_samples = otu_subset.shape[0]
    total_features = otu_subset.shape[1]

    records = []
    for thresh in thresholds:
        min_occ = max(1, int(np.ceil(thresh * n_samples)))
        present = (otu_subset > 0).sum(axis=0)
        mask = (present.values >= min_occ)
        n_retained = int(mask.sum())
        n_removed = total_features - n_retained

        frac_retained = n_retained / total_features if total_features > 0 else 0.0
        n_zero_samples = int((otu_subset.iloc[:, mask] if n_retained > 0
                              else otu_subset.iloc[:, :0]).sum(axis=1).eq(0).sum())

        records.append({
            "prevalence_threshold": thresh,
            "threshold_label": f"{thresh*100:.1f}%",
            "min_occurrences": min_occ,
            "total_features": total_features,
            "features_retained": n_retained,
            "features_removed": n_removed,
            "fraction_retained": round(frac_retained, 6),
            "samples_with_zero_retained": n_zero_samples,
        })

    return pd.DataFrame(records)


def compute_preprocessing_summary(
    modality_results: Dict[str, Dict],
) -> pd.DataFrame:
    records = []
    for modality, mod_results in modality_results.items():
        if not isinstance(mod_results, dict):
            continue
        for strategy_key, strategy_res in mod_results.items():
            if not isinstance(strategy_res, dict):
                continue
            if strategy_key == "clr_pca":
                for clr_key, clr_res in strategy_res.items():
                    thresh_info = clr_res.get("threshold_info", {})
                    evr = clr_res.get("explained_variance_ratio", None)
                    pc1_var = evr[0] if evr and len(evr) > 0 else None
                    pc2_var = evr[1] if evr and len(evr) > 1 else None
                    records.append({
                        "modality": modality,
                        "strategy": "CLR_PCA",
                        "prevalence_threshold": thresh_info.get("threshold", None),
                        "engine": clr_res.get("engine", "none"),
                        "success": clr_res.get("success", False),
                        "n_features_retained": thresh_info.get("features_after", None),
                        "pc1_explained_variance": pc1_var,
                        "pc2_explained_variance": pc2_var,
                    })
            else:
                is_nmds = "nmds" in strategy_key
                engine = strategy_res.get("engine", "none")
                coords = strategy_res.get("coordinates", None)
                n_components = coords.shape[1] if coords is not None else 0
                stress = strategy_res.get("stress", None)
                eigvals = strategy_res.get("eigvals", None)
                pc1_var = eigvals[0] if eigvals and len(eigvals) > 0 else stress
                records.append({
                    "modality": modality,
                    "strategy": strategy_key.replace("_pcoa", "_PCoA").replace("_nmds", "_NMDS"),
                    "prevalence_threshold": None,
                    "engine": engine,
                    "success": strategy_res.get("success", False),
                    "n_features_retained": None,
                    "pc1_explained_variance": pc1_var,
                    "pc2_explained_variance": eigvals[1] if eigvals and len(eigvals) > 1 else None,
                })
    return pd.DataFrame(records)
