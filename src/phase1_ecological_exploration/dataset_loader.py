from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd

from src.data_loading import (
    ABUNDANCE_FILES,
    FEATURE_METADATA_FILES,
    METADATA_FILE,
    MODALITIES,
    ProjectData,
    build_sample_manifest,
    load_project_data,
)

# Temporary compatibility adapter: prefer importing from src.data_loading in new code.


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_input_provenance(data_dir: str | Path) -> dict[str, dict[str, dict[str, str | int] | None]]:
    data_dir = Path(data_dir)
    provenance: dict[str, dict[str, dict[str, str | int] | None]] = {}

    for modality in MODALITIES:
        otu_path = data_dir / ABUNDANCE_FILES[modality]
        meta_path = data_dir / FEATURE_METADATA_FILES[modality]
        provenance[modality] = {
            "otu": {
                "path": str(otu_path),
                "size_bytes": otu_path.stat().st_size,
                "sha256": file_sha256(otu_path),
            },
            "meta": {
                "path": str(meta_path),
                "size_bytes": meta_path.stat().st_size,
                "sha256": file_sha256(meta_path),
            },
        }

    metadata_path = data_dir / METADATA_FILE
    provenance["META"] = {
        "otu": {
            "path": str(metadata_path),
            "size_bytes": metadata_path.stat().st_size,
            "sha256": file_sha256(metadata_path),
        },
        "meta": None,
    }

    return provenance


def to_legacy_datasets(project_data: ProjectData) -> dict[str, dict[str, pd.DataFrame | None]]:
    datasets: dict[str, dict[str, pd.DataFrame | None]] = {}
    for modality in MODALITIES:
        datasets[modality] = {
            "otu": project_data.communities[modality],
            "meta": project_data.feature_metadata[modality],
        }
    datasets["META"] = {"otu": project_data.metadata, "meta": None}
    return datasets


def load_all_datasets(data_dir: str | Path):
    project_data = load_project_data(data_dir)
    datasets = to_legacy_datasets(project_data)
    provenance = build_input_provenance(data_dir)
    return datasets, provenance


def load_all_datasets_with_manifest(data_dir: str | Path):
    project_data = load_project_data(data_dir)
    datasets = to_legacy_datasets(project_data)
    provenance = build_input_provenance(data_dir)
    sample_manifest = build_sample_manifest(project_data)
    return datasets, provenance, sample_manifest
