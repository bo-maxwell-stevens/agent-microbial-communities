from __future__ import annotations

from pathlib import Path

import pandas as pd


def compute_overlap_summary(
    communities: dict[str, pd.DataFrame],
    sample_manifest: pd.DataFrame,
) -> pd.DataFrame:
    kingdom_keys = ["AMF", "BAC", "EUK", "ITS"]

    sample_sets = {
        modality: set(communities[modality].index.astype(str))
        for modality in kingdom_keys
    }
    meta_samples = set(sample_manifest["sample_id"].astype(str))

    pair_rows = []
    all_keys = kingdom_keys + ["META"]
    for i, left in enumerate(all_keys):
        for right in all_keys[i + 1 :]:
            left_set = sample_sets.get(left, meta_samples)
            right_set = sample_sets.get(right, meta_samples)
            overlap = len(left_set.intersection(right_set))
            union_size = len(left_set.union(right_set))
            pair_rows.append(
                {
                    "dataset_1": left,
                    "dataset_2": right,
                    "overlap_count": overlap,
                    "dataset_1_size": len(left_set),
                    "dataset_2_size": len(right_set),
                    "jaccard": round(overlap / union_size, 4) if union_size else 0.0,
                }
            )

    summary_rows = []
    for modality in kingdom_keys:
        otu = communities[modality]
        present = sum(1 for s in sample_manifest["sample_id"].astype(str) if s in otu.index)
        absent = len(sample_manifest) - present
        summary_rows.append(
            {
                "kingdom": modality,
                "samples_in_otu_table": len(otu),
                "samples_in_meta": present,
                "samples_missing_from_meta": absent,
                "otu_count": otu.shape[1],
            }
        )

    for pair in pair_rows:
        summary_rows.append(
            {
                "kingdom": f"{pair['dataset_1']}_vs_{pair['dataset_2']}",
                "samples_in_otu_table": pair["overlap_count"],
                "samples_in_meta": pair["dataset_1_size"],
                "samples_missing_from_meta": pair["dataset_2_size"],
                "otu_count": pair["jaccard"],
            }
        )

    return pd.DataFrame(summary_rows)


def write_overlap_summary(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
