from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.data_loading import (
    AMF_IDENTIFIER_STATUS_COLUMN,
    AMF_IDENTIFIER_STATUS_UNRESOLVED,
    AMF_UNRESOLVED_FEATURE_ID,
    AMF_UNRESOLVED_SOURCE_COLUMN,
    METADATA_SAMPLE_ID_COLUMN,
    build_sample_manifest,
    load_project_data,
)


def _write_tsv(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _write_minimal_non_amf_files(data_dir: Path) -> None:
    _write_tsv(data_dir / "BAC_OTU_table_final.tsv", "sample_id\tOTU1\nS1\t1\nS2\t0\n")
    _write_tsv(data_dir / "EUK_OTU_table_final.tsv", "sample_id\tOTU1\nS1\t1\nS2\t0\n")
    _write_tsv(data_dir / "ITS_OTU_table_final.tsv", "sample_id\tSH1\nS1\t1\nS2\t0\n")

    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "BAC_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "EUK_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"SH": ["SH1"]}).to_csv(data_dir / "ITS_feature_metadata.tsv", sep="\t", index=False)

    pd.DataFrame({METADATA_SAMPLE_ID_COLUMN: ["S1", "S2"]}).to_csv(
        data_dir / "Final_data_with_diversity_prefixed.csv",
        index=False,
    )


def _write_amf_case(
    data_dir: Path,
    *,
    amf_otu_header: list[str],
    amf_otu_rows: list[list[int]],
    amf_vt_rows: list[object],
) -> None:
    header = "\t".join(["sample_id", *amf_otu_header])
    row_lines = []
    for sample_id, values in zip(["S1", "S2"], amf_otu_rows, strict=True):
        row_lines.append("\t".join([sample_id, *[str(v) for v in values]]))
    _write_tsv(data_dir / "AMF_OTU_table_final.tsv", header + "\n" + "\n".join(row_lines) + "\n")

    pd.DataFrame({"VT": amf_vt_rows}).to_csv(data_dir / "AMF_feature_metadata.tsv", sep="\t", index=False)


def _base_amf_valid_case(data_dir: Path, unresolved_values: tuple[int, int] = (0, 5583)) -> None:
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", "VTX002", AMF_UNRESOLVED_SOURCE_COLUMN],
        amf_otu_rows=[[10, 2, unresolved_values[0]], [4, 1, unresolved_values[1]]],
        amf_vt_rows=["VTX001", "VTX002", None],
    )


def test_unresolved_amf_feature_is_retained_and_values_unchanged(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _base_amf_valid_case(data_dir, unresolved_values=(0, 5583))
    _write_minimal_non_amf_files(data_dir)

    with pytest.warns(UserWarning, match="AMF unresolved feature retained"):
        project_data = load_project_data(data_dir)

    amf = project_data.communities["AMF"]
    assert AMF_UNRESOLVED_SOURCE_COLUMN not in amf.columns
    assert AMF_UNRESOLVED_FEATURE_ID in amf.columns
    assert amf.loc["S1", AMF_UNRESOLVED_FEATURE_ID] == 0
    assert amf.loc["S2", AMF_UNRESOLVED_FEATURE_ID] == 5583


def test_placeholder_identifier_assigned_to_amf_abundance_and_metadata_consistently(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _base_amf_valid_case(data_dir)
    _write_minimal_non_amf_files(data_dir)

    with pytest.warns(UserWarning):
        project_data = load_project_data(data_dir)

    amf = project_data.communities["AMF"]
    amf_meta = project_data.feature_metadata["AMF"]
    assert amf.columns[-1] == AMF_UNRESOLVED_FEATURE_ID
    assert amf_meta["VT"].iloc[-1] == AMF_UNRESOLVED_FEATURE_ID
    assert AMF_IDENTIFIER_STATUS_COLUMN in amf_meta.columns
    assert amf_meta[AMF_IDENTIFIER_STATUS_COLUMN].iloc[-1] == AMF_IDENTIFIER_STATUS_UNRESOLVED


def test_leading_valid_vt_ids_remain_unchanged_and_ordered(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _base_amf_valid_case(data_dir)
    _write_minimal_non_amf_files(data_dir)

    with pytest.warns(UserWarning):
        project_data = load_project_data(data_dir)

    assert project_data.communities["AMF"].columns[:2].tolist() == ["VTX001", "VTX002"]
    assert project_data.feature_metadata["AMF"]["VT"].iloc[:2].tolist() == ["VTX001", "VTX002"]


def test_nonzero_unresolved_feature_is_never_dropped(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _base_amf_valid_case(data_dir, unresolved_values=(7, 5583))
    _write_minimal_non_amf_files(data_dir)

    with pytest.warns(UserWarning):
        project_data = load_project_data(data_dir)

    amf = project_data.communities["AMF"]
    assert amf.shape[1] == 3
    assert AMF_UNRESOLVED_FEATURE_ID in amf.columns
    assert int(amf[AMF_UNRESOLVED_FEATURE_ID].sum()) == 5590


def test_rule_fails_if_unnamed_column_is_not_last(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", AMF_UNRESOLVED_SOURCE_COLUMN, "VTX002"],
        amf_otu_rows=[[10, 0, 2], [4, 5583, 1]],
        amf_vt_rows=["VTX001", "VTX002", None],
    )
    _write_minimal_non_amf_files(data_dir)

    with pytest.raises(ValueError, match="not the trailing abundance feature"):
        load_project_data(data_dir)


def test_rule_fails_if_blank_metadata_row_missing(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", "VTX002", AMF_UNRESOLVED_SOURCE_COLUMN],
        amf_otu_rows=[[10, 2, 0], [4, 1, 5583]],
        amf_vt_rows=["VTX001", "VTX002", "VTX003"],
    )
    _write_minimal_non_amf_files(data_dir)

    with pytest.raises(ValueError, match="exactly one blank VT row"):
        load_project_data(data_dir)


def test_rule_fails_if_more_than_one_unnamed_amf_feature_exists(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", "Unnamed: 100", AMF_UNRESOLVED_SOURCE_COLUMN],
        amf_otu_rows=[[10, 0, 0], [4, 1, 5583]],
        amf_vt_rows=["VTX001", "VTX002", None],
    )
    _write_minimal_non_amf_files(data_dir)

    with pytest.raises(ValueError, match="exactly one unnamed abundance feature"):
        load_project_data(data_dir)


def test_rule_fails_if_leading_abundance_and_metadata_ids_do_not_match(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", "VTX999", AMF_UNRESOLVED_SOURCE_COLUMN],
        amf_otu_rows=[[10, 2, 0], [4, 1, 5583]],
        amf_vt_rows=["VTX001", "VTX002", None],
    )
    _write_minimal_non_amf_files(data_dir)

    with pytest.raises(ValueError, match="leading abundance and VT identifiers do not match"):
        load_project_data(data_dir)


def test_rule_fails_if_blank_vt_row_is_not_last(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _write_amf_case(
        data_dir,
        amf_otu_header=["VTX001", "VTX002", AMF_UNRESOLVED_SOURCE_COLUMN],
        amf_otu_rows=[[10, 2, 0], [4, 1, 5583]],
        amf_vt_rows=[None, "VTX001", "VTX002"],
    )
    _write_minimal_non_amf_files(data_dir)

    with pytest.raises(ValueError, match="blank VT row must be the final"):
        load_project_data(data_dir)


def test_warning_mentions_placeholder_and_non_identified_vt(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    _base_amf_valid_case(data_dir)
    _write_minimal_non_amf_files(data_dir)

    with pytest.warns(UserWarning, match=r"AMF_UNRESOLVED_FEATURE_386") as rec:
        load_project_data(data_dir)

    text = str(rec.list[0].message)
    assert "Do not interpret this placeholder as an identified MaarjAM VT" in text
    assert "total_reads=5583" in text


def test_load_project_data_requires_canonical_metadata_column(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    _write_tsv(data_dir / "AMF_OTU_table_final.tsv", "sample_id\tVTX001\nS1\t1\n")
    _write_tsv(data_dir / "BAC_OTU_table_final.tsv", "sample_id\tOTU1\nS1\t1\n")
    _write_tsv(data_dir / "EUK_OTU_table_final.tsv", "sample_id\tOTU1\nS1\t1\n")
    _write_tsv(data_dir / "ITS_OTU_table_final.tsv", "sample_id\tSH1\nS1\t1\n")

    pd.DataFrame({"wrong_id": ["S1"]}).to_csv(data_dir / "Final_data_with_diversity_prefixed.csv", index=False)
    pd.DataFrame({"VT": ["VTX001"]}).to_csv(data_dir / "AMF_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "BAC_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "EUK_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"SH": ["SH1"]}).to_csv(data_dir / "ITS_feature_metadata.tsv", sep="\t", index=False)

    with pytest.raises(KeyError, match=METADATA_SAMPLE_ID_COLUMN):
        load_project_data(data_dir)


def test_build_sample_manifest_tracks_membership_in_metadata_order(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    _write_tsv(data_dir / "AMF_OTU_table_final.tsv", "sample_id\tVTX001\nS1\t1\n")
    _write_tsv(data_dir / "BAC_OTU_table_final.tsv", "sample_id\tOTU1\nS2\t1\n")
    _write_tsv(data_dir / "EUK_OTU_table_final.tsv", "sample_id\tOTU1\nS1\t1\nS2\t1\n")
    _write_tsv(data_dir / "ITS_OTU_table_final.tsv", "sample_id\tSH1\nS1\t1\n")

    pd.DataFrame({METADATA_SAMPLE_ID_COLUMN: ["S2", "S1"]}).to_csv(
        data_dir / "Final_data_with_diversity_prefixed.csv",
        index=False,
    )
    pd.DataFrame({"VT": ["VTX001"]}).to_csv(data_dir / "AMF_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "BAC_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"OTU": ["OTU1"]}).to_csv(data_dir / "EUK_feature_metadata.tsv", sep="\t", index=False)
    pd.DataFrame({"SH": ["SH1"]}).to_csv(data_dir / "ITS_feature_metadata.tsv", sep="\t", index=False)

    project_data = load_project_data(data_dir)
    manifest = build_sample_manifest(project_data)

    assert manifest["sample_id"].tolist() == ["S2", "S1"]
    assert manifest[["in_AMF", "in_BAC", "in_EUK", "in_ITS", "in_META"]].shape == (2, 5)
