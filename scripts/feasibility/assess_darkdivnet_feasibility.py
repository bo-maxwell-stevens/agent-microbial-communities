#!/usr/bin/env python3
"""Lightweight feasibility and statistical architecture audit for DarkDivNet x multi-kingdom microbiome integration.

Outputs:
- docs/sample_integration_feasibility.md
- docs/sequencing_depth_and_sparsity.md
- docs/analysis_feasibility_matrix.md
- docs/kingdom_decoupling_hypothesis_assessment.md
- docs/recommended_phase1_analysis.md
- lightweight CSV/JSON in results/feasibility/
"""
from __future__ import annotations

import csv
import json
import platform
import subprocess
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
RESULTS = ROOT / "results" / "feasibility"
RESULTS.mkdir(parents=True, exist_ok=True)

KINGDOM_FILES = {
    "AMF": DATA / "AMF_OTU_table_final.tsv",
    "BAC": DATA / "BAC_OTU_table_final.tsv",
    "EUK": DATA / "EUK_OTU_table_final.tsv",
    "ITS": DATA / "ITS_OTU_table_final.tsv",
}
META_FILE = DATA / "Final_data_with_diversity_prefixed.csv"

PREVALENCE_THRESHOLDS = [0.01, 0.02, 0.05, 0.10]
LIBRARY_THRESHOLDS = [0, 500, 1000, 2000, 5000]


def norm_sample_id(s: str) -> str:
    return str(s).strip()


def q(vals, p):
    if len(vals) == 0:
        return float("nan")
    return float(np.quantile(np.asarray(vals, dtype=float), p))


@dataclass
class KingdomMetrics:
    kingdom: str
    n_samples: int
    n_features: int
    sample_ids: list[str]
    duplicates: list[str]
    library_sizes: dict[str, float]
    richness: dict[str, int]
    zero_library_n: int
    zero_library_samples: list[str]
    nonzero_cells: int
    sparsity: float
    prevalence_props: list[float]
    prevalence_quantiles: dict[str, float]
    prevalence_retention: dict[str, int]
    parse_warnings_n: int


def parse_otu_table(path: Path, kingdom: str) -> KingdomMetrics:
    warnings_n = 0
    sample_ids = []
    lib_sizes = {}
    richness = {}

    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader)
        n_features = len(header) - 1
        prevalence = [0] * n_features

        for row in reader:
            if not row:
                continue
            sid = norm_sample_id(row[0])
            sample_ids.append(sid)
            lib = 0.0
            nz = 0
            vals = row[1:]
            if len(vals) != n_features:
                warnings_n += 1
                if len(vals) < n_features:
                    vals = vals + ["0"] * (n_features - len(vals))
                else:
                    vals = vals[:n_features]

            for i, v in enumerate(vals):
                if v == "" or v.lower() == "nan":
                    continue
                if v == "0" or v == "0.0":
                    continue
                try:
                    x = float(v)
                except Exception:
                    warnings_n += 1
                    continue
                if x > 0:
                    prevalence[i] += 1
                    nz += 1
                    lib += x
            lib_sizes[sid] = lib
            richness[sid] = nz

    counts = Counter(sample_ids)
    duplicates = sorted([s for s, c in counts.items() if c > 1])
    n_samples = len(sample_ids)
    zero_samples = sorted([s for s in sample_ids if lib_sizes.get(s, 0.0) <= 0])
    nonzero_cells = int(sum(richness.values()))
    total_cells = n_samples * n_features if n_samples and n_features else 1
    sparsity = 1.0 - (nonzero_cells / total_cells)

    prevalence_props = [(p / n_samples) if n_samples else 0.0 for p in prevalence]
    prevalence_quantiles = {
        "q00": q(prevalence_props, 0.00),
        "q25": q(prevalence_props, 0.25),
        "q50": q(prevalence_props, 0.50),
        "q75": q(prevalence_props, 0.75),
        "q90": q(prevalence_props, 0.90),
        "q95": q(prevalence_props, 0.95),
        "q99": q(prevalence_props, 0.99),
        "q100": q(prevalence_props, 1.00),
    }
    retention = {
        f">={int(t*100)}pct": int(sum(1 for p in prevalence_props if p >= t))
        for t in PREVALENCE_THRESHOLDS
    }

    return KingdomMetrics(
        kingdom=kingdom,
        n_samples=n_samples,
        n_features=n_features,
        sample_ids=sample_ids,
        duplicates=duplicates,
        library_sizes=lib_sizes,
        richness=richness,
        zero_library_n=len(zero_samples),
        zero_library_samples=zero_samples,
        nonzero_cells=nonzero_cells,
        sparsity=sparsity,
        prevalence_props=prevalence_props,
        prevalence_quantiles=prevalence_quantiles,
        prevalence_retention=retention,
        parse_warnings_n=warnings_n,
    )


def pairwise_overlap_table(sample_sets: dict[str, set[str]]):
    names = list(sample_sets.keys())
    rows = []
    for a in names:
        for b in names:
            inter = len(sample_sets[a] & sample_sets[b])
            union = len(sample_sets[a] | sample_sets[b])
            jacc = inter / union if union else float("nan")
            rows.append({"dataset_a": a, "dataset_b": b, "overlap_n": inter, "jaccard": jacc})
    return pd.DataFrame(rows)


def region_structure_permutation_test(meta_presence_df: pd.DataFrame, n_perm: int = 2000, seed: int = 42):
    rng = np.random.default_rng(seed)
    df = meta_presence_df.copy()
    if "region" not in df.columns or df["region"].isna().all():
        return {"available": False}
    work = df.dropna(subset=["region"]).copy()
    if work["region"].nunique() < 2:
        return {"available": False}

    def stat_fn(tmp):
        rates = tmp.groupby("region", dropna=True)["full_overlap"].mean().values
        return float(np.max(rates) - np.min(rates)) if len(rates) else 0.0

    obs = stat_fn(work)
    labels = work["full_overlap"].to_numpy()
    ge = 0
    for _ in range(n_perm):
        shuffled = labels.copy()
        rng.shuffle(shuffled)
        tmp = work.copy()
        tmp["full_overlap"] = shuffled
        s = stat_fn(tmp)
        if s >= obs:
            ge += 1
    p = (ge + 1) / (n_perm + 1)
    return {
        "available": True,
        "observed_max_minus_min_rate": obs,
        "perm_p_value": p,
        "n_perm": n_perm,
    }


def choose_score(n_full_overlap: int, analysis: str) -> str:
    moderate = "Moderate feasibility"
    low = "Low feasibility"
    notrec = "Not recommended"

    mapping = {
        "compositional ordination": moderate if n_full_overlap >= 70 else low,
        "PERMANOVA": moderate if n_full_overlap >= 70 else low,
        "dbRDA": moderate if n_full_overlap >= 70 else low,
        "variation partitioning": low,
        "RF + SHAP": low,
        "multi-kingdom integration": moderate if n_full_overlap >= 80 else low,
        "co-occurrence networks": notrec,
        "latent embeddings": moderate,
        "sparse PCA": moderate,
        "CCA/RDA": low,
        "distance-decay analyses": moderate,
        "beta diversity partitioning": moderate if n_full_overlap >= 70 else low,
        "stochastic vs deterministic assembly metrics": low,
    }
    return mapping[analysis]


def main():
    t0 = datetime.now(timezone.utc)

    meta = pd.read_csv(META_FILE)
    if "canonical" in meta.columns:
        meta["sample_id"] = meta["canonical"].map(norm_sample_id)
    elif "SampleID_y" in meta.columns:
        meta["sample_id"] = meta["SampleID_y"].map(norm_sample_id)
    else:
        raise RuntimeError("No suitable sample-id column found in metadata")

    meta = meta.dropna(subset=["sample_id"]).copy()
    meta_ids = set(meta["sample_id"].tolist())

    km = {k: parse_otu_table(p, k) for k, p in KINGDOM_FILES.items()}

    sample_sets = {"META": meta_ids}
    for k, m in km.items():
        sample_sets[k] = set(m.sample_ids)

    union_ids = sorted(set().union(*sample_sets.values()))
    presence_rows = []
    meta_lookup = meta.set_index("sample_id", drop=False)
    for sid in union_ids:
        row = {
            "sample_id": sid,
            "in_META": sid in sample_sets["META"],
            "in_AMF": sid in sample_sets["AMF"],
            "in_BAC": sid in sample_sets["BAC"],
            "in_EUK": sid in sample_sets["EUK"],
            "in_ITS": sid in sample_sets["ITS"],
        }
        row["n_datasets_present"] = sum(int(row[c]) for c in ["in_META", "in_AMF", "in_BAC", "in_EUK", "in_ITS"])
        row["full_overlap"] = row["n_datasets_present"] == 5
        if sid in meta_lookup.index:
            row["region"] = meta_lookup.loc[sid, "region"] if "region" in meta_lookup.columns else np.nan
            row["site.id"] = meta_lookup.loc[sid, "site.id"] if "site.id" in meta_lookup.columns else np.nan
            row["compl"] = meta_lookup.loc[sid, "compl"] if "compl" in meta_lookup.columns else np.nan
            row["dark"] = meta_lookup.loc[sid, "dark"] if "dark" in meta_lookup.columns else np.nan
            row["compl.perc"] = meta_lookup.loc[sid, "compl.perc"] if "compl.perc" in meta_lookup.columns else np.nan
        else:
            row["region"] = np.nan
            row["site.id"] = np.nan
            row["compl"] = np.nan
            row["dark"] = np.nan
            row["compl.perc"] = np.nan
        presence_rows.append(row)

    presence_df = pd.DataFrame(presence_rows)
    presence_df.to_csv(RESULTS / "sample_presence_matrix.csv", index=False)

    patt = (
        presence_df.assign(pattern=lambda d: d[["in_META", "in_AMF", "in_BAC", "in_EUK", "in_ITS"]].astype(int).astype(str).agg("".join, axis=1))
        .groupby("pattern", as_index=False)
        .agg(n_samples=("sample_id", "count"))
        .sort_values("n_samples", ascending=False)
    )
    patt.to_csv(RESULTS / "missingness_patterns.csv", index=False)

    pair_df = pairwise_overlap_table(sample_sets)
    pair_df.to_csv(RESULTS / "pairwise_overlap_long.csv", index=False)

    pivot_n = pair_df.pivot(index="dataset_a", columns="dataset_b", values="overlap_n")
    pivot_j = pair_df.pivot(index="dataset_a", columns="dataset_b", values="jaccard")
    pivot_n.to_csv(RESULTS / "pairwise_overlap_counts_matrix.csv")
    pivot_j.to_csv(RESULTS / "pairwise_overlap_jaccard_matrix.csv")

    full_overlap = set.intersection(sample_sets["META"], sample_sets["AMF"], sample_sets["BAC"], sample_sets["EUK"], sample_sets["ITS"])

    meta_presence = presence_df[presence_df["in_META"]].copy()
    region_summary = (
        meta_presence.groupby("region", dropna=False)
        .agg(
            n_meta=("sample_id", "count"),
            n_full_overlap=("full_overlap", "sum"),
            pct_full_overlap=("full_overlap", "mean"),
            n_amf=("in_AMF", "sum"),
            n_bac=("in_BAC", "sum"),
            n_euk=("in_EUK", "sum"),
            n_its=("in_ITS", "sum"),
        )
        .reset_index()
        .sort_values("pct_full_overlap", ascending=False)
    )
    region_summary.to_csv(RESULTS / "region_overlap_summary.csv", index=False)

    structure_test = region_structure_permutation_test(meta_presence[["sample_id", "region", "full_overlap"]])

    dup_rows = []
    for k, m in km.items():
        if not m.duplicates:
            dup_rows.append({"dataset": k, "sample_id": "", "dup_count": 0})
        else:
            counts = Counter(m.sample_ids)
            for sid in m.duplicates:
                dup_rows.append({"dataset": k, "sample_id": sid, "dup_count": counts[sid]})
    pd.DataFrame(dup_rows).to_csv(RESULTS / "duplicate_sample_ids.csv", index=False)

    seq_rows = []
    prev_rows = []
    ret_rows = []
    lib_long_rows = []
    richness_rows = []

    for k, m in km.items():
        libs = list(m.library_sizes.values())
        rich = list(m.richness.values())

        seq_rows.append({
            "kingdom": k,
            "n_samples": m.n_samples,
            "n_features": m.n_features,
            "median_library": q(libs, 0.50),
            "q25_library": q(libs, 0.25),
            "q75_library": q(libs, 0.75),
            "q05_library": q(libs, 0.05),
            "q95_library": q(libs, 0.95),
            "zero_library_n": m.zero_library_n,
            "zero_library_pct": m.zero_library_n / m.n_samples if m.n_samples else float("nan"),
            "median_richness": q(rich, 0.50),
            "q25_richness": q(rich, 0.25),
            "q75_richness": q(rich, 0.75),
            "sparsity": m.sparsity,
            "nonzero_cells": m.nonzero_cells,
            "parse_warnings_n": m.parse_warnings_n,
        })

        for sid, lib in m.library_sizes.items():
            lib_long_rows.append({"kingdom": k, "sample_id": sid, "library_size": lib})
            richness_rows.append({"kingdom": k, "sample_id": sid, "richness_nonzero_taxa": m.richness[sid]})

        for qn, qv in m.prevalence_quantiles.items():
            prev_rows.append({"kingdom": k, "quantile": qn, "prevalence_prop": qv})
        for th, cnt in m.prevalence_retention.items():
            ret_rows.append({"kingdom": k, "threshold": th, "retained_features": cnt, "retained_pct": cnt / m.n_features if m.n_features else float("nan")})

    seq_df = pd.DataFrame(seq_rows)
    seq_df.to_csv(RESULTS / "sequencing_qc_by_kingdom.csv", index=False)
    pd.DataFrame(prev_rows).to_csv(RESULTS / "taxon_prevalence_quantiles.csv", index=False)
    pd.DataFrame(ret_rows).to_csv(RESULTS / "prevalence_threshold_retention.csv", index=False)
    pd.DataFrame(lib_long_rows).to_csv(RESULTS / "sample_library_sizes_long.csv", index=False)
    pd.DataFrame(richness_rows).to_csv(RESULTS / "sample_richness_long.csv", index=False)

    filter_rows = []
    for thr in LIBRARY_THRESHOLDS:
        kept = []
        for sid in sorted(full_overlap):
            ok = True
            for k in ["AMF", "BAC", "EUK", "ITS"]:
                if km[k].library_sizes.get(sid, 0.0) < thr:
                    ok = False
                    break
            if ok:
                kept.append(sid)
        filter_rows.append({"library_threshold_all_kingdoms": thr, "n_full_overlap_kept": len(kept)})
    pd.DataFrame(filter_rows).to_csv(RESULTS / "full_overlap_retention_by_library_threshold.csv", index=False)

    analyses = [
        "compositional ordination",
        "PERMANOVA",
        "dbRDA",
        "variation partitioning",
        "RF + SHAP",
        "multi-kingdom integration",
        "co-occurrence networks",
        "latent embeddings",
        "sparse PCA",
        "CCA/RDA",
        "distance-decay analyses",
        "beta diversity partitioning",
        "stochastic vs deterministic assembly metrics",
    ]

    n_full = len(full_overlap)
    a_rows = []
    for a in analyses:
        score = choose_score(n_full, a)
        if a == "co-occurrence networks":
            risk = "High false-positive risk with sparse compositional counts and n about 84 overlap"
            assumptions = "Large n, stable associations, compositional correction"
        elif a in {"RF + SHAP", "CCA/RDA", "variation partitioning", "stochastic vs deterministic assembly metrics"}:
            risk = "High overfitting or unstable estimates under current n/p"
            assumptions = "Requires aggressive feature reduction and strict blocked validation"
        else:
            risk = "Manageable with constrained design and blocked permutation or CV"
            assumptions = "Requires prevalence filtering, compositional transforms, and confounder control"

        a_rows.append({
            "analysis": a,
            "score": score,
            "n_full_overlap_basis": n_full,
            "primary_assumptions": assumptions,
            "primary_risks": risk,
            "publishable_now": score in {"High feasibility", "Moderate feasibility"},
        })

    a_df = pd.DataFrame(a_rows)
    a_df.to_csv(RESULTS / "analysis_feasibility_matrix.csv", index=False)

    try:
        git_hash = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_hash = "unknown"

    run_meta = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "git_commit": git_hash,
        "input_file_sizes": {p.name: p.stat().st_size for p in [META_FILE, *KINGDOM_FILES.values()]},
        "full_overlap_n": n_full,
        "union_n": len(union_ids),
        "meta_n": len(meta_ids),
        "parse_warnings_total": int(sum(m.parse_warnings_n for m in km.values())),
    }
    (RESULTS / "run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    full_ret = pd.DataFrame(filter_rows)
    keep1000 = int(full_ret.loc[full_ret["library_threshold_all_kingdoms"] == 1000, "n_full_overlap_kept"].iloc[0])

    strongest = "Distance-based multi-kingdom coupling analysis on full-overlap cohort with prevalence-filtered CLR-PCA embeddings and blocked permutation tests"
    weakest = "Direct co-occurrence network inference across all kingdoms on current overlap"
    biggest_stat = "n about 84 in full overlap relative to extreme dimensionality especially BAC, creating high overfitting and pseudoreplication risk without dimensionality reduction and blocked validation"
    biggest_eco = "Quantifying whether plant completeness gradients are accompanied by consistent strengthening or weakening of cross-kingdom compositional coupling"

    doc1 = f"""# Sample Integration Feasibility Audit

Generated: {run_meta['timestamp_utc']}  
Git commit: `{git_hash}`

## Key counts
- META samples: {len(sample_sets['META'])}
- AMF samples: {len(sample_sets['AMF'])}
- BAC samples: {len(sample_sets['BAC'])}
- EUK samples: {len(sample_sets['EUK'])}
- ITS samples: {len(sample_sets['ITS'])}
- Union across META+AMF+BAC+EUK+ITS: {len(union_ids)}
- Full-overlap cohort all five: {n_full}

## Pairwise overlap counts
See `results/feasibility/pairwise_overlap_counts_matrix.csv` and `pairwise_overlap_jaccard_matrix.csv`.

## Missingness structure
- Presence matrix: `results/feasibility/sample_presence_matrix.csv`
- Pattern frequencies: `results/feasibility/missingness_patterns.csv`

Most missingness is driven by metadata coverage META having fewer samples than sequencing tables, not by large discordance among AMF/BAC/EUK/ITS, which are largely co-registered.

## Duplicate sample audit
See `results/feasibility/duplicate_sample_ids.csv`.
- Interpretation: duplicates should be treated as technical anomalies requiring de-duplication before inferential modeling.

## Overlap by region and site.id
See `results/feasibility/region_overlap_summary.csv`.

Statistical structure check region-level permutation on full-overlap membership among META samples:
- observed max-minus-min overlap rate across regions: {structure_test.get('observed_max_minus_min_rate', float('nan')):.3f}
- permutation p-value: {structure_test.get('perm_p_value', float('nan')):.4f}
- permutations: {structure_test.get('n_perm', 0)}

Interpretation:
- If p lower than 0.05, overlap loss is region-structured, increasing confounding risk.
- If p at least 0.05, strong structure is not statistically evident, but power is limited.
- `site.id` has about one sample per site, so inferential site-level missingness tests are underpowered.

## Integration strategy assessment
Given overlap geometry and dimensionality:

1. Full-overlap only n={n_full}
   - Pros: cleanest inferential alignment across plant metrics and all kingdoms.
   - Cons: reduced n and power, especially for high-dimensional supervised models.
   - Use for: primary integrative analyses.

2. Pairwise overlap subsets
   - Pros: larger effective n for targeted kingdom-pair questions.
   - Cons: effect-size comparability across pairs is harder.
   - Use for: sensitivity analyses and mechanism probing.

3. Kingdom-specific analyses
   - Pros: maximizes per-kingdom sample and feature signal.
   - Cons: does not directly test cross-kingdom coupling.
   - Use for: supporting analyses and robustness checks.

4. Latent embeddings and hierarchical integration
   - Pros: compresses p much larger than n regime and improves statistical stability.
   - Cons: may reduce direct taxon-level interpretability.
   - Use for: core integrative pipeline under current n.

## Statistical tradeoff conclusion
A defensible architecture is full-overlap for primary cross-kingdom inference plus pairwise and kingdom-specific sensitivity analyses, with aggressive dimensionality reduction and blocked validation to mitigate pseudoreplication and overfitting.
"""
    (DOCS / "sample_integration_feasibility.md").write_text(doc1, encoding="utf-8")

    seq_lines = []
    for _, r in seq_df.sort_values("kingdom").iterrows():
        seq_lines.append(
            f"- **{r['kingdom']}**: n_samples={int(r['n_samples'])}, n_features={int(r['n_features'])}, "
            f"median_library={r['median_library']:.1f}, IQR_library=[{r['q25_library']:.1f}, {r['q75_library']:.1f}], "
            f"zero_library={int(r['zero_library_n'])} ({100*r['zero_library_pct']:.1f}%), "
            f"median_richness={r['median_richness']:.1f}, sparsity={r['sparsity']:.4f}"
        )

    doc2 = f"""# Sequencing Depth and Sparsity Assessment

Generated: {run_meta['timestamp_utc']}  
Git commit: `{git_hash}`

## Per-kingdom library-size and sparsity summaries
{chr(10).join(seq_lines)}

Source tables:
- `results/feasibility/sequencing_qc_by_kingdom.csv`
- `results/feasibility/sample_library_sizes_long.csv`
- `results/feasibility/sample_richness_long.csv`
- `results/feasibility/taxon_prevalence_quantiles.csv`
- `results/feasibility/prevalence_threshold_retention.csv`

## Zero-library and imbalance checks
- Zero-library samples should be excluded before compositional transforms.
- Strong feature and sample imbalance is expected especially BAC and necessitates prevalence filtering and dimensionality reduction.

## Prevalence and suggested thresholds
Threshold retention is in `prevalence_threshold_retention.csv`.

Recommended baseline filter for initial integrative work:
- Per kingdom retain taxa with prevalence at least 5 percent within analysis cohort.
- Sensitivity checks at 2 percent and 10 percent prevalence filters.

Rationale:
- Less than 2 percent retains many near-idiosyncratic features unstable for inference.
- At least 10 percent may over-prune and remove ecologically relevant rare taxa.

## Approximate compositional stability and CLR expectations
- Aitchison geometry is feasible after removing zero-library samples and prevalence-filtering sparse taxa.
- CLR on raw ultra-sparse matrices is unstable due to pseudocount sensitivity.
- Safer route: prevalence-filter then CLR then low-rank representation before integration.

## Dimensionality reduction necessity
Dimensionality reduction is essential for BAC/EUK/ITS and still advisable for AMF, given n about {n_full} for full-overlap analyses.
"""
    (DOCS / "sequencing_depth_and_sparsity.md").write_text(doc2, encoding="utf-8")

    matrix_rows_md = []
    for _, r in a_df.iterrows():
        matrix_rows_md.append(
            f"| {r['analysis']} | {r['score']} | {r['primary_assumptions']} | {r['primary_risks']} | {'Yes' if r['publishable_now'] else 'No'} |"
        )

    doc3 = f"""# Analysis Feasibility Matrix

Generated: {run_meta['timestamp_utc']}  
Git commit: `{git_hash}`

Current basis:
- META n={len(sample_sets['META'])}
- Full-overlap META+AMF+BAC+EUK+ITS n={n_full}
- Feature dimensionality remains extreme especially BAC, requiring strict reduction.

| Analysis class | Feasibility score | Key assumptions | Main risks and reviewer criticism | Publishable now |
|---|---|---|---|---|
{chr(10).join(matrix_rows_md)}

Detailed machine-readable version:
- `results/feasibility/analysis_feasibility_matrix.csv`

## Key risk themes
- Pseudoreplication and confounding must be controlled with blocked designs.
- Compositionality risks are high for raw-count distance or network approaches.
- Overfitting risk is high for supervised models unless reduced to low-dimensional representations with strict validation.

## Decision summary
- Most defensible now: constrained distance-based and reduced-space multivariate analyses.
- Least defensible now: unconstrained taxon-level cross-kingdom network inference on n about {n_full}.
"""
    (DOCS / "analysis_feasibility_matrix.md").write_text(doc3, encoding="utf-8")

    doc4 = f"""# Kingdom-Decoupling Threshold Hypothesis Assessment

Generated: {run_meta['timestamp_utc']}  
Git commit: `{git_hash}`

## Hypothesis under review
As plant communities become less complete higher dark diversity and lower completeness, cross-kingdom microbial coupling weakens and assembly becomes more decoupled or stochastic.

## Ecological plausibility
- Plausible because plant composition and completeness can alter litter chemistry, root exudation, microhabitat filtering, and trophic scaffolding that influence microbial community covariance.
- Plausible directional expectation: lower completeness may weaken deterministic host or environment filtering and increase heterogeneity in microbial composition.

## Novelty and literature alignment
- Conceptually novel in this specific plant dark-diversity framing.
- Aligns with broad literature on plant-soil feedbacks and host filtering, but direct dark-diversity to multi-kingdom coupling tests are limited.

## Testability with current data
- Full integrated cohort n={n_full}.
- This supports moderate-complexity distance-based tests of coupling gradients.
- It does not strongly support high-parameter threshold discovery at taxon level without heavy regularization.

## Alternative explanations and confounders
- Regional structure and unmeasured site processes.
- Soil chemistry and climate covariation with completeness metrics.
- Differential sequencing depth and sparsity artifacts across kingdoms.
- Technical effects if present.

## What evidence would support the hypothesis
1. Coupling metric for kingdom spaces shows reproducible monotonic decline across completeness gradient bins.
2. Signal persists after controlling for region, soil, and climate covariates with blocked permutation.
3. Pattern replicates in sensitivity analyses pairwise kingdom subsets and prevalence thresholds.

## Methodological recommendation
- Prefer distance-based or reduced-space approaches over taxon-level network edges for phase 1.
- Embedding-based integration kingdom-wise CLR plus low-rank axes is safer than direct high-dimensional coupling statistics.

## Critical risk statement
The hypothesis is promising but can become underpowered if framed as precise threshold estimation with many covariates at n about {n_full}. It is more defensible as a gradient and coupling-strength hypothesis in phase 1.
"""
    (DOCS / "kingdom_decoupling_hypothesis_assessment.md").write_text(doc4, encoding="utf-8")

    doc5 = f"""# Recommended Phase 1 Analysis

Generated: {run_meta['timestamp_utc']}  
Git commit: `{git_hash}`

## Recommended pipeline
Distance-based multi-kingdom coupling analysis on full-overlap cohort with prevalence-filtered CLR embeddings and blocked permutation inference.

## Exact samples to use
- Primary cohort: samples present in META+AMF+BAC+EUK+ITS n={n_full}.
- Sensitivity cohort: full-overlap with minimum library threshold at least 1000 reads in all kingdoms n={keep1000}. See `full_overlap_retention_by_library_threshold.csv`.

## Exact kingdoms to include
AMF, BAC, EUK, ITS linked to plant dark-diversity and completeness metrics from META.

## Filtering recommendations
1. Remove zero-library samples per kingdom.
2. Within each kingdom in the analysis cohort, prevalence-filter taxa at least 5 percent with 2 percent and 10 percent sensitivity checks.
3. Optional cap on ultra-low-library samples if instability remains threshold grid already provided.

## Normalization strategy
- Convert counts to compositional representation with conservative pseudocount.
- Apply CLR transform after filtering.
- Standardize reduced components before cross-kingdom integration.

## Dimensionality reduction approach
- Kingdom-wise PCA or sparse PCA on CLR matrix.
- Retain a small fixed number of axes per kingdom for example top 5 to 10, justified by explained variance and stability.

## Validation strategy
- Blocked permutation tests respecting region and site structure where possible.
- Sensitivity analyses over prevalence thresholds and library thresholds.
- Avoid unconstrained feature-level model tuning in phase 1.

## Expected outputs
- Coupling-strength versus completeness gradients effect sizes and permutation p-values.
- Robustness profile across filtering choices.
- Clear decision on whether stronger integrative modeling is justified in phase 2.

## Computational cost
Moderate and feasible on current infrastructure without heavy HPC.

## Expected novelty and manuscript potential
High ecological relevance and publishable if effect directions are consistent and robust under sensitivity checks.

## Key risks
- n about {n_full} remains limiting for complex interaction models.
- Over-interpretation risk if coupling metrics are not robust across filtering settings.

## Why this is the strongest next step
It is biologically meaningful, statistically defensible under current overlap constraints, and provides a decisive feasibility signal before expensive model development.
"""
    (DOCS / "recommended_phase1_analysis.md").write_text(doc5, encoding="utf-8")

    summary = {
        "branch": subprocess.check_output(["git", "-C", str(ROOT), "branch", "--show-current"], text=True).strip(),
        "git_commit_start": git_hash,
        "files_written_docs": [
            "docs/sample_integration_feasibility.md",
            "docs/sequencing_depth_and_sparsity.md",
            "docs/analysis_feasibility_matrix.md",
            "docs/kingdom_decoupling_hypothesis_assessment.md",
            "docs/recommended_phase1_analysis.md",
        ],
        "files_written_results_count": len(list(RESULTS.glob("*"))),
        "strongest_feasible_analysis": strongest,
        "least_defensible_analysis": weakest,
        "biggest_statistical_concern": biggest_stat,
        "biggest_ecological_opportunity": biggest_eco,
        "project_manuscript_feasible_now": True,
    }
    (RESULTS / "completion_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    dt = (datetime.now(timezone.utc) - t0).total_seconds()
    print(json.dumps({"status": "ok", "elapsed_sec": dt, "full_overlap_n": n_full, "union_n": len(union_ids)}, indent=2))


if __name__ == "__main__":
    main()
