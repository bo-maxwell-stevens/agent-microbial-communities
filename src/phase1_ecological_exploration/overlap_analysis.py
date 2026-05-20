from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def compute_overlap_summary(
    datasets: Dict,
) -> pd.DataFrame:
    kingdom_keys = ["AMF", "BAC", "EUK", "ITS"]
    sample_sets = {}
    for k in kingdom_keys:
        sample_sets[k] = set(datasets[k]["otu"].index.astype(str))

    meta_samples = set(datasets["META"]["otu"].iloc[:, 0].astype(str))

    pairs = []
    all_keys = kingdom_keys + ["META"]
    for i, k1 in enumerate(all_keys):
        for k2 in all_keys[i + 1 :]:
            s1 = sample_sets.get(k1, meta_samples)
            s2 = sample_sets.get(k2, meta_samples)
            overlap = len(s1 & s2)
            pairs.append(
                {
                    "dataset_1": k1,
                    "dataset_2": k2,
                    "overlap_count": overlap,
                    "dataset_1_size": len(s1),
                    "dataset_2_size": len(s2),
                    "jaccard": (
                        round(
                            overlap / len(s1 | s2), 4
                        )
                        if s1 | s2
                        else 0.0
                    ),
                }
            )

    rows = []
    for k in kingdom_keys:
        otu = datasets[k]["otu"]
        present = sum(1 for s in meta_samples if s in otu.index)
        absent = len(meta_samples) - present
        rows.append(
            {
                "kingdom": k,
                "samples_in_otu_table": len(otu),
                "samples_in_meta": present,
                "samples_missing_from_meta": absent,
                "otu_count": otu.shape[1],
            }
        )

    summary_rows = []
    for r in rows:
        summary_rows.append(r)
    for p in pairs:
        summary_rows.append(
            {
                "kingdom": f"{p['dataset_1']}_vs_{p['dataset_2']}",
                "samples_in_otu_table": p["overlap_count"],
                "samples_in_meta": p["dataset_1_size"],
                "samples_missing_from_meta": p["dataset_2_size"],
                "otu_count": p["jaccard"],
            }
        )

    result = pd.DataFrame(summary_rows)
    return result


def write_overlap_summary(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)
