#!/usr/bin/env python3
"""Dataset QC v2 workflow for cross-modality microbial datasets.

Outputs:
- Harmonization audit (overlaps, duplicates, missing summaries, canonical inventory)
- Sequencing depth and prevalence QC
- Reproducibility metadata and parse logs

This script never modifies raw data.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


@dataclass(frozen=True)
class ModalitySpec:
    name: str
    abundance_file: str
    sep: str
    feature_metadata_file: Optional[str] = None


ABUNDANCE_MODALITIES: tuple[ModalitySpec, ...] = (
    ModalitySpec("AMF", "AMF_OTU_table_final.tsv", "\t", "AMF_feature_metadata.tsv"),
    ModalitySpec("BAC", "BAC_OTU_table_final.tsv", "\t", "BAC_feature_metadata.tsv"),
    ModalitySpec("EUK", "EUK_OTU_table_final.tsv", "\t", "EUK_feature_metadata.tsv"),
    ModalitySpec("ITS", "ITS_OTU_table_final.tsv", "\t", "ITS_feature_metadata.tsv"),
)

META_MODALITY = "META"
META_FILE = "Final_data_with_diversity_prefixed.csv"
META_SAMPLE_ID_COLUMN = "canonical"
ALL_MODALITIES = [spec.name for spec in ABUNDANCE_MODALITIES] + [META_MODALITY]


@dataclass
class ParseMessage:
    level: str
    modality: str
    file: str
    message: str


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def git_commit_hash(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def normalize_identifier(value: object, label: str) -> str:
    if value is None:
        raise ValueError(f"{label} contains missing value")
    raw = str(value).strip()
    if raw == "" or raw.lower() in {"nan", "none", "na"}:
        raise ValueError(f"{label} contains missing value")
    return raw


def normalize_identifier_index(index: pd.Index, label: str) -> pd.Index:
    cleaned: List[str] = []
    bad_positions: List[int] = []
    for i, value in enumerate(index.tolist(), start=1):
        try:
            cleaned.append(normalize_identifier(value, label))
        except ValueError:
            bad_positions.append(i)
    if bad_positions:
        preview = ", ".join(map(str, bad_positions[:10]))
        raise ValueError(f"{label} has invalid IDs at row positions: {preview}")
    return pd.Index(cleaned)


def collect_duplicate_ids(values: List[str], id_field: str) -> pd.DataFrame:
    counts = pd.Series(values, dtype="string").value_counts(dropna=False)
    dup = counts[counts > 1].sort_index()
    if dup.empty:
        return pd.DataFrame(columns=[id_field, "count"])
    return dup.rename_axis(id_field).reset_index(name="count")


def summarize_series(series: pd.Series) -> Dict[str, object]:
    if series.empty:
        return {
            "n": 0,
            "min": float("nan"),
            "q25": float("nan"),
            "median": float("nan"),
            "mean": float("nan"),
            "q75": float("nan"),
            "max": float("nan"),
        }
    q = series.quantile([0.25, 0.5, 0.75])
    return {
        "n": int(series.shape[0]),
        "min": float(series.min()),
        "q25": float(q.loc[0.25]),
        "median": float(q.loc[0.5]),
        "mean": float(series.mean()),
        "q75": float(q.loc[0.75]),
        "max": float(series.max()),
    }


def compute_prevalence(abundance: pd.DataFrame) -> pd.Series:
    return (abundance > 0).sum(axis=0) / abundance.shape[0]


def _read_csv(path: Path, sep: str, index_col: Optional[int] = None) -> pd.DataFrame:
    try:
        return pd.read_csv(path, sep=sep, index_col=index_col)
    except FileNotFoundError:
        raise
    except (UnicodeDecodeError, pd.errors.ParserError, OSError) as exc:
        raise ValueError(f"Failed to parse {path}: {exc}") from exc


def validate_abundance_matrix(abundance: pd.DataFrame, modality: str, file_label: str) -> None:
    if abundance.shape[1] == 0:
        raise ValueError(f"{modality} {file_label} has no feature columns")

    if abundance.columns.has_duplicates:
        dup = collect_duplicate_ids([str(c) for c in abundance.columns], id_field="taxon_id")
        first = dup.iloc[0]
        raise ValueError(
            f"{modality} {file_label} has duplicate taxon IDs; first duplicate: {first['taxon_id']} (count={int(first['count'])})"
        )

    if abundance.isna().any().any():
        row_idx, col_idx = abundance.isna().to_numpy().nonzero()
        first_row = abundance.index[row_idx[0]]
        first_col = abundance.columns[col_idx[0]]
        raise ValueError(
            f"{modality} {file_label} has missing abundance value at sample_id={first_row}, taxon_id={first_col}"
        )

    nonnumeric_columns = [col for col, dtype in abundance.dtypes.items() if not pd.api.types.is_numeric_dtype(dtype)]
    if nonnumeric_columns:
        examples: List[str] = []
        for col in nonnumeric_columns[:5]:
            coerced = pd.to_numeric(abundance[col], errors="coerce")
            bad = coerced.isna()
            if bad.any():
                sample_id = abundance.index[bad.to_numpy().nonzero()[0][0]]
                value = abundance.loc[sample_id, col]
                examples.append(f"sample_id={sample_id}, taxon_id={col}, value={value!r}")
        details = "; ".join(examples) if examples else f"columns={nonnumeric_columns[:5]}"
        raise ValueError(f"{modality} {file_label} contains nonnumeric abundance values ({details})")

    negative = abundance < 0
    if negative.any().any():
        row_idx, col_idx = negative.to_numpy().nonzero()
        first_row = abundance.index[row_idx[0]]
        first_col = abundance.columns[col_idx[0]]
        first_val = abundance.loc[first_row, first_col]
        raise ValueError(
            f"Negative abundance value detected in {modality} {file_label} at sample_id={first_row}, taxon_id={first_col}, value={first_val}"
        )


def load_main_metadata_samples(path: Path, sample_column: str = META_SAMPLE_ID_COLUMN) -> pd.Index:
    df = _read_csv(path, sep=",")
    if sample_column not in df.columns:
        raise ValueError(
            f"Main metadata file {path} is missing explicit sample-ID column '{sample_column}'"
        )
    cleaned = normalize_identifier_index(pd.Index(df[sample_column].tolist()), label=f"{META_MODALITY} sample-ID column")
    return cleaned


def load_abundance_table(path: Path, sep: str, modality: str) -> pd.DataFrame:
    df = _read_csv(path, sep=sep, index_col=0)
    if df.empty:
        raise ValueError(f"{modality} abundance table is empty: {path}")

    df.index = normalize_identifier_index(df.index, label=f"{modality} abundance sample IDs")
    sample_dups = collect_duplicate_ids(df.index.tolist(), id_field="sample_id")
    if not sample_dups.empty:
        first = sample_dups.iloc[0]
        raise ValueError(
            f"{modality} abundance table has duplicate sample IDs; first duplicate: {first['sample_id']} (count={int(first['count'])})"
        )

    validate_abundance_matrix(df, modality=modality, file_label=path.name)
    return df


def load_feature_metadata_ids(path: Path, modality: str) -> pd.Index:
    df = _read_csv(path, sep="\t")
    if df.empty or df.shape[1] == 0:
        raise ValueError(f"{modality} feature metadata is empty: {path}")
    first_col = df.columns[0]
    ids = normalize_identifier_index(pd.Index(df[first_col].tolist()), label=f"{modality} feature metadata IDs")
    return ids


def compute_modality_qc(modality: str, abundance: pd.DataFrame) -> dict:
    library_sizes = abundance.sum(axis=1)
    richness = (abundance > 0).sum(axis=1)
    prevalence = compute_prevalence(abundance)

    min_depth = max(1000.0, float(library_sizes.quantile(0.01)))
    threshold_rows = [
        {
            "modality": modality,
            "threshold_type": "taxon_prevalence_fraction",
            "threshold_value": thr,
            "retained_taxa": int((prevalence >= thr).sum()),
            "total_taxa": int(prevalence.shape[0]),
        }
        for thr in [0.01, 0.05, 0.1]
    ]
    threshold_rows.append(
        {
            "modality": modality,
            "threshold_type": "sample_library_size_min_reads",
            "threshold_value": float(min_depth),
            "retained_taxa": "",
            "total_taxa": "",
        }
    )

    return {
        "library_sizes": library_sizes,
        "richness": richness,
        "prevalence": prevalence,
        "threshold_rows": threshold_rows,
    }


def compute_pairwise_overlap(sample_sets: Dict[str, set]) -> pd.DataFrame:
    matrix = pd.DataFrame(index=ALL_MODALITIES, columns=ALL_MODALITIES, dtype=int)
    for a in ALL_MODALITIES:
        for b in ALL_MODALITIES:
            matrix.loc[a, b] = len(sample_sets.get(a, set()).intersection(sample_sets.get(b, set())))
    return matrix


def build_sample_harmonization_outputs(sample_sets: Dict[str, set]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    all_samples = sorted(set().union(*sample_sets.values()))

    canonical_rows = [
        {
            "sample_id": sid,
            **{f"in_{mod}": int(sid in sample_sets.get(mod, set())) for mod in ALL_MODALITIES},
        }
        for sid in all_samples
    ]
    canonical_df = pd.DataFrame(canonical_rows)
    if canonical_df.empty:
        canonical_df = pd.DataFrame(columns=["sample_id"] + [f"in_{mod}" for mod in ALL_MODALITIES])
    canonical_df["modalities_present"] = canonical_df[[f"in_{mod}" for mod in ALL_MODALITIES]].sum(axis=1)

    meta_samples = sample_sets.get(META_MODALITY, set())
    summary_rows = []
    detail_rows = []
    for mod in ALL_MODALITIES:
        mod_samples = sample_sets.get(mod, set())
        missing_from_modality = sorted(meta_samples - mod_samples)
        additional_in_modality = sorted(mod_samples - meta_samples)
        summary_rows.append(
            {
                "modality": mod,
                "n_samples_in_modality": len(mod_samples),
                "n_missing_from_modality_vs_meta": len(missing_from_modality),
                "n_additional_in_modality_vs_meta": len(additional_in_modality),
            }
        )
        detail_rows.extend(
            {"modality": mod, "comparison": "missing_from_modality_vs_meta", "sample_id": sid}
            for sid in missing_from_modality
        )
        detail_rows.extend(
            {"modality": mod, "comparison": "additional_in_modality_vs_meta", "sample_id": sid}
            for sid in additional_in_modality
        )

    missing_summary_df = pd.DataFrame(summary_rows)
    missing_detail_df = pd.DataFrame(detail_rows, columns=["modality", "comparison", "sample_id"])

    overlap_df = compute_pairwise_overlap(sample_sets).reset_index().rename(columns={"index": "modality"})
    return overlap_df, canonical_df, missing_summary_df, missing_detail_df


def load_and_validate_inputs(
    data_dir: Path,
    parse_messages: List[ParseMessage],
    file_size_rows: List[dict],
    duplicate_sample_rows: List[dict],
    duplicate_feature_rows: List[dict],
) -> tuple[Dict[str, pd.DataFrame], Dict[str, set], pd.Index]:
    abundance_tables: Dict[str, pd.DataFrame] = {}
    sample_sets: Dict[str, set] = {name: set() for name in ALL_MODALITIES}

    meta_path = data_dir / META_FILE
    if meta_path.exists():
        file_size_rows.append({"modality": META_MODALITY, "file": str(meta_path), "size_bytes": meta_path.stat().st_size})
        try:
            meta_ids = load_main_metadata_samples(meta_path)
            sample_sets[META_MODALITY] = set(meta_ids.tolist())
            dup_meta = collect_duplicate_ids(meta_ids.tolist(), id_field="sample_id")
            if not dup_meta.empty:
                for _, row in dup_meta.iterrows():
                    duplicate_sample_rows.append(
                        {
                            "modality": META_MODALITY,
                            "scope": "within_modality",
                            "sample_id": row["sample_id"],
                            "count": int(row["count"]),
                            "source": "metadata_rows",
                        }
                    )
        except ValueError as exc:
            parse_messages.append(ParseMessage("ERROR", META_MODALITY, str(meta_path), str(exc)))
            meta_ids = pd.Index([], dtype="string")
    else:
        parse_messages.append(ParseMessage("ERROR", META_MODALITY, str(meta_path), "Expected main metadata file missing"))
        meta_ids = pd.Index([], dtype="string")

    for spec in ABUNDANCE_MODALITIES:
        abundance_path = data_dir / spec.abundance_file
        if not abundance_path.exists():
            parse_messages.append(ParseMessage("WARNING", spec.name, str(abundance_path), "Expected file missing"))
            continue

        file_size_rows.append({"modality": spec.name, "file": str(abundance_path), "size_bytes": abundance_path.stat().st_size})
        try:
            abundance = load_abundance_table(abundance_path, sep=spec.sep, modality=spec.name)
        except ValueError as exc:
            parse_messages.append(ParseMessage("ERROR", spec.name, str(abundance_path), str(exc)))
            continue

        abundance_tables[spec.name] = abundance
        sample_sets[spec.name] = set(abundance.index.tolist())

        dup_samples = collect_duplicate_ids(abundance.index.tolist(), id_field="sample_id")
        if not dup_samples.empty:
            for _, row in dup_samples.iterrows():
                duplicate_sample_rows.append(
                    {
                        "modality": spec.name,
                        "scope": "within_modality",
                        "sample_id": row["sample_id"],
                        "count": int(row["count"]),
                        "source": "abundance_rows",
                    }
                )

        dup_taxa = collect_duplicate_ids([str(c) for c in abundance.columns], id_field="taxon_id")
        if not dup_taxa.empty:
            for _, row in dup_taxa.iterrows():
                duplicate_feature_rows.append(
                    {
                        "modality": spec.name,
                        "taxon_id": row["taxon_id"],
                        "count": int(row["count"]),
                        "source": "abundance_columns",
                    }
                )

        if spec.feature_metadata_file:
            feature_path = data_dir / spec.feature_metadata_file
            if feature_path.exists():
                file_size_rows.append({"modality": spec.name, "file": str(feature_path), "size_bytes": feature_path.stat().st_size})
                try:
                    feature_ids = load_feature_metadata_ids(feature_path, modality=spec.name)
                    dup_feature_ids = collect_duplicate_ids(feature_ids.tolist(), id_field="taxon_id")
                    if not dup_feature_ids.empty:
                        for _, row in dup_feature_ids.iterrows():
                            duplicate_feature_rows.append(
                                {
                                    "modality": spec.name,
                                    "taxon_id": row["taxon_id"],
                                    "count": int(row["count"]),
                                    "source": "feature_metadata_rows",
                                }
                            )
                except ValueError as exc:
                    parse_messages.append(ParseMessage("WARNING", spec.name, str(feature_path), str(exc)))
            else:
                parse_messages.append(ParseMessage("WARNING", spec.name, str(feature_path), "Feature metadata file missing"))

    return abundance_tables, sample_sets, meta_ids


def write_outputs(
    results_dir: Path,
    docs_dir: Path,
    repo_root: Path,
    parse_messages: List[ParseMessage],
    file_size_rows: List[dict],
    duplicate_sample_rows: List[dict],
    duplicate_feature_rows: List[dict],
    sample_sets: Dict[str, set],
    abundance_tables: Dict[str, pd.DataFrame],
) -> None:
    overlap_df, canonical_df, missing_summary_df, missing_detail_df = build_sample_harmonization_outputs(sample_sets)

    overlap_df.to_csv(results_dir / "pairwise_overlap_matrix.csv", index=False)
    canonical_df.to_csv(results_dir / "canonical_sample_inventory.csv", index=False)
    missing_summary_df.to_csv(results_dir / "missing_sample_summary.csv", index=False)
    missing_detail_df.to_csv(results_dir / "missing_sample_details.csv", index=False)

    duplicate_sample_df = pd.DataFrame(
        duplicate_sample_rows,
        columns=["modality", "scope", "sample_id", "count", "source"],
    )
    duplicate_sample_df.to_csv(results_dir / "duplicate_sample_detection.csv", index=False)

    duplicate_feature_df = pd.DataFrame(
        duplicate_feature_rows,
        columns=["modality", "taxon_id", "count", "source"],
    )
    duplicate_feature_df.to_csv(results_dir / "duplicate_feature_detection.csv", index=False)

    lib_rows: List[dict] = []
    lib_summary_rows: List[dict] = []
    zero_lib_rows: List[dict] = []
    prevalence_rows: List[dict] = []
    prevalence_summary_rows: List[dict] = []
    threshold_rows: List[dict] = []
    richness_rows: List[dict] = []
    richness_summary_rows: List[dict] = []

    for modality, abundance in abundance_tables.items():
        qc = compute_modality_qc(modality, abundance)
        library_sizes = qc["library_sizes"]
        richness = qc["richness"]
        prevalence = qc["prevalence"]

        lib_rows.extend(
            {"modality": modality, "sample_id": sid, "library_size": float(depth)}
            for sid, depth in library_sizes.items()
        )
        zero_lib_rows.extend(
            {"modality": modality, "sample_id": sid, "library_size": float(depth)}
            for sid, depth in library_sizes.items()
            if float(depth) == 0.0
        )

        lib_summary_rows.append({"modality": modality, **summarize_series(library_sizes)})

        richness_rows.extend(
            {"modality": modality, "sample_id": sid, "richness": int(val)}
            for sid, val in richness.items()
        )
        richness_summary_rows.append({"modality": modality, **summarize_series(richness)})

        prevalence_rows.extend(
            {"modality": modality, "taxon_id": taxon_id, "prevalence_fraction": float(prev)}
            for taxon_id, prev in prevalence.items()
        )
        prevalence_summary_rows.append({"modality": modality, **summarize_series(prevalence)})

        threshold_rows.extend(qc["threshold_rows"])

    pd.DataFrame(lib_rows, columns=["modality", "sample_id", "library_size"]).to_csv(
        results_dir / "library_sizes_per_sample.csv", index=False
    )
    pd.DataFrame(lib_summary_rows, columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"]).to_csv(
        results_dir / "library_size_summary.csv", index=False
    )
    pd.DataFrame(zero_lib_rows, columns=["modality", "sample_id", "library_size"]).to_csv(
        results_dir / "zero_library_samples.csv", index=False
    )

    pd.DataFrame(prevalence_rows, columns=["modality", "taxon_id", "prevalence_fraction"]).to_csv(
        results_dir / "taxon_prevalence_distribution.csv", index=False
    )
    pd.DataFrame(prevalence_summary_rows, columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"]).to_csv(
        results_dir / "taxon_prevalence_summary.csv", index=False
    )
    pd.DataFrame(
        threshold_rows,
        columns=["modality", "threshold_type", "threshold_value", "retained_taxa", "total_taxa"],
    ).to_csv(results_dir / "suggested_filtering_thresholds.csv", index=False)

    pd.DataFrame(richness_rows, columns=["modality", "sample_id", "richness"]).to_csv(
        results_dir / "richness_per_sample.csv", index=False
    )
    pd.DataFrame(richness_summary_rows, columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"]).to_csv(
        results_dir / "richness_summary.csv", index=False
    )

    parse_df = pd.DataFrame([m.__dict__ for m in parse_messages], columns=["level", "modality", "file", "message"])
    parse_df.to_csv(results_dir / "parse_warnings_errors.csv", index=False)

    pd.DataFrame(file_size_rows, columns=["modality", "file", "size_bytes"]).to_csv(
        results_dir / "input_file_sizes.csv", index=False
    )

    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.replace("\n", " "),
        "pandas_version": pd.__version__,
        "platform": platform.platform(),
        "git_commit_hash": git_commit_hash(repo_root),
        "repo_root": str(repo_root),
        "results_dir": str(results_dir),
        "docs_dir": str(docs_dir),
        "n_parse_warnings_or_errors": int(parse_df.shape[0]),
    }
    (results_dir / "reproducibility_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    pd.DataFrame([{"key": k, "value": v} for k, v in metadata.items()]).to_csv(
        results_dir / "reproducibility_metadata.csv", index=False
    )

    n_total_samples = int(canonical_df.shape[0])
    n_zero = int(len(zero_lib_rows))
    n_dups = int(duplicate_sample_df.shape[0])

    lines = [
        "# Dataset QC v2 Report",
        "",
        f"- Generated: {metadata['timestamp_utc']}",
        f"- Git commit: `{metadata['git_commit_hash']}`",
        f"- Python: `{metadata['python_version']}`",
        f"- pandas: `{metadata['pandas_version']}`",
        "",
        "## 1) Sample harmonization audit",
        "",
        f"- Canonical union sample count: **{n_total_samples}**",
        f"- Duplicate sample detection records (within tables): **{n_dups}**",
        "- Pairwise overlap matrix: `results/dataset_qc_v2/pairwise_overlap_matrix.csv`",
        "- Canonical inventory: `results/dataset_qc_v2/canonical_sample_inventory.csv`",
        "- Missing sample summary vs META: `results/dataset_qc_v2/missing_sample_summary.csv`",
        "- Missing sample details vs META: `results/dataset_qc_v2/missing_sample_details.csv`",
        "",
        "## 2) Sequencing depth and prevalence QC",
        "",
        f"- Zero-library sample records: **{n_zero}**",
        "- Library size summaries: `results/dataset_qc_v2/library_size_summary.csv`",
        "- Taxon prevalence distributions: `results/dataset_qc_v2/taxon_prevalence_distribution.csv`",
        "- Suggested filtering thresholds: `results/dataset_qc_v2/suggested_filtering_thresholds.csv`",
        "- Richness summaries: `results/dataset_qc_v2/richness_summary.csv`",
        "",
        "## 3) Reproducibility metadata",
        "",
        "- Reproducibility metadata JSON: `results/dataset_qc_v2/reproducibility_metadata.json`",
        "- Input file sizes: `results/dataset_qc_v2/input_file_sizes.csv`",
        "- Parse warnings/errors: `results/dataset_qc_v2/parse_warnings_errors.csv`",
        "",
    ]

    if parse_df.empty:
        lines.extend(["## Parse diagnostics", "", "No parse warnings or errors detected.", ""])
    else:
        lines.extend(["## Parse diagnostics", "", f"Total warnings/errors: **{parse_df.shape[0]}**", ""])
        for _, row in parse_df.head(25).iterrows():
            lines.append(f"- {row['level']} [{row['modality']}] `{row['file']}` — {row['message']}")
        if parse_df.shape[0] > 25:
            lines.append(f"- ... and {parse_df.shape[0] - 25} more records in CSV")

    (docs_dir / "dataset_qc_v2_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_qc(repo_root: Path, data_dir: Path, results_dir: Path, docs_dir: Path) -> None:
    ensure_dir(results_dir)
    ensure_dir(docs_dir)

    parse_messages: List[ParseMessage] = []
    file_size_rows: List[dict] = []
    duplicate_sample_rows: List[dict] = []
    duplicate_feature_rows: List[dict] = []

    abundance_tables, sample_sets, _meta_ids = load_and_validate_inputs(
        data_dir=data_dir,
        parse_messages=parse_messages,
        file_size_rows=file_size_rows,
        duplicate_sample_rows=duplicate_sample_rows,
        duplicate_feature_rows=duplicate_feature_rows,
    )

    write_outputs(
        results_dir=results_dir,
        docs_dir=docs_dir,
        repo_root=repo_root,
        parse_messages=parse_messages,
        file_size_rows=file_size_rows,
        duplicate_sample_rows=duplicate_sample_rows,
        duplicate_feature_rows=duplicate_feature_rows,
        sample_sets=sample_sets,
        abundance_tables=abundance_tables,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run dataset QC v2 workflow")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--data-dir", default="data", help="Relative path to input data directory")
    parser.add_argument("--results-dir", default="results/dataset_qc_v2", help="Relative output directory for CSV/JSON")
    parser.add_argument("--docs-dir", default="docs", help="Relative docs output directory for markdown report")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    repo_root = Path(args.repo_root).resolve()
    data_dir = (repo_root / args.data_dir).resolve()
    results_dir = (repo_root / args.results_dir).resolve()
    docs_dir = (repo_root / args.docs_dir).resolve()

    run_qc(repo_root=repo_root, data_dir=data_dir, results_dir=results_dir, docs_dir=docs_dir)
    print(f"QC complete. Outputs in {results_dir} and report in {docs_dir / 'dataset_qc_v2_report.md'}")


if __name__ == "__main__":
    main()
