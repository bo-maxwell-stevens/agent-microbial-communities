from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import pandas as pd


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
        "kingdom_coverage": {},
    }

    for k in ["AMF", "BAC", "EUK", "ITS"]:
        otu = datasets[k]["otu"]
        present = [s for s in sample_ids if s in otu.index]
        cohort_info["kingdom_coverage"][k] = {
            "samples_present": len(present),
            "sample_ids": present,
        }

    cohort_info["all_kingdoms_present"] = [
        s
        for s in sample_ids
        if all(
            s in datasets[k]["otu"].index
            for k in ["AMF", "BAC", "EUK", "ITS"]
        )
    ]
    cohort_info["count_all_kingdoms_present"] = len(
        cohort_info["all_kingdoms_present"]
    )

    region_counts = (
        meta_df["region"].value_counts().to_dict()
        if "region" in meta_df.columns
        else {}
    )
    cohort_info["region_counts"] = region_counts

    return cohort_info


def write_cohort_definition(cohort_info: Dict, path: Path) -> None:
    serializable = {}
    for k, v in cohort_info.items():
        if isinstance(v, list) and v and isinstance(v[0], str):
            serializable[k] = {"count": len(v), "items": v}
        elif isinstance(v, dict):
            cleaned = {}
            for kk, vv in v.items():
                if isinstance(vv, dict) and "sample_ids" in vv:
                    cleaned[kk] = {
                        "samples_present": vv["samples_present"],
                        "sample_ids": vv["sample_ids"],
                    }
                else:
                    cleaned[kk] = vv
            serializable[k] = cleaned
        else:
            serializable[k] = v
    path.write_text(json.dumps(serializable, indent=2))
