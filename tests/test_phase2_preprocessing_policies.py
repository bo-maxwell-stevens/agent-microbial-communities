from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_module(rel_path: str, module_name: str):
    path = REPO_ROOT / rel_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


p2 = _load_module("scripts/04_cross_kingdom_coupling.py", "phase2_policy_mod")


def test_no_feature_prevalence_result_raises_clear_error():
    tbl = pd.DataFrame({"f1": [0, 0, 0], "f2": [0, 0, 0]}, index=["S1", "S2", "S3"])
    with pytest.raises(ValueError, match=r"modality=AMF") as exc:
        p2.prepare_branch_modality(tbl, ["S1", "S2", "S3"], threshold=0.5, branch="CLR", modality="AMF")
    msg = str(exc.value)
    assert "threshold=0.5" in msg
    assert "n_samples=3" in msg
    assert "min_occurrences=2" in msg


def test_threshold_behavior_unchanged_when_features_pass():
    tbl = pd.DataFrame(
        {
            "keep": [1, 0, 1, 0],
            "drop": [1, 0, 0, 0],
        },
        index=["S1", "S2", "S3", "S4"],
    )
    out = p2.prepare_branch_modality(tbl, ["S1", "S2", "S3", "S4"], threshold=0.5, branch="presence/absence", modality="AMF")
    assert out["n_features"] == 1
    assert out["transformed"].columns.tolist() == ["keep"]


def test_zero_library_rows_identified_after_filtering():
    tbl = pd.DataFrame(
        {
            "f1": [1, 1, 0, 1],
            "f2": [0, 1, 0, 1],
        },
        index=["S1", "S2", "S3", "S4"],
    )
    out = p2.prepare_branch_modality(tbl, ["S1", "S2", "S3", "S4"], threshold=0.5, branch="CLR", modality="AMF")
    assert out["excluded_zero_library_samples"] == ["S3"]
    assert "S3" not in out["transformed"].index


def test_zero_library_samples_removed_from_pair_and_order_identical():
    cohort = ["S1", "S2", "S3", "S4"]
    amf = pd.DataFrame({"f1": [1, 1, 0, 1], "f2": [0, 1, 0, 1]}, index=cohort)
    its = pd.DataFrame({"g1": [1, 1, 1, 1], "g2": [0, 1, 0, 1]}, index=cohort)

    out_amf = p2.prepare_branch_modality(amf, cohort, threshold=0.5, branch="CLR", modality="AMF")
    out_its = p2.prepare_branch_modality(its, cohort, threshold=0.5, branch="CLR", modality="ITS")

    called_orders: list[list[str]] = []
    original_euclidean = p2.euclidean_distance

    def _capture_order(df: pd.DataFrame):
        called_orders.append(df.index.tolist())
        return original_euclidean(df)

    p2.euclidean_distance = _capture_order
    try:
        row = p2.run_pair(out_amf, out_its, cohort, "AMF", "ITS")
    finally:
        p2.euclidean_distance = original_euclidean

    assert row["n_samples"] == 3
    assert row["excluded_zero_library_samples_a"] == "S3"
    assert row["excluded_zero_library_samples_b"] == ""
    assert len(called_orders) == 2
    assert called_orders[0] == called_orders[1]


def test_clr_pseudocount_is_explicit_1e6_minus():
    assert p2.CLR_PSEUDOCOUNT == pytest.approx(1e-6)

    cohort = ["S1", "S2", "S3"]
    amf = pd.DataFrame({"f1": [1, 1, 1], "f2": [1, 0, 1]}, index=cohort)

    captured = {}
    original_clr = p2.clr_transform

    def _capture(df: pd.DataFrame, pseudocount: float = 0.5):
        captured["pseudocount"] = pseudocount
        return original_clr(df, pseudocount=pseudocount)

    p2.clr_transform = _capture
    try:
        p2.prepare_branch_modality(amf, cohort, threshold=0.5, branch="CLR", modality="AMF")
    finally:
        p2.clr_transform = original_clr

    assert captured["pseudocount"] == pytest.approx(1e-6)


def test_real_data_d092_excluded_only_for_amf_clr_010_and_presence_absence_keeps_cohort():
    cohort = pd.read_csv(REPO_ROOT / "results/phase2_confirmatory_coupling/sample_cohort_used.csv")["Sample_ID"].astype(str).tolist()
    amf = pd.read_csv(REPO_ROOT / "data/AMF_OTU_table_final.tsv", sep="\t", index_col=0)
    its = pd.read_csv(REPO_ROOT / "data/ITS_OTU_table_final.tsv", sep="\t", index_col=0)
    euk = pd.read_csv(REPO_ROOT / "data/EUK_OTU_table_final.tsv", sep="\t", index_col=0)

    amf_clr = p2.prepare_branch_modality(amf, cohort, threshold=0.10, branch="CLR", modality="AMF")
    its_clr = p2.prepare_branch_modality(its, cohort, threshold=0.10, branch="CLR", modality="ITS")
    euk_clr = p2.prepare_branch_modality(euk, cohort, threshold=0.10, branch="CLR", modality="EUK")

    assert "D092.N1" in amf_clr["excluded_zero_library_samples"]
    assert "D092.N1" not in its_clr["excluded_zero_library_samples"]
    assert "D092.N1" not in euk_clr["excluded_zero_library_samples"]

    row_amf_its = p2.run_pair(amf_clr, its_clr, cohort, "AMF", "ITS")
    row_amf_euk = p2.run_pair(amf_clr, euk_clr, cohort, "AMF", "EUK")
    row_euk_its = p2.run_pair(euk_clr, its_clr, cohort, "EUK", "ITS")

    assert row_amf_its["n_samples"] == 83
    assert row_amf_euk["n_samples"] == 83
    assert row_euk_its["n_samples"] == 84

    amf_pa = p2.prepare_branch_modality(amf, cohort, threshold=0.10, branch="presence/absence", modality="AMF")
    its_pa = p2.prepare_branch_modality(its, cohort, threshold=0.10, branch="presence/absence", modality="ITS")
    row_pa = p2.run_pair(amf_pa, its_pa, cohort, "AMF", "ITS")
    assert row_pa["n_samples"] == 84


def test_output_contains_exclusion_audit_fields():
    expected = {
        "n_samples",
        "excluded_zero_library_samples_a",
        "excluded_zero_library_samples_b",
    }
    cohort = ["S1", "S2", "S3"]
    df = pd.DataFrame({"f1": [1, 1, 1], "f2": [1, 0, 1]}, index=cohort)
    out1 = p2.prepare_branch_modality(df, cohort, threshold=0.5, branch="CLR", modality="AMF")
    out2 = p2.prepare_branch_modality(df, cohort, threshold=0.5, branch="CLR", modality="ITS")
    row = p2.run_pair(out1, out2, cohort, "AMF", "ITS")
    assert expected.issubset(set(row.keys()))
