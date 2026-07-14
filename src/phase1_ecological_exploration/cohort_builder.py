from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _serialize(obj):
    if isinstance(obj, list) and all(isinstance(x, str) for x in obj):
        return {"count": len(obj), "items": obj}
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


def build_cohorts(
    communities: dict[str, pd.DataFrame],
    metadata: pd.DataFrame,
    sample_manifest: pd.DataFrame,
) -> dict:
    sample_ids = sample_manifest["sample_id"].astype(str).tolist()
    sample_set = set(sample_ids)

    modality_specific_cohorts = {}
    for modality in ["AMF", "BAC", "EUK", "ITS"]:
        otu_samples = set(communities[modality].index.astype(str))
        present = sorted(otu_samples.intersection(sample_set))
        missing = sorted(sample_set.difference(otu_samples))
        modality_specific_cohorts[modality] = {
            "samples_present": present,
            "samples_missing": missing,
        }

    otu_sets = {
        modality: set(communities[modality].index.astype(str))
        for modality in ["AMF", "BAC", "EUK", "ITS"]
    }
    all_microbial = sorted(
        otu_sets["AMF"].intersection(otu_sets["BAC"], otu_sets["EUK"], otu_sets["ITS"])
    )
    microbial_plus_metadata = sorted(s for s in all_microbial if s in sample_set)

    region_counts = metadata["region"].value_counts().to_dict() if "region" in metadata.columns else {}

    return {
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


def write_cohort_definition(cohort_info: dict, path: Path) -> None:
    path.write_text(json.dumps(_serialize(cohort_info), indent=2))
