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
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
            ["git", "rev-parse", "HEAD"], cwd=repo_root, stderr=subprocess.STDOUT, text=True
        )
        return out.strip()
    except Exception:
        return "UNKNOWN"


def infer_sample_id_column(df: pd.DataFrame) -> Optional[str]:
    candidates = [
        "sample",
        "sample_id",
        "sampleid",
        "sample.id",
        "sample_name",
        "id",
        "plot_id",
        "plot",
    ]
    lowered = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lowered:
            return lowered[c]

    # fallback: first column if most values are unique and string-like
    if len(df.columns) > 0:
        c0 = df.columns[0]
        s = df[c0].astype(str)
        if s.nunique(dropna=True) >= max(10, int(0.5 * len(s))):
            return c0
    return None


def clean_ids(values: List[str]) -> List[str]:
    out: List[str] = []
    for v in values:
        if v is None:
            continue
        s = str(v).strip()
        if s == "" or s.lower() in {"nan", "none", "na"}:
            continue
        out.append(s)
    return out


def parse_otu_samples(df: pd.DataFrame, modality: str) -> Tuple[List[str], List[str], pd.DataFrame]:
    """Return sample ids, duplicate ids, and numeric abundance matrix (samples x taxa)."""
    if len(df.columns) == 0:
        return [], [], pd.DataFrame()

    sample_ids = clean_ids(df.iloc[:, 0].tolist())

    dup = pd.Index(sample_ids).duplicated(keep=False)
    duplicates = sorted(pd.Index(sample_ids)[dup].unique().tolist())

    abundance = df.iloc[:, 1:].copy() if len(df.columns) > 1 else pd.DataFrame()
    abundance = abundance.apply(pd.to_numeric, errors="coerce").fillna(0)
    if abundance.shape[0] == len(sample_ids):
        abundance.index = sample_ids

    return sample_ids, duplicates, abundance


def parse_metadata_samples(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    sample_col = infer_sample_id_column(df)
    if sample_col is None:
        return [], []
    ids = clean_ids(df[sample_col].tolist())
    dup = pd.Index(ids).duplicated(keep=False)
    duplicates = sorted(pd.Index(ids)[dup].unique().tolist())
    return ids, duplicates


def overlap_matrix(sample_sets: Dict[str, set]) -> pd.DataFrame:
    keys = list(MODALITIES.keys())
    mat = pd.DataFrame(index=keys, columns=keys, data=0)
    for a in keys:
        for b in keys:
            mat.loc[a, b] = len(sample_sets.get(a, set()).intersection(sample_sets.get(b, set())))
    return mat


def safe_to_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def summarize_series(s: pd.Series, prefix: str = "") -> Dict[str, object]:
    if s.empty:
        return {
            f"{prefix}n": 0,
            f"{prefix}min": float("nan"),
            f"{prefix}q25": float("nan"),
            f"{prefix}median": float("nan"),
            f"{prefix}mean": float("nan"),
            f"{prefix}q75": float("nan"),
            f"{prefix}max": float("nan"),
        }
    q = s.quantile([0.25, 0.5, 0.75])
    return {
        f"{prefix}n": int(s.shape[0]),
        f"{prefix}min": float(s.min()),
        f"{prefix}q25": float(q.loc[0.25]),
        f"{prefix}median": float(q.loc[0.5]),
        f"{prefix}mean": float(s.mean()),
        f"{prefix}q75": float(q.loc[0.75]),
        f"{prefix}max": float(s.max()),
    }


def run_qc(repo_root: Path, data_dir: Path, results_dir: Path, docs_dir: Path) -> None:
    ensure_dir(results_dir)
    ensure_dir(docs_dir)

    parse_messages: List[ParseMessage] = []
    sample_sets: Dict[str, set] = {k: set() for k in MODALITIES}
    duplicate_rows: List[dict] = []
    modality_file_sizes: List[dict] = []

    libsize_rows: List[dict] = []
    libsize_summary_rows: List[dict] = []
    zero_lib_rows: List[dict] = []

    prevalence_rows: List[dict] = []
    prevalence_summary_rows: List[dict] = []
    threshold_rows: List[dict] = []

    richness_rows: List[dict] = []
    richness_summary_rows: List[dict] = []

    for modality, spec in MODALITIES.items():
        otu_path = data_dir / spec["otu"]
        sep = spec["sep"]

        if not otu_path.exists():
            parse_messages.append(ParseMessage("WARNING", modality, str(otu_path), "Expected file missing"))
            continue

        modality_file_sizes.append(
            {
                "modality": modality,
                "file": str(otu_path),
                "size_bytes": otu_path.stat().st_size,
            }
        )

        try:
            df = pd.read_csv(otu_path, sep=sep)
        except Exception as exc:
            parse_messages.append(ParseMessage("ERROR", modality, str(otu_path), f"Failed to parse: {exc}"))
            continue

        if df.empty:
            parse_messages.append(ParseMessage("WARNING", modality, str(otu_path), "Parsed file is empty"))
            continue

        if modality == "META":
            meta_ids, dups = parse_metadata_samples(df)
            sample_sets[modality] = set(meta_ids)
            for d in dups:
                duplicate_rows.append(
                    {
                        "modality": modality,
                        "scope": "within_modality",
                        "sample_id": d,
                        "count": int(meta_ids.count(d)),
                        "source": "metadata_rows",
                    }
                )
            continue

        sample_ids, dups, abundance = parse_otu_samples(df, modality)
        sample_sets[modality] = set(sample_ids)

        for d in dups:
            duplicate_rows.append(
                {
                    "modality": modality,
                    "scope": "within_modality",
                    "sample_id": d,
                    "count": int(sample_ids.count(d)),
                    "source": "otu_columns",
                }
            )

        if abundance.empty:
            parse_messages.append(ParseMessage("WARNING", modality, str(otu_path), "No abundance columns detected"))
            continue

        library_sizes = abundance.sum(axis=1)
        richness = (abundance > 0).sum(axis=1)
        prevalence = (abundance > 0).sum(axis=0) / abundance.shape[0]

        for sid, depth in library_sizes.items():
            libsize_rows.append({"modality": modality, "sample_id": sid, "library_size": float(depth)})
            if float(depth) == 0.0:
                zero_lib_rows.append({"modality": modality, "sample_id": sid, "library_size": 0.0})

        lib_stats = summarize_series(library_sizes, prefix="")
        lib_stats["modality"] = modality
        libsize_summary_rows.append(lib_stats)

        for sid, r in richness.items():
            richness_rows.append({"modality": modality, "sample_id": sid, "richness": int(r)})

        rich_stats = summarize_series(richness, prefix="")
        rich_stats["modality"] = modality
        richness_summary_rows.append(rich_stats)

        for i, prev in enumerate(prevalence.tolist(), start=1):
            prevalence_rows.append(
                {"modality": modality, "taxon_index": i, "prevalence_fraction": float(prev)}
            )

        prev_stats = summarize_series(prevalence, prefix="")
        prev_stats["modality"] = modality
        prevalence_summary_rows.append(prev_stats)

        # Suggested thresholds (report candidate prevalences and a data-driven depth suggestion)
        min_depth = max(1000.0, float(library_sizes.quantile(0.01)))
        for thr in [0.01, 0.05, 0.1]:
            retained = int((prevalence >= thr).sum())
            threshold_rows.append(
                {
                    "modality": modality,
                    "threshold_type": "taxon_prevalence_fraction",
                    "threshold_value": thr,
                    "retained_taxa": retained,
                    "total_taxa": int(prevalence.shape[0]),
                }
            )
        threshold_rows.append(
            {
                "modality": modality,
                "threshold_type": "sample_library_size_min_reads",
                "threshold_value": float(min_depth),
                "retained_taxa": "",
                "total_taxa": "",
            }
        )

        # Optional per-modality feature metadata duplicate check
        meta_file = spec.get("meta")
        if meta_file:
            meta_path = data_dir / meta_file
            if meta_path.exists():
                modality_file_sizes.append(
                    {
                        "modality": modality,
                        "file": str(meta_path),
                        "size_bytes": meta_path.stat().st_size,
                    }
                )
                try:
                    mdf = pd.read_csv(meta_path, sep="\t")
                    meta_ids, dups_meta = parse_metadata_samples(mdf)
                    if dups_meta:
                        for d in dups_meta:
                            duplicate_rows.append(
                                {
                                    "modality": modality,
                                    "scope": "within_modality",
                                    "sample_id": d,
                                    "count": int(meta_ids.count(d)),
                                    "source": "feature_metadata_rows",
                                }
                            )
                except Exception as exc:
                    parse_messages.append(
                        ParseMessage("WARNING", modality, str(meta_path), f"Feature metadata parse failed: {exc}")
                    )
            else:
                parse_messages.append(ParseMessage("WARNING", modality, str(meta_path), "Feature metadata file missing"))

    # Harmonization artifacts
    overlap = overlap_matrix(sample_sets)
    overlap_out = overlap.reset_index().rename(columns={"index": "modality"})
    safe_to_csv(overlap_out, results_dir / "pairwise_overlap_matrix.csv")

    all_samples = sorted(set().union(*sample_sets.values()))
    canonical_rows = []
    for sid in all_samples:
        row = {"sample_id": sid}
        for mod in MODALITIES.keys():
            row[f"in_{mod}"] = int(sid in sample_sets.get(mod, set()))
        row["modalities_present"] = int(sum(row[f"in_{m}"] for m in MODALITIES.keys()))
        canonical_rows.append(row)

    canonical_df = pd.DataFrame(
        canonical_rows,
        columns=["sample_id"] + [f"in_{m}" for m in MODALITIES.keys()] + ["modalities_present"],
    )
    safe_to_csv(canonical_df, results_dir / "canonical_sample_inventory.csv")

    missing_rows = []
    for mod in MODALITIES.keys():
        present = sample_sets.get(mod, set())
        missing = sorted(set(all_samples) - set(present))
        missing_rows.append(
            {
                "modality": mod,
                "n_present": len(present),
                "n_missing_from_canonical_union": len(missing),
                "missing_samples": ";".join(missing),
            }
        )
    missing_df = pd.DataFrame(missing_rows)
    safe_to_csv(missing_df, results_dir / "missing_sample_summary.csv")

    # Across-modality duplicate report: samples seen in >1 modality are expected overlap,
    # but we still report counts as audit metadata.
    counts = []
    for sid in all_samples:
        c = sum(1 for m in MODALITIES if sid in sample_sets.get(m, set()))
        if c > 1:
            counts.append({"modality": "ALL", "scope": "across_modalities", "sample_id": sid, "count": c, "source": "cross_presence"})
    duplicate_df = pd.DataFrame(
        duplicate_rows + counts,
        columns=["modality", "scope", "sample_id", "count", "source"],
    )
    safe_to_csv(duplicate_df, results_dir / "duplicate_sample_detection.csv")

    # QC outputs
    safe_to_csv(
        pd.DataFrame(libsize_rows, columns=["modality", "sample_id", "library_size"]),
        results_dir / "library_sizes_per_sample.csv",
    )
    safe_to_csv(
        pd.DataFrame(
            libsize_summary_rows,
            columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"],
        ),
        results_dir / "library_size_summary.csv",
    )
    safe_to_csv(
        pd.DataFrame(zero_lib_rows, columns=["modality", "sample_id", "library_size"]),
        results_dir / "zero_library_samples.csv",
    )

    safe_to_csv(
        pd.DataFrame(prevalence_rows, columns=["modality", "taxon_index", "prevalence_fraction"]),
        results_dir / "taxon_prevalence_distribution.csv",
    )
    safe_to_csv(
        pd.DataFrame(
            prevalence_summary_rows,
            columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"],
        ),
        results_dir / "taxon_prevalence_summary.csv",
    )
    safe_to_csv(
        pd.DataFrame(
            threshold_rows,
            columns=[
                "modality",
                "threshold_type",
                "threshold_value",
                "retained_taxa",
                "total_taxa",
            ],
        ),
        results_dir / "suggested_filtering_thresholds.csv",
    )

    safe_to_csv(
        pd.DataFrame(richness_rows, columns=["modality", "sample_id", "richness"]),
        results_dir / "richness_per_sample.csv",
    )
    safe_to_csv(
        pd.DataFrame(
            richness_summary_rows,
            columns=["modality", "n", "min", "q25", "median", "mean", "q75", "max"],
        ),
        results_dir / "richness_summary.csv",
    )

    parse_df = pd.DataFrame(
        [m.__dict__ for m in parse_messages],
        columns=["level", "modality", "file", "message"],
    )
    safe_to_csv(parse_df, results_dir / "parse_warnings_errors.csv")

    file_sizes_df = pd.DataFrame(modality_file_sizes, columns=["modality", "file", "size_bytes"])
    safe_to_csv(file_sizes_df, results_dir / "input_file_sizes.csv")

    # Reproducibility metadata
    metadata = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.replace("\n", " "),
        "pandas_version": pd.__version__,
        "platform": platform.platform(),
        "git_commit_hash": git_commit_hash(repo_root),
        "repo_root": str(repo_root),
        "data_dir": str(data_dir),
        "results_dir": str(results_dir),
        "docs_dir": str(docs_dir),
        "n_parse_warnings_or_errors": int(parse_df.shape[0]),
    }

    (results_dir / "reproducibility_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    pd.DataFrame([{"key": k, "value": v} for k, v in metadata.items()]).to_csv(
        results_dir / "reproducibility_metadata.csv", index=False
    )

    # Markdown report
    n_total_samples = len(all_samples)
    n_zero = int(pd.DataFrame(zero_lib_rows).shape[0]) if zero_lib_rows else 0
    n_dups = int(duplicate_df.shape[0]) if not duplicate_df.empty else 0

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
        f"- Duplicate detection records: **{n_dups}**",
        "- Pairwise overlap matrix: `results/dataset_qc_v2/pairwise_overlap_matrix.csv`",
        "- Canonical inventory: `results/dataset_qc_v2/canonical_sample_inventory.csv`",
        "- Missing sample summary: `results/dataset_qc_v2/missing_sample_summary.csv`",
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
        lines.extend([
            "## Parse diagnostics",
            "",
            "No parse warnings or errors detected.",
            "",
        ])
    else:
        lines.extend([
            "## Parse diagnostics",
            "",
            f"Total warnings/errors: **{parse_df.shape[0]}**",
            "",
        ])
        for _, row in parse_df.head(25).iterrows():
            lines.append(
                f"- {row['level']} [{row['modality']}] `{row['file']}` — {row['message']}"
            )
        if parse_df.shape[0] > 25:
            lines.append(f"- ... and {parse_df.shape[0] - 25} more records in CSV")

    report_path = docs_dir / "dataset_qc_v2_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



def main() -> None:
    parser = argparse.ArgumentParser(description="Run dataset QC v2 workflow")
    parser.add_argument("--repo-root", default=".", help="Repository root path")
    parser.add_argument("--data-dir", default="data", help="Relative path to input data directory")
    parser.add_argument("--results-dir", default="results/dataset_qc_v2", help="Relative output directory for CSV/JSON")
    parser.add_argument("--docs-dir", default="docs", help="Relative docs output directory for markdown report")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    data_dir = (repo_root / args.data_dir).resolve()
    results_dir = (repo_root / args.results_dir).resolve()
    docs_dir = (repo_root / args.docs_dir).resolve()

    run_qc(repo_root=repo_root, data_dir=data_dir, results_dir=results_dir, docs_dir=docs_dir)
    print(f"QC complete. Outputs in {results_dir} and report in {docs_dir / 'dataset_qc_v2_report.md'}")


if __name__ == "__main__":
    main()
