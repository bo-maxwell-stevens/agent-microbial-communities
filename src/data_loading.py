from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import warnings

import pandas as pd

METADATA_SAMPLE_ID_COLUMN = "canonical"
METADATA_FILE = "Final_data_with_diversity_prefixed.csv"

MODALITIES: tuple[str, ...] = ("AMF", "BAC", "EUK", "ITS")

ABUNDANCE_FILES: dict[str, str] = {
    "AMF": "AMF_OTU_table_final.tsv",
    "BAC": "BAC_OTU_table_final.tsv",
    "EUK": "EUK_OTU_table_final.tsv",
    "ITS": "ITS_OTU_table_final.tsv",
}

FEATURE_METADATA_FILES: dict[str, str] = {
    "AMF": "AMF_feature_metadata.tsv",
    "BAC": "BAC_feature_metadata.tsv",
    "EUK": "EUK_feature_metadata.tsv",
    "ITS": "ITS_feature_metadata.tsv",
}

FEATURE_ID_COLUMNS: dict[str, str] = {
    "AMF": "VT",
    "BAC": "OTU",
    "EUK": "OTU",
    "ITS": "SH",
}

# Explicit AMF source-file defect handling (project-specific).
AMF_UNRESOLVED_SOURCE_COLUMN = "Unnamed: 386"
AMF_UNRESOLVED_FEATURE_ID = "AMF_UNRESOLVED_FEATURE_386"
AMF_IDENTIFIER_STATUS_COLUMN = "identifier_status"
AMF_IDENTIFIER_STATUS_UNRESOLVED = "unresolved_export_id"


@dataclass(frozen=True)
class ProjectData:
    """Authoritative project loading output."""

    communities: dict[str, pd.DataFrame]
    metadata: pd.DataFrame
    feature_metadata: dict[str, pd.DataFrame]


def _clean_string_series(series: pd.Series, *, source: str) -> pd.Series:
    if series.isna().any():
        raise ValueError(f"{source}: contains missing values")
    cleaned = series.astype(str).str.strip()
    if cleaned.eq("").any():
        raise ValueError(f"{source}: contains blank values")
    return cleaned


def _validate_unique(values: pd.Series, *, source: str) -> None:
    if not values.is_unique:
        dupes = values[values.duplicated()].unique().tolist()[:5]
        raise ValueError(f"{source}: duplicate values detected, examples={dupes}")


def _load_abundance_table(path: Path, modality: str) -> pd.DataFrame:
    raw = pd.read_csv(path, sep="\t", low_memory=False)
    if raw.shape[1] < 2:
        raise ValueError(f"{modality}: abundance table must contain sample ID + at least one feature column")

    sample_ids = _clean_string_series(raw.iloc[:, 0], source=f"{modality} sample IDs")
    _validate_unique(sample_ids, source=f"{modality} sample IDs")

    feature_ids = pd.Series(raw.columns[1:]).astype(str).str.strip()
    if feature_ids.eq("").any():
        raise ValueError(f"{modality}: feature columns contain blank names")
    _validate_unique(feature_ids, source=f"{modality} abundance feature IDs")

    abundance_raw = raw.iloc[:, 1:]
    if abundance_raw.isna().to_numpy().any():
        raise ValueError(f"{modality}: abundance table contains missing cells")

    abundance = abundance_raw.apply(pd.to_numeric, errors="coerce")
    if abundance.isna().to_numpy().any():
        raise ValueError(f"{modality}: abundance table contains nonnumeric values")

    if (abundance < 0).to_numpy().any():
        raise ValueError(f"{modality}: abundance table contains negative values")

    abundance.index = sample_ids.to_numpy()
    abundance.columns = feature_ids.to_list()
    return abundance


def _load_feature_metadata(path: Path, modality: str) -> pd.DataFrame:
    feature_df = pd.read_csv(path, sep="\t", low_memory=False)
    feature_id_col = FEATURE_ID_COLUMNS[modality]
    if feature_id_col not in feature_df.columns:
        raise KeyError(
            f"{modality}: expected feature ID column {feature_id_col!r} in {path.name}; "
            f"found {feature_df.columns[:10].tolist()}"
        )
    return feature_df


def _apply_amf_unresolved_feature_rule(
    abundance: pd.DataFrame,
    feature_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, str | None]:
    """Apply one explicit AMF unresolved-feature correction.

    Required AMF structure:
    - exactly one unnamed abundance feature and it is the final column
    - that final abundance feature is exactly 'Unnamed: 386'
    - exactly one blank VT row in AMF feature metadata and it is final
    - all leading 385 abundance IDs exactly match leading 385 VT values

    Behavior:
    - preserve abundance values exactly
    - rename unresolved abundance feature to AMF_UNRESOLVED_FEATURE_386
    - replace blank VT with AMF_UNRESOLVED_FEATURE_386
    - annotate metadata status column with unresolved_export_id for that row
    """

    unnamed_columns = [c for c in abundance.columns if str(c).startswith("Unnamed:")]
    if not unnamed_columns:
        return abundance, feature_df, None

    if len(unnamed_columns) != 1:
        raise ValueError(
            f"AMF: expected exactly one unnamed abundance feature column, found {unnamed_columns}"
        )

    unnamed_col = unnamed_columns[0]
    if unnamed_col != AMF_UNRESOLVED_SOURCE_COLUMN:
        raise ValueError(
            f"AMF: expected final unresolved source column {AMF_UNRESOLVED_SOURCE_COLUMN!r}, found {unnamed_col!r}"
        )

    if abundance.columns[-1] != AMF_UNRESOLVED_SOURCE_COLUMN:
        raise ValueError(
            "AMF: unresolved source column exists but is not the trailing abundance feature"
        )

    if FEATURE_ID_COLUMNS["AMF"] not in feature_df.columns:
        raise KeyError("AMF: VT column is required in AMF_feature_metadata.tsv")

    vt_raw = feature_df["VT"]
    vt_blank = vt_raw.isna() | vt_raw.astype(str).str.strip().eq("")
    if vt_blank.sum() != 1:
        raise ValueError("AMF: expected exactly one blank VT row to align with unresolved source feature")

    blank_idx = vt_blank[vt_blank].index[0]
    if blank_idx != len(feature_df) - 1:
        raise ValueError("AMF: blank VT row must be the final AMF feature metadata row")

    if abundance.shape[1] != feature_df.shape[0]:
        raise ValueError(
            "AMF: abundance feature count must match AMF feature metadata row count before unresolved-feature repair"
        )

    leading_abundance = abundance.columns[:-1].astype(str).tolist()
    leading_metadata = vt_raw.iloc[:-1].astype(str).str.strip().tolist()
    if leading_abundance != leading_metadata:
        raise ValueError("AMF: leading abundance and VT identifiers do not match before unresolved-feature repair")

    repaired_abundance = abundance.rename(columns={AMF_UNRESOLVED_SOURCE_COLUMN: AMF_UNRESOLVED_FEATURE_ID})
    repaired_feature_df = feature_df.copy()
    repaired_feature_df.loc[blank_idx, "VT"] = AMF_UNRESOLVED_FEATURE_ID

    if AMF_IDENTIFIER_STATUS_COLUMN not in repaired_feature_df.columns:
        repaired_feature_df[AMF_IDENTIFIER_STATUS_COLUMN] = ""
    repaired_feature_df.loc[blank_idx, AMF_IDENTIFIER_STATUS_COLUMN] = AMF_IDENTIFIER_STATUS_UNRESOLVED

    unresolved_series = repaired_abundance[AMF_UNRESOLVED_FEATURE_ID]
    nonzero_series = unresolved_series[unresolved_series != 0]
    warning_message = (
        "AMF unresolved feature retained under AMF_UNRESOLVED_FEATURE_386: "
        "no recoverable VT identifier in source export; "
        f"nonzero_samples={int(nonzero_series.shape[0])}; "
        f"total_reads={int(unresolved_series.sum())}. "
        "Do not interpret this placeholder as an identified MaarjAM VT."
    )

    return repaired_abundance, repaired_feature_df, warning_message


def _validate_feature_alignment(
    modality: str,
    abundance: pd.DataFrame,
    feature_df: pd.DataFrame,
) -> pd.DataFrame:
    feature_id_col = FEATURE_ID_COLUMNS[modality]

    feature_ids = feature_df[feature_id_col]
    if feature_ids.isna().any() or feature_ids.astype(str).str.strip().eq("").any():
        raise ValueError(f"{modality}: missing feature IDs detected in {feature_id_col}")

    feature_ids = feature_ids.astype(str).str.strip()
    _validate_unique(feature_ids, source=f"{modality} feature metadata IDs")

    abundance_ids = abundance.columns.astype(str)
    abundance_id_set = set(abundance_ids)
    feature_id_set = set(feature_ids)

    features_missing_metadata = [x for x in abundance_ids if x not in feature_id_set]
    metadata_features_not_in_abundance = [x for x in feature_ids if x not in abundance_id_set]
    if features_missing_metadata or metadata_features_not_in_abundance:
        raise ValueError(
            f"{modality}: feature ID mismatch; "
            f"features_missing_metadata={features_missing_metadata[:5]}, "
            f"metadata_features_not_in_abundance={metadata_features_not_in_abundance[:5]}"
        )

    if abundance_ids.tolist() != feature_ids.tolist():
        raise ValueError(f"{modality}: feature order mismatch between abundance table and feature metadata")

    aligned_feature_df = feature_df.copy()
    aligned_feature_df[feature_id_col] = feature_ids
    return aligned_feature_df


def _load_metadata(path: Path) -> pd.DataFrame:
    metadata = pd.read_csv(path, sep=",", low_memory=False)
    if METADATA_SAMPLE_ID_COLUMN not in metadata.columns:
        raise KeyError(
            f"META: expected sample ID column {METADATA_SAMPLE_ID_COLUMN!r} in {path.name}; "
            f"found {metadata.columns[:10].tolist()}"
        )

    canonical = _clean_string_series(
        metadata[METADATA_SAMPLE_ID_COLUMN],
        source=f"META {METADATA_SAMPLE_ID_COLUMN}",
    )
    _validate_unique(canonical, source=f"META {METADATA_SAMPLE_ID_COLUMN}")

    metadata = metadata.copy()
    metadata[METADATA_SAMPLE_ID_COLUMN] = canonical
    return metadata


def load_project_data(data_dir: str | Path) -> ProjectData:
    """Load and validate project abundance, metadata, and feature metadata tables."""

    data_dir = Path(data_dir)

    communities: dict[str, pd.DataFrame] = {}
    feature_metadata: dict[str, pd.DataFrame] = {}

    for modality in MODALITIES:
        abundance = _load_abundance_table(data_dir / ABUNDANCE_FILES[modality], modality)
        feature_df = _load_feature_metadata(data_dir / FEATURE_METADATA_FILES[modality], modality)

        if modality == "AMF":
            abundance, feature_df, amf_warning = _apply_amf_unresolved_feature_rule(abundance, feature_df)
            if amf_warning:
                warnings.warn(amf_warning, category=UserWarning, stacklevel=2)

        feature_df = _validate_feature_alignment(modality, abundance, feature_df)

        communities[modality] = abundance
        feature_metadata[modality] = feature_df

    metadata = _load_metadata(data_dir / METADATA_FILE)

    return ProjectData(
        communities=communities,
        metadata=metadata,
        feature_metadata=feature_metadata,
    )


def build_sample_manifest(project_data: ProjectData) -> pd.DataFrame:
    """Build canonical sample membership manifest in metadata order."""

    manifest = pd.DataFrame({
        "sample_id": project_data.metadata[METADATA_SAMPLE_ID_COLUMN].astype(str).tolist()
    })

    for modality in MODALITIES:
        sample_ids = set(project_data.communities[modality].index.astype(str))
        manifest[f"in_{modality}"] = manifest["sample_id"].isin(sample_ids)

    manifest["in_META"] = True
    membership_cols = [f"in_{m}" for m in MODALITIES] + ["in_META"]
    manifest["modalities_present"] = manifest[membership_cols].sum(axis=1)
    return manifest


def select_complete_samples(
    sample_manifest: pd.DataFrame,
    required_modalities: tuple[str, ...],
) -> list[str]:
    """Return sample IDs present in all requested modalities (and META if requested)."""

    required_cols = [f"in_{m}" for m in required_modalities]
    missing_cols = [c for c in required_cols if c not in sample_manifest.columns]
    if missing_cols:
        raise KeyError(f"Manifest missing required membership columns: {missing_cols}")

    mask = sample_manifest[required_cols].all(axis=1)
    return sample_manifest.loc[mask, "sample_id"].astype(str).tolist()
