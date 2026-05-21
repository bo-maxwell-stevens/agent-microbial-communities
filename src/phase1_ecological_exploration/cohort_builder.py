from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import pandas as pd


def _serialize(obj):
    if isinstance(obj, list) and all(isinstance(x, str) for x in obj):
        return {"count": len(obj), "items": obj}
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def build_cohorts(
    datasets: Dict,
) -> Dict:
    meta_df = datasets["META"]["otu"]
    canonical_col = "canonical"
    if canonical_col not in meta_df.columns:
        raise KeyError(
            f"Column '{canonical_col}' not found in META dataset. "
            f"Available: {list(meta_df.columns)[:10]}..."
        )

    sample_ids = list(meta_df[canonical_col].dropna().unique())
    sample_set = set(sample_ids)

    modality_specific_cohorts = {}
    for k in ["AMF", "BAC", "EUK", "ITS"]:
        otu = datasets[k]["otu"]
        otu_samples = set(otu.index.astype(str))
        present = sorted(otu_samples & sample_set)
        missing = sorted(sample_set - otu_samples)
        modality_specific_cohorts[k] = {
            "samples_present": present,
            "samples_missing": missing,
        }

    otu_sets = {
        k: set(datasets[k]["otu"].index.astype(str))
        for k in ["AMF", "BAC", "EUK", "ITS"]
    }
    all_microbial = sorted(
        otu_sets["AMF"] & otu_sets["BAC"] & otu_sets["EUK"] & otu_sets["ITS"]
    )
    microbial_plus_metadata = sorted(
        s for s in all_microbial if s in sample_set
    )

    region_counts = (
        meta_df["region"].value_counts().to_dict()
        if "region" in meta_df.columns
        else {}
    )

    cohort_info = {
        "cohort_name": "darkdivnet_phase1_cohort",
        "description": (
            "Primary analytic cohort for Phase 1 ecological exploration. "
            "Samples are those present in Final_data_with_diversity_prefixed.csv "
            "and form the intersection of available metadata and at least one "
            "microbial kingdom dataset."
        ),
        "total_samples": len(sample_ids),
        "sample_ids": sample_ids,
        "all_microbial_overlap": all_microbial,
        "microbial_plus_metadata_overlap": microbial_plus_metadata,
        "modality_specific_cohorts": modality_specific_cohorts,
        "region_counts": region_counts,
    }

    return cohort_info


def write_cohort_definition(cohort_info: Dict, path: Path) -> None:
    serializable = _serialize(cohort_info)
    path.write_text(json.dumps(serializable, indent=2))
