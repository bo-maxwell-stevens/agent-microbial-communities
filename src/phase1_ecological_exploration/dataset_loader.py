from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


MODALITIES = {
    "AMF": {
        "otu": "AMF_OTU_table_final.tsv",
        "meta": "AMF_feature_metadata.tsv",
        "sep": "\t",
    },
    "BAC": {
        "otu": "BAC_OTU_table_final.tsv",
        "meta": "BAC_feature_metadata.tsv",
        "sep": "\t",
    },
    "EUK": {
        "otu": "EUK_OTU_table_final.tsv",
        "meta": "EUK_feature_metadata.tsv",
        "sep": "\t",
    },
    "ITS": {
        "otu": "ITS_OTU_table_final.tsv",
        "meta": "ITS_feature_metadata.tsv",
        "sep": "\t",
    },
    "META": {
        "otu": "Final_data_with_diversity_prefixed.csv",
        "meta": None,
        "sep": ",",
    },
}


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_modality_otu(
    data_dir: Path, key: str
) -> tuple[pd.DataFrame, Dict[str, str]]:
    info = MODALITIES[key]
    path = data_dir / info["otu"]
    size = path.stat().st_size
    sha = file_sha256(path)
    if key == "META":
        df = pd.read_csv(path, sep=info["sep"], low_memory=False)
    else:
        df = pd.read_csv(path, sep=info["sep"], index_col=0, low_memory=False)
        df.columns = df.columns.astype(str)
        df = df.apply(pd.to_numeric, errors="coerce").fillna(0.0).astype(int)
    provenance = {"path": str(path), "size_bytes": size, "sha256": sha}
    return df, provenance


def load_modality_meta(
    data_dir: Path, key: str
) -> tuple[Optional[pd.DataFrame], Optional[Dict[str, str]]]:
    info = MODALITIES[key]
    if info["meta"] is None:
        return None, None
    path = data_dir / info["meta"]
    size = path.stat().st_size
    sha = file_sha256(path)
    df = pd.read_csv(path, sep=info["sep"], index_col=0, low_memory=False)
    df.columns = df.columns.astype(str)
    provenance = {"path": str(path), "size_bytes": size, "sha256": sha}
    return df, provenance


def load_all_datasets(data_dir: str | Path) -> Dict:
    data_dir = Path(data_dir)
    datasets = {}
    provenance = {}
    for key in MODALITIES:
        otu, otu_prov = load_modality_otu(data_dir, key)
        meta, meta_prov = load_modality_meta(data_dir, key)
        datasets[key] = {"otu": otu, "meta": meta}
        provenance[key] = {"otu": otu_prov, "meta": meta_prov}
    return datasets, provenance
