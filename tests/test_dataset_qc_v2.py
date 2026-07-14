import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


def load_qc_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "01_data_qc.py"
    spec = importlib.util.spec_from_file_location("dataset_qc_v2", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_metadata_requires_explicit_sample_column(tmp_path):
    qc = load_qc_module()
    meta_path = tmp_path / "meta.csv"
    pd.DataFrame({"wrong": ["S1", "S2"]}).to_csv(meta_path, index=False)
    with pytest.raises(ValueError, match="sample-ID column"):
        qc.load_main_metadata_samples(meta_path, sample_column="canonical")


def test_validate_abundance_matrix_rejects_nonnumeric():
    qc = load_qc_module()
    abundance = pd.DataFrame({"OTU1": [1, "bad"], "OTU2": [3, 4]}, index=["S1", "S2"])
    with pytest.raises(ValueError, match="nonnumeric"):
        qc.validate_abundance_matrix(abundance, modality="BAC", file_label="test")


def test_validate_abundance_matrix_rejects_missing_values():
    qc = load_qc_module()
    abundance = pd.DataFrame({"OTU1": [1, None], "OTU2": [3, 4]}, index=["S1", "S2"])
    with pytest.raises(ValueError, match="missing abundance"):
        qc.validate_abundance_matrix(abundance, modality="BAC", file_label="test")


def test_validate_abundance_matrix_rejects_negative_values():
    qc = load_qc_module()
    abundance = pd.DataFrame({"OTU1": [1, -2], "OTU2": [3, 4]}, index=["S1", "S2"])
    with pytest.raises(ValueError, match="Negative abundance"):
        qc.validate_abundance_matrix(abundance, modality="BAC", file_label="test")


def test_collect_duplicate_ids_counts_true_duplicates():
    qc = load_qc_module()
    dup_df = qc.collect_duplicate_ids(["S1", "S2", "S1", "S1"], id_field="sample_id")
    assert dup_df.to_dict(orient="records") == [{"sample_id": "S1", "count": 3}]


def test_prevalence_preserves_taxon_ids():
    qc = load_qc_module()
    abundance = pd.DataFrame({"OTU_A": [1, 0], "OTU_B": [1, 1]}, index=["S1", "S2"])
    prev = qc.compute_prevalence(abundance)
    assert list(prev.index) == ["OTU_A", "OTU_B"]
    assert prev.loc["OTU_A"] == 0.5
    assert prev.loc["OTU_B"] == 1.0


def test_normalize_index_preserves_row_alignment_after_cleaning():
    qc = load_qc_module()
    abundance = pd.DataFrame({"OTU1": [10, 20]}, index=[" S1 ", "S2"])
    cleaned = qc.normalize_identifier_index(abundance.index, label="abundance index")
    abundance.index = cleaned
    assert list(abundance.index) == ["S1", "S2"]
    assert abundance.loc["S1", "OTU1"] == 10
