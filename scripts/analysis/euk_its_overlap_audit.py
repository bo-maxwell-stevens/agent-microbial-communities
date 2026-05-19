#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


CATEGORIES = ["Fungi", "Metazoa", "Viridiplantae", "Other_Protist_or_Euk", "Unknown/Unclassified"]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Audit EUK-ITS overlap and fungal contribution in EUK signal")
    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
    p.add_argument("--euk-feature-metadata", default="data/EUK_feature_metadata.tsv")
    p.add_argument("--its-feature-metadata", default="data/ITS_feature_metadata.tsv")
    p.add_argument("--euk-table", default="data/EUK_OTU_table_final.tsv")
    p.add_argument("--its-table", default="data/ITS_OTU_table_final.tsv")
    p.add_argument("--output-dir", default="results/euk_its_overlap_audit")
    p.add_argument("--n-pcs", type=int, default=5)
    p.add_argument("--pseudocount", type=float, default=1e-6)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n-permutations", type=int, default=199)
    return p.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_warning(warnings_list: list[str], msg: str) -> None:
    warnings_list.append(msg)


def write_warnings(outdir: Path, warnings_list: list[str]) -> None:
    deduped = list(dict.fromkeys([w.strip() for w in warnings_list if w and str(w).strip()]))
    lines = [f"[{now_utc()}] {w}" for w in deduped]
    (outdir / "warnings.log").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def choose_meta_sample_col(meta: pd.DataFrame) -> str:
    for c in ["canonical", "SampleID_y", "SampleID", "sample_id"]:
        if c in meta.columns:
            return c
    raise ValueError("No metadata sample-id column found")


def read_otu(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    sample_col = df.columns[0]
    df = df.rename(columns={sample_col: "sample_id"})
    df["sample_id"] = df["sample_id"].astype(str)
    num = df.drop(columns=["sample_id"]).apply(pd.to_numeric, errors="coerce").fillna(0.0).astype(np.float32)
    return pd.concat([df[["sample_id"]], num], axis=1)


def classify_taxonomy(raw_tax: str) -> str:
    s = str(raw_tax)
    sl = s.lower()
    if sl.strip() in {"", "nan"}:
        return "Unknown/Unclassified"
    if "unclassified" in sl or "uncultured" in sl or "unknown" in sl:
        return "Unknown/Unclassified"
    if "fungi (kingdom)" in sl or "k__fungi" in sl or "; fungi" in sl or " fungi (" in sl or "f__" in sl and "k__fungi" in sl:
        return "Fungi"
    if "metazoa" in sl or "animalia" in sl:
        return "Metazoa"
    if "viridiplantae" in sl or "streptophyta" in sl or "embryophyta" in sl:
        return "Viridiplantae"
    return "Other_Protist_or_Euk"


def relative_abundance(x: pd.DataFrame) -> pd.DataFrame:
    rs = x.sum(axis=1).replace(0, np.nan)
    return x.div(rs, axis=0).fillna(0.0)


def clr_transform(x: pd.DataFrame, pseudocount: float) -> pd.DataFrame:
    z = x.astype(np.float64) + pseudocount
    gm = np.exp(np.log(z).mean(axis=1))
    clr = np.log(z.div(gm, axis=0)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return clr.astype(np.float32)


def pca_embed(x: pd.DataFrame, n_pcs: int) -> np.ndarray:
    arr = x.to_numpy(dtype=np.float64)
    if arr.shape[1] == 0:
        raise ValueError("No features available for PCA")
    k = max(1, min(n_pcs, arr.shape[1], arr.shape[0] - 1 if arr.shape[0] > 1 else 1))
    arr = StandardScaler(with_mean=True, with_std=True).fit_transform(arr)
    pca = PCA(n_components=k, random_state=0)
    return pca.fit_transform(arr)


def rv_coefficient(a: np.ndarray, b: np.ndarray) -> float:
    aa = a @ a.T
    bb = b @ b.T
    den = float(np.sqrt(np.trace(aa @ aa) * np.trace(bb @ bb)))
    if den <= 0:
        return np.nan
    return float(np.trace(aa @ bb) / den)


def coupling_metrics(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    _, _, disparity = procrustes(a, b)
    da = pdist(a, metric="euclidean")
    db = pdist(b, metric="euclidean")
    mr, _ = spearmanr(da, db)
    pr, _ = pearsonr(da, db)
    return {
        "procrustes_corr": float(1.0 - disparity),
        "mantel_spearman_r": float(mr),
        "rv_coeff": float(rv_coefficient(a, b)),
        "embedding_distance_pearson_r": float(pr),
    }


def perm_pvalue(observed: float, null_values: list[float]) -> float:
    arr = np.asarray(null_values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0 or not np.isfinite(observed):
        return np.nan
    ge = np.sum(np.abs(arr) >= abs(observed))
    return float((ge + 1) / (arr.size + 1))


def coupling_with_permutation(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, n_perm: int) -> dict[str, float]:
    obs = coupling_metrics(a, b)
    nulls: dict[str, list[float]] = {k: [] for k in obs.keys()}
    for _ in range(n_perm):
        bp = b[rng.permutation(b.shape[0]), :]
        m = coupling_metrics(a, bp)
        for k, v in m.items():
            nulls[k].append(float(v))
    out = dict(obs)
    for k in obs.keys():
        out[f"{k}_perm_p"] = perm_pvalue(obs[k], nulls[k])
    return out


def file_hash(path: Path) -> str:
    import hashlib

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    started = time.time()
    args = parse_args()
    rng = np.random.default_rng(args.seed)

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    warnings_list: list[str] = []

    meta = pd.read_csv(args.metadata)
    sample_col = choose_meta_sample_col(meta)

    euk_feat = pd.read_csv(args.euk_feature_metadata, sep="\t")
    its_feat = pd.read_csv(args.its_feature_metadata, sep="\t")

    # Taxonomy field detection
    euk_tax_col = "taxonomy" if "taxonomy" in euk_feat.columns else euk_feat.columns[-1]
    its_tax_col = "taxonomy" if "taxonomy" in its_feat.columns else its_feat.columns[-1]

    if euk_tax_col != "taxonomy":
        append_warning(warnings_list, f"EUK taxonomy column inferred as {euk_tax_col}")
    if its_tax_col != "taxonomy":
        append_warning(warnings_list, f"ITS taxonomy column inferred as {its_tax_col}")

    euk_feat = euk_feat.copy()
    euk_feat["category"] = euk_feat[euk_tax_col].map(classify_taxonomy)

    euk = read_otu(args.euk_table)
    its = read_otu(args.its_table)

    # full-overlap samples
    keep = sorted(set(meta[sample_col].astype(str)) & set(euk["sample_id"].astype(str)) & set(its["sample_id"].astype(str)))
    meta_ov = meta[meta[sample_col].astype(str).isin(keep)].copy()
    meta_ov["sample_id"] = meta_ov[sample_col].astype(str)
    meta_ov = meta_ov.set_index("sample_id").loc[keep].reset_index()

    euk = euk[euk["sample_id"].isin(keep)].copy().set_index("sample_id").loc[keep].reset_index()
    its = its[its["sample_id"].isin(keep)].copy().set_index("sample_id").loc[keep].reset_index()

    euk_feature_ids = [c for c in euk.columns if c != "sample_id"]
    if "OTU" not in euk_feat.columns:
        raise ValueError("EUK feature metadata must include OTU column")

    taxmap = euk_feat[["OTU", "category"]].drop_duplicates().set_index("OTU")["category"].to_dict()

    # Assign missing OTUs in table but not metadata as unknown
    missing_otus = [otu for otu in euk_feature_ids if otu not in taxmap]
    if missing_otus:
        append_warning(warnings_list, f"{len(missing_otus)} EUK OTUs missing from feature metadata; assigned Unknown/Unclassified")
        for otu in missing_otus:
            taxmap[otu] = "Unknown/Unclassified"

    # Feature-level summary
    feature_counts = pd.Series([taxmap.get(otu, "Unknown/Unclassified") for otu in euk_feature_ids]).value_counts()

    # Read-level summary
    euk_num = euk.drop(columns=["sample_id"])
    read_sums = euk_num.sum(axis=0)
    read_by_cat: dict[str, float] = {}
    for otu, reads in read_sums.items():
        cat = taxmap.get(otu, "Unknown/Unclassified")
        read_by_cat[cat] = read_by_cat.get(cat, 0.0) + float(reads)

    total_features = len(euk_feature_ids)
    total_reads = float(euk_num.to_numpy(dtype=float).sum())

    summary_rows = []
    for cat in CATEGORIES:
        fcount = int(feature_counts.get(cat, 0))
        rcount = float(read_by_cat.get(cat, 0.0))
        summary_rows.append(
            {
                "category": cat,
                "feature_count": fcount,
                "feature_fraction": float(fcount / total_features) if total_features > 0 else np.nan,
                "read_count": rcount,
                "read_fraction": float(rcount / total_reads) if total_reads > 0 else np.nan,
                "taxonomy_column_euk": euk_tax_col,
                "taxonomy_column_its": its_tax_col,
                "n_overlap_samples": len(keep),
            }
        )
    tax_summary = pd.DataFrame(summary_rows)
    tax_summary.to_csv(outdir / "euk_taxonomic_summary.csv", index=False)

    fungal_features = [otu for otu in euk_feature_ids if taxmap.get(otu, "Unknown/Unclassified") == "Fungi"]
    nonfungal_features = [otu for otu in euk_feature_ids if taxmap.get(otu, "Unknown/Unclassified") != "Fungi"]

    if not fungal_features:
        append_warning(warnings_list, "No fungal-assigned EUK features detected")

    # Sample-level fungal fraction
    fungal_reads = euk[fungal_features].sum(axis=1) if fungal_features else pd.Series(np.zeros(len(euk)), index=euk.index)
    total_euk_reads = euk.drop(columns=["sample_id"]).sum(axis=1)
    nonfungal_reads = total_euk_reads - fungal_reads

    by_sample = pd.DataFrame(
        {
            "sample_id": euk["sample_id"],
            "euk_total_reads": total_euk_reads.astype(float),
            "euk_fungal_reads": fungal_reads.astype(float),
            "euk_nonfungal_reads": nonfungal_reads.astype(float),
        }
    )
    by_sample["euk_fungal_fraction"] = np.where(by_sample["euk_total_reads"] > 0, by_sample["euk_fungal_reads"] / by_sample["euk_total_reads"], np.nan)

    its_total = its.drop(columns=["sample_id"]).sum(axis=1)
    by_sample["its_total_reads"] = its_total.astype(float).to_numpy()
    by_sample.to_csv(outdir / "euk_fungal_fraction_by_sample.csv", index=False)

    # Coupling analyses
    subset_tables: dict[str, pd.DataFrame] = {
        "EUK_all": euk,
    }
    if len(fungal_features) >= 2:
        subset_tables["EUK_fungal"] = pd.concat([euk[["sample_id"]], euk[fungal_features]], axis=1)
    else:
        append_warning(warnings_list, "Insufficient fungal EUK features for subset coupling")

    if len(nonfungal_features) >= 2:
        subset_tables["EUK_nonfungal"] = pd.concat([euk[["sample_id"]], euk[nonfungal_features]], axis=1)
    else:
        append_warning(warnings_list, "Insufficient nonfungal EUK features for subset coupling")

    its_ra = relative_abundance(its.drop(columns=["sample_id"]))
    its_clr = clr_transform(its_ra, args.pseudocount)
    its_emb = pca_embed(its_clr, args.n_pcs)

    coupling_rows = []
    pc1_values: dict[str, np.ndarray] = {"ITS_PC1": its_emb[:, 0]}

    for subset_name, sdf in subset_tables.items():
        sdf_num = sdf.drop(columns=["sample_id"])
        if sdf_num.shape[1] < 2:
            append_warning(warnings_list, f"Skipping {subset_name}: <2 features")
            continue
        ra = relative_abundance(sdf_num)
        clr = clr_transform(ra, args.pseudocount)
        emb = pca_embed(clr, args.n_pcs)
        pc1_values[f"{subset_name}_PC1"] = emb[:, 0]
        metrics = coupling_with_permutation(emb, its_emb, rng, args.n_permutations)
        coupling_rows.append(
            {
                "row_type": "subset_coupling",
                "subset": subset_name,
                "n_samples": len(keep),
                "n_features_subset": int(sdf_num.shape[1]),
                **metrics,
            }
        )

    # Association checks: fungal fraction vs ITS library and PCA axes
    assoc_targets = {
        "ITS_library_size": by_sample["its_total_reads"].to_numpy(dtype=float),
    }
    assoc_targets.update({k: v.astype(float) for k, v in pc1_values.items()})

    fx = by_sample["euk_fungal_fraction"].to_numpy(dtype=float)
    for name, y in assoc_targets.items():
        mask = np.isfinite(fx) & np.isfinite(y)
        if mask.sum() < 8:
            append_warning(warnings_list, f"Skipping association fungal_fraction vs {name}: insufficient finite n")
            continue
        r, p = spearmanr(fx[mask], y[mask])
        coupling_rows.append(
            {
                "row_type": "association",
                "subset": "EUK_fungal_fraction",
                "n_samples": int(mask.sum()),
                "n_features_subset": np.nan,
                "association_target": name,
                "spearman_r": float(r),
                "spearman_p": float(p),
            }
        )

    pd.DataFrame(coupling_rows).to_csv(outdir / "euk_its_subset_coupling.csv", index=False)

    # metadata
    repo_root = Path(__file__).resolve().parents[2]
    try:
        git_hash = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_hash = "unknown"

    input_paths = [
        Path(args.metadata),
        Path(args.euk_feature_metadata),
        Path(args.its_feature_metadata),
        Path(args.euk_table),
        Path(args.its_table),
    ]
    outputs = [
        outdir / "euk_taxonomic_summary.csv",
        outdir / "euk_fungal_fraction_by_sample.csv",
        outdir / "euk_its_subset_coupling.csv",
        outdir / "warnings.log",
    ]

    run_meta = {
        "timestamp_utc": now_utc(),
        "runtime_seconds": round(time.time() - started, 3),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "git_commit": git_hash,
        "args": vars(args),
        "sample_col": sample_col,
        "n_overlap_samples": len(keep),
        "euk_taxonomy_column": euk_tax_col,
        "its_taxonomy_column": its_tax_col,
        "euk_fungal_feature_count": len(fungal_features),
        "euk_nonfungal_feature_count": len(nonfungal_features),
        "input_file_sizes": {p.name: p.stat().st_size for p in input_paths},
        "input_file_hashes_sha256": {p.name: file_hash(p) for p in input_paths},
        "output_file_sizes": {p.name: p.stat().st_size for p in outputs if p.exists()},
        "warnings_count": len(list(dict.fromkeys(warnings_list))),
        "warnings": list(dict.fromkeys(warnings_list)),
    }

    write_warnings(outdir, warnings_list)
    (outdir / "run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
