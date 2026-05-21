from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import pandas as pd


def get_git_commit(repo_root: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=repo_root,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def generate_normalization_plan(
    datasets: Dict,
    cohort_info: Dict,
    output_path: Path,
) -> None:
    lines = []
    lines.append("# Normalization Plan for Phase 1 Ecological Exploration")
    lines.append("")
    lines.append(
        "This document outlines recommended normalization and transformation "
        "strategies for microbial abundance data across the four kingdoms "
        "(AMF, BAC, EUK, ITS)."
    )
    lines.append("")

    lines.append("## Per-Kingdom Summary Statistics")
    lines.append("")
    lines.append(
        "| Kingdom | Samples | OTUs | Read min | Read median | Read max | "
        "Nonzero min | Nonzero median | Nonzero max | Sparsity |"
    )
    lines.append(
        "|---------|---------|------|----------|-------------|----------|"
        "-------------|----------------|-------------|----------|"
    )
    for k in ["AMF", "BAC", "EUK", "ITS"]:
        otu = datasets[k]["otu"]
        total_reads = otu.sum(axis=1)
        nonzero_features = (otu > 0).sum(axis=1)
        sparsity = 1.0 - (otu > 0).sum().sum() / (otu.shape[0] * otu.shape[1])
        lines.append(
            f"| {k} | {otu.shape[0]} | {otu.shape[1]} | "
            f"{int(total_reads.min())} | {int(total_reads.median())} | "
            f"{int(total_reads.max())} | "
            f"{int(nonzero_features.min())} | {int(nonzero_features.median())} | "
            f"{int(nonzero_features.max())} | {sparsity:.4f} |"
        )
    lines.append("")

    lines.append("## General Recommendations")
    lines.append("")
    lines.append(
        "The following recommendations apply uniformly across all four kingdoms. "
        "Adjust prevalence thresholds per kingdom based on sparsity and sample size."
    )
    lines.append("")

    lines.append("### Prevalence Filtering")
    lines.append(
        "- Filter features present in < 5% of samples (recommended minimum)."
    )
    lines.append(
        "- For rare-biosphere analyses, consider a 1% prevalence threshold."
    )
    lines.append(
        "- Remove features with zero counts across all samples."
    )
    lines.append("")

    lines.append("### Compositional / CLR Recommendations")
    lines.append(
        "- Microbial abundance data are compositional in nature. "
        "Apply Centered Log-Ratio (CLR) transformation after replacing zeros "
        "with a multiplicative Bayesian replacement (e.g., cmultRepl in "
        "zCompositions)."
    )
    lines.append(
        "- CLR is recommended prior to ordination (PCA, RDA) and correlation "
        "analysis (e.g., SparCC, Spearman on CLR values)."
    )
    lines.append(
        "- For sparse data, consider a pseudo-count of +1 before log-transform "
        "as a simpler alternative, though CLR is preferable."
    )
    lines.append("")

    lines.append("### Binary (Presence/Absence) Transformation")
    lines.append(
        "- A complementary binary workflow can be run alongside quantitative "
        "analyses to assess robustness of ecological patterns."
    )
    lines.append(
        "- Binarize at threshold > 0 (any positive count = present)."
    )
    lines.append(
        "- Use for: Jaccard dissimilarity, nestedness analysis (beta diversity "
        "partitioning), and incidence-based ordination."
    )
    lines.append("")

    lines.append("### Ordination Recommendations")
    lines.append(
        "- Quantitative: Use CLR-transformed values with PCA or RDA."
    )
    lines.append(
        "- Qualitative: Use Hellinger-transformed values with PCA "
        "(good compromise for sparse data)."
    )
    lines.append(
        "- Beta diversity: Bray-Curtis on rarefied or CLR-transformed data; "
        "Jaccard on binary data."
    )
    lines.append(
        "- Constrained ordination: RDA with environmental predictors "
        "(pH, nutrients, climate) from the metadata table."
    )
    lines.append("")

    lines.append("### Robustness / Sensitivity Analysis Suggestions")
    lines.append(
        "- Compare results across at least two preprocessing pipelines "
        "(e.g., CLR + PCA vs. Hellinger + PCA)."
    )
    lines.append(
        "- Subsampling (rarefaction) to minimum library size; repeat "
        "multiple iterations to assess stability."
    )
    lines.append(
        "- Jackknife / bootstrap resampling of samples to assess "
        "ordination stability."
    )
    lines.append(
        "- Test impact of prevalence filtering thresholds (1%, 5%, 10%) "
        "on downstream results."
    )
    lines.append(
        "- Cross-validate constrained ordination with leave-one-out or "
        "permutation tests."
    )
    lines.append("")

    output_path.write_text("\n".join(lines))


def generate_analysis_plan(
    cohort_info: Dict,
    overlap_df: Optional[pd.DataFrame],
    output_path: Path,
) -> None:
    lines = []
    lines.append("# Analysis Plan for Phase 1 Ecological Exploration")
    lines.append("")
    lines.append(
        "This plan describes the proposed ecological analyses for Phase 1, "
        "using the defined cohort and data derived from all four microbial "
        "kingdoms."
    )
    lines.append("")

    lines.append("## 1. Cohort Summary")
    lines.append("")
    mp_overlap = cohort_info.get("microbial_plus_metadata_overlap", [])
    total = cohort_info.get("total_samples", "N/A")
    lines.append(f"- **Total samples in cohort**: {total}")
    lines.append(
        f"- **Samples with data across all 4 kingdoms + metadata**: {len(mp_overlap)}"
    )
    for k, cov in cohort_info.get("modality_specific_cohorts", {}).items():
        lines.append(
            f"  - {k}: {len(cov['samples_present'])} present, "
            f"{len(cov['samples_missing'])} missing"
        )
    lines.append("")

    if overlap_df is not None:
        lines.append("### Dataset Overlap Summary")
        lines.append("")
        lines.append(f"```")
        lines.append(overlap_df.to_string(index=False))
        lines.append(f"```")
        lines.append("")

    lines.append("## 2. Ecological Questions")
    lines.append("")
    questions = [
        "How do alpha and beta diversity patterns compare across AMF, BAC, "
        "EUK, and ITS communities along the same environmental gradients?",
        "What is the degree of cross-kingdom coupling in community composition?",
        "Do sparsity and prevalence distributions differ systematically by kingdom, "
        "and how does that affect analytical choices?",
        "Which environmental variables (pH, nutrients, climate) best explain "
        "community variation within and across kingdoms?",
        "Are compositional patterns robust to choices of data transformation "
        "and filtering?",
    ]
    for q in questions:
        lines.append(f"- {q}")
    lines.append("")

    lines.append("## 3. Proposed Workflow")
    lines.append("")
    steps = [
        "**(A) Preprocessing & Filtering** — Apply prevalence filtering per kingdom; "
        "evaluate impact of multiple thresholds.",
        "**(B) Normalization** — Apply CLR transformation (with zero-replacement) "
        "for quantitative analyses; binarize for incidence-based analyses.",
        "**(C) Alpha Diversity** — Compare observed richness, Shannon, and "
        "inverse Simpson across kingdoms; associate with environmental gradients.",
        "**(D) Beta Diversity** — Ordination (PCA on CLR, PCoA on BC/Jaccard); "
        "test for differences by region / environmental groups.",
        "**(E) Cross-Kingdom Coupling** — Procrustes analysis, Mantel tests, "
        "and co-correspondence analysis between kingdoms.",
        "**(F) Environmental Drivers** — RDA / db-RDA with forward-selected "
        "environmental predictors; variance partitioning.",
        "**(G) Robustness** — Sensitivity analysis across preprocessing choices; "
        "bootstrap evaluation of ordination stability.",
    ]
    for s in steps:
        lines.append(f"- {s}")
    lines.append("")

    lines.append("## 4. Output Deliverables")
    lines.append("")
    deliverables = [
        "Filtered and normalized OTU tables (one per kingdom).",
        "Alpha diversity comparison tables and figures.",
        "Ordination plots (PCA, PCoA) with environmental vectors.",
        "Cross-kingdom coupling statistics (Procrustes, Mantel).",
        "RDA results with variance partitioning.",
        "Robustness/sensitivity summary report.",
    ]
    for d in deliverables:
        lines.append(f"- {d}")
    lines.append("")

    output_path.write_text("\n".join(lines))


def generate_runtime_metadata(
    datasets: Dict,
    provenance: Dict,
    cohort_info: Dict,
    repo_root: Path,
    output_path: Path,
    argv: Optional[list[str]] = None,
) -> None:
    metadata = {
        "pipeline": "phase1_ecological_exploration",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_commit": get_git_commit(repo_root),
        "python_version": sys.version,
        "platform": platform.platform(),
        "command_line": argv or [],
        "input_provenance": {},
        "cohort_summary": {
            "total_samples": cohort_info.get("total_samples"),
            "all_microbial_overlap": len(
                cohort_info.get("all_microbial_overlap", [])
            ),
            "microbial_plus_metadata_overlap": len(
                cohort_info.get("microbial_plus_metadata_overlap", [])
            ),
        },
    }

    for k, prov in provenance.items():
        metadata["input_provenance"][k] = {
            "otu": {
                "path": prov["otu"]["path"],
                "size_bytes": prov["otu"]["size_bytes"],
                "sha256": prov["otu"]["sha256"],
            },
        }
        if prov["meta"] is not None:
            metadata["input_provenance"][k]["meta"] = {
                "path": prov["meta"]["path"],
                "size_bytes": prov["meta"]["size_bytes"],
                "sha256": prov["meta"]["sha256"],
            }

    output_path.write_text(json.dumps(metadata, indent=2))
