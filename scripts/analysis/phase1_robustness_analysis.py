#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

KINGDOMS = ["AMF", "BAC", "EUK", "ITS"]
PLANT_METRIC_CANDIDATES = ["compl", "dark_div", "darkdiv", "completeness", "dark"]
ENV_COVARIATES = [
    "pH_KCl",
    "N_pct",
    "C_pct",
    "P_Mehlich3_mg_100g",
    "K_Mehlich3_mg_100g",
    "hfp.300",
    "bio1now.100",
    "bio12now.100",
    "region",
    "PC1",
    "PC2",
    "PC3",
    "PC4",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase-1 robustness and sensitivity analysis for reduced-space kingdom coupling")
    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
    p.add_argument("--amf", default="data/AMF_OTU_table_final.tsv")
    p.add_argument("--bac", default="data/BAC_OTU_table_final.tsv")
    p.add_argument("--euk", default="data/EUK_OTU_table_final.tsv")
    p.add_argument("--its", default="data/ITS_OTU_table_final.tsv")
    p.add_argument("--output-dir", default="results/phase1_robustness")
    p.add_argument("--prevalence-thresholds", nargs="+", type=float, default=[0.01, 0.05, 0.10, 0.20])
    p.add_argument("--n-pcs-options", nargs="+", type=int, default=[5, 10, 20])
    p.add_argument("--n-permutations", type=int, default=199)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--pseudocount", type=float, default=1e-6)
    return p.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_checkpoint(outdir: Path, stage: str, payload: dict | None = None) -> None:
    with (outdir / "checkpoints.log").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"timestamp_utc": now_utc(), "stage": stage, "payload": payload or {}}) + "\n")


def write_warnings(outdir: Path, warning_lines: list[str]) -> None:
    deduped = list(dict.fromkeys([w.strip() for w in warning_lines if str(w).strip()]))
    lines = [f"[{now_utc()}] {w}" for w in deduped]
    (outdir / "warnings.log").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def choose_meta_sample_col(meta: pd.DataFrame) -> str:
    for c in ["canonical", "SampleID_y", "SampleID", "sample_id"]:
        if c in meta.columns:
            return c
    raise ValueError("No metadata sample-id column found (expected one of canonical/SampleID_y/SampleID/sample_id)")


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(pd.to_numeric, errors="coerce").fillna(0.0).astype(np.float32)


def read_otu(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    sample_col = df.columns[0]
    df = df.rename(columns={sample_col: "sample_id"})
    df["sample_id"] = df["sample_id"].astype(str)
    num = coerce_numeric(df.drop(columns=["sample_id"]))
    return pd.concat([df[["sample_id"]], num], axis=1)


def overlap_filter(meta: pd.DataFrame, tables: dict[str, pd.DataFrame], sample_col: str) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], list[str]]:
    keep = set(meta[sample_col].astype(str).tolist())
    for t in tables.values():
        keep &= set(t["sample_id"].astype(str).tolist())
    keep_ids = sorted(keep)

    m = meta[meta[sample_col].astype(str).isin(keep_ids)].copy()
    m["sample_id"] = m[sample_col].astype(str)
    m = m.set_index("sample_id").loc[keep_ids].reset_index()

    out = {}
    for k, t in tables.items():
        tt = t[t["sample_id"].astype(str).isin(keep_ids)].copy()
        tt = tt.set_index("sample_id").loc[keep_ids].reset_index()
        out[k] = tt

    return m, out, keep_ids


def prevalence_filter(table: pd.DataFrame, threshold: float) -> tuple[pd.DataFrame, dict[str, float]]:
    x = table.drop(columns=["sample_id"])
    prev = (x > 0).mean(axis=0)
    keep_cols = prev[prev >= threshold].index.tolist()
    if not keep_cols:
        keep_cols = prev.sort_values(ascending=False).head(1).index.tolist()
    filt = pd.concat([table[["sample_id"]], x[keep_cols]], axis=1)

    row_var = x.var(axis=1, ddof=1).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    filt_var = x[keep_cols].var(axis=1, ddof=1).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    denom = float(row_var.mean())
    retained_var_frac = float((filt_var.mean() / denom) if denom > 0 else np.nan)

    return filt, {
        "features_before": int(x.shape[1]),
        "features_after": int(len(keep_cols)),
        "retained_taxa_fraction": float(len(keep_cols) / x.shape[1]) if x.shape[1] > 0 else np.nan,
        "retained_variance_fraction": retained_var_frac,
    }


def relative_abundance(table: pd.DataFrame) -> pd.DataFrame:
    x = table.drop(columns=["sample_id"]).astype(np.float32)
    rs = x.sum(axis=1).replace(0, np.nan)
    ra = x.div(rs, axis=0).fillna(0.0)
    return pd.concat([table[["sample_id"]], ra], axis=1)


def clr_transform(table: pd.DataFrame, pseudocount: float) -> pd.DataFrame:
    x = table.drop(columns=["sample_id"]).astype(np.float64) + pseudocount
    gm = np.exp(np.log(x).mean(axis=1))
    clr = np.log(x.div(gm, axis=0)).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return pd.concat([table[["sample_id"]], clr.astype(np.float32)], axis=1)


def pca_embed(table: pd.DataFrame, n_pcs: int) -> tuple[np.ndarray, np.ndarray]:
    x = table.drop(columns=["sample_id"]).to_numpy(dtype=np.float64)
    if x.shape[1] == 0:
        raise ValueError("No features after filtering")
    max_pc = max(1, min(n_pcs, x.shape[0] - 1 if x.shape[0] > 1 else 1, x.shape[1]))
    x = StandardScaler(with_mean=True, with_std=True).fit_transform(x)
    pca = PCA(n_components=max_pc, random_state=0)
    emb = pca.fit_transform(x)
    return emb, pca.explained_variance_ratio_


def rv_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    xx = x @ x.T
    yy = y @ y.T
    num = float(np.trace(xx @ yy))
    den = float(np.sqrt(np.trace(xx @ xx) * np.trace(yy @ yy)))
    return num / den if den > 0 else np.nan


def distance_corr_spearman(a: np.ndarray, b: np.ndarray) -> float:
    da = pdist(a, metric="euclidean")
    db = pdist(b, metric="euclidean")
    r, _ = spearmanr(da, db)
    return float(r)


def distance_corr_pearson(a: np.ndarray, b: np.ndarray) -> float:
    da = pdist(a, metric="euclidean")
    db = pdist(b, metric="euclidean")
    r, _ = pearsonr(da, db)
    return float(r)


def random_orthonormal_matrix(k: int, rng: np.random.Generator) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(k, k)))
    return q


def perm_pvalue(obs: float, null_vals: Iterable[float]) -> float:
    arr = np.asarray(list(null_vals), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0 or not np.isfinite(obs):
        return np.nan
    ge = np.sum(np.abs(arr) >= abs(obs))
    return float((ge + 1) / (arr.size + 1))


def null_summary(obs: float, null_vals: list[float]) -> dict[str, float]:
    arr = np.asarray(null_vals, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return {
            "observed": float(obs),
            "null_mean": np.nan,
            "null_sd": np.nan,
            "null_q025": np.nan,
            "null_q975": np.nan,
            "perm_p": np.nan,
        }
    return {
        "observed": float(obs),
        "null_mean": float(np.mean(arr)),
        "null_sd": float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0,
        "null_q025": float(np.quantile(arr, 0.025)),
        "null_q975": float(np.quantile(arr, 0.975)),
        "perm_p": perm_pvalue(float(obs), arr.tolist()),
    }


def coupling_metrics(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    _, _, disparity = procrustes(a, b)
    return {
        "procrustes_corr": float(1.0 - disparity),
        "mantel_spearman_r": distance_corr_spearman(a, b),
        "rv_coeff": rv_coefficient(a, b),
        "embedding_distance_pearson_r": distance_corr_pearson(a, b),
    }


def build_covariate_matrix(df: pd.DataFrame, warning_lines: list[str]) -> tuple[np.ndarray | None, list[str]]:
    available = [c for c in ENV_COVARIATES if c in df.columns]
    if not available:
        return None, []

    blocks: list[pd.DataFrame] = []
    used: list[str] = []

    for c in available:
        s = df[c]
        if pd.api.types.is_numeric_dtype(s):
            num = pd.to_numeric(s, errors="coerce")
            if num.notna().sum() < 8:
                warning_lines.append(f"Skipped covariate {c}: too many missing values")
                continue
            num = num.fillna(num.median())
            blocks.append(pd.DataFrame({c: num.astype(float)}))
            used.append(c)
        else:
            cat = s.astype(str).fillna("NA")
            dummies = pd.get_dummies(cat, prefix=c, drop_first=True, dtype=float)
            if dummies.shape[1] == 0:
                warning_lines.append(f"Skipped covariate {c}: single category after encoding")
                continue
            blocks.append(dummies)
            used.append(c)

    if not blocks:
        return None, []

    z = pd.concat(blocks, axis=1)
    z = z.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return z.to_numpy(dtype=float), used


def residualize(y: np.ndarray, z: np.ndarray) -> np.ndarray:
    z2 = np.column_stack([np.ones(z.shape[0]), z])
    beta, *_ = np.linalg.lstsq(z2, y, rcond=None)
    return y - z2 @ beta


def assoc_perm(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, n_perm: int) -> dict[str, float]:
    r, p = spearmanr(x, y)
    null = []
    for _ in range(n_perm):
        yp = y[rng.permutation(len(y))]
        rp, _ = spearmanr(x, yp)
        null.append(float(rp))
    out = null_summary(float(r), null)
    out.update({"spearman_r": float(r), "spearman_p": float(p)})
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

    warning_lines: list[str] = []
    log_checkpoint(outdir, "start", {"args": vars(args)})

    try:
        meta = pd.read_csv(args.metadata)
    except Exception as e:  # noqa: BLE001
        warning_lines.append(f"metadata parse error: {type(e).__name__}: {e}")
        raise

    sample_col = choose_meta_sample_col(meta)
    tables = {
        "AMF": read_otu(args.amf),
        "BAC": read_otu(args.bac),
        "EUK": read_otu(args.euk),
        "ITS": read_otu(args.its),
    }
    log_checkpoint(outdir, "inputs_loaded", {"sample_col": sample_col})

    meta_ov, tab_ov, keep_ids = overlap_filter(meta, tables, sample_col)
    log_checkpoint(outdir, "overlap_done", {"full_overlap_n": len(keep_ids)})

    thresholds = sorted(set(float(t) for t in args.prevalence_thresholds))
    pcs_options = sorted(set(int(x) for x in args.n_pcs_options))

    prevalence_rows: list[dict] = []
    coupling_rows: list[dict] = []
    env_rows: list[dict] = []
    null_rows: list[dict] = []
    robustness_rows: list[dict] = []
    assoc_rows: list[dict] = []

    available_plant_metrics = [m for m in PLANT_METRIC_CANDIDATES if m in meta_ov.columns]
    if not available_plant_metrics:
        warning_lines.append("No target plant completeness/dark-diversity metric found in metadata")

    for threshold in thresholds:
        filtered: dict[str, pd.DataFrame] = {}
        embeddings_by_pc: dict[int, dict[str, np.ndarray]] = {}

        for k in KINGDOMS:
            fdf, summ = prevalence_filter(tab_ov[k], threshold)
            filtered[k] = fdf
            prevalence_rows.append({
                "threshold": threshold,
                "kingdom": k,
                **summ,
                "n_samples": int(fdf.shape[0]),
            })

        for n_pcs in pcs_options:
            emb: dict[str, np.ndarray] = {}
            var_exp: dict[str, float] = {}

            for k in KINGDOMS:
                ra = relative_abundance(filtered[k])
                clr = clr_transform(ra, args.pseudocount)
                e, v = pca_embed(clr, n_pcs)
                emb[k] = e
                var_exp[k] = float(np.nansum(v))

            embeddings_by_pc[n_pcs] = emb

            # Coupling + null checks for each pair
            pair_metrics = []
            for a, b in itertools.combinations(KINGDOMS, 2):
                obs = coupling_metrics(emb[a], emb[b])

                # shuffle-label null (permute sample alignments in b)
                perm_null = {k: [] for k in obs.keys()}
                rand_align_null = {k: [] for k in obs.keys()}
                for _ in range(args.n_permutations):
                    bp = emb[b][rng.permutation(emb[b].shape[0]), :]
                    m_perm = coupling_metrics(emb[a], bp)
                    for mk, mv in m_perm.items():
                        perm_null[mk].append(float(mv))

                    q = random_orthonormal_matrix(emb[b].shape[1], rng)
                    br = emb[b] @ q
                    m_rot = coupling_metrics(emb[a], br)
                    for mk, mv in m_rot.items():
                        rand_align_null[mk].append(float(mv))

                # environmental adjustment
                pair_df = pd.DataFrame({"sample_id": keep_ids})
                for kk in KINGDOMS:
                    for pc_idx in range(emb[kk].shape[1]):
                        pair_df[f"{kk}_PC{pc_idx+1}"] = emb[kk][:, pc_idx]
                pair_df = pair_df.merge(meta_ov, on="sample_id", how="left")
                z, covars_used = build_covariate_matrix(pair_df, warning_lines)

                if z is not None and z.shape[0] == emb[a].shape[0]:
                    a_res = residualize(emb[a], z)
                    b_res = residualize(emb[b], z)
                    adj = coupling_metrics(a_res, b_res)
                else:
                    adj = {k: np.nan for k in obs.keys()}
                    covars_used = []

                row_base = {
                    "threshold": threshold,
                    "n_pcs": n_pcs,
                    "kingdom_a": a,
                    "kingdom_b": b,
                    "n_samples": len(keep_ids),
                    "covariates_used": "|".join(covars_used) if covars_used else "none",
                }

                c_row = dict(row_base)
                for mk, mv in obs.items():
                    c_row[mk] = mv
                    c_row[f"adj_{mk}"] = float(adj.get(mk, np.nan))
                    c_row[f"delta_{mk}"] = float(adj.get(mk, np.nan) - mv) if np.isfinite(adj.get(mk, np.nan)) else np.nan
                coupling_rows.append(c_row)
                pair_metrics.append(obs)

                for mk, mv in obs.items():
                    pnull = null_summary(mv, perm_null[mk])
                    pnull.update(row_base)
                    pnull["metric"] = mk
                    pnull["null_type"] = "shuffled_labels"
                    null_rows.append(pnull)

                    rnull = null_summary(mv, rand_align_null[mk])
                    rnull.update(row_base)
                    rnull["metric"] = mk
                    rnull["null_type"] = "random_alignment"
                    null_rows.append(rnull)

                # Environmental adjustment summary per pair
                for mk in obs.keys():
                    raw_v = float(obs[mk])
                    adj_v = float(adj.get(mk, np.nan))
                    env_rows.append({
                        **row_base,
                        "metric": mk,
                        "raw_value": raw_v,
                        "adjusted_value": adj_v,
                        "delta": float(adj_v - raw_v) if np.isfinite(adj_v) else np.nan,
                        "attenuation_abs_ratio": float(abs(adj_v) / abs(raw_v)) if np.isfinite(adj_v) and abs(raw_v) > 1e-12 else np.nan,
                    })

            # Association stability with plant gradients
            summary_df = pd.DataFrame({"sample_id": keep_ids})
            for k in KINGDOMS:
                summary_df[f"{k}_PC1"] = emb[k][:, 0]
            disp = []
            for i in range(len(keep_ids)):
                vecs = [emb[k][i, :] for k in KINGDOMS]
                d = [float(np.linalg.norm(u - v)) for u, v in itertools.combinations(vecs, 2)]
                disp.append(float(np.mean(d)))
            summary_df["cross_kingdom_dispersion"] = disp

            adf = summary_df.merge(meta_ov, on="sample_id", how="left")
            z_assoc, assoc_covars_used = build_covariate_matrix(adf, warning_lines)

            for micro in [c for c in summary_df.columns if c != "sample_id"]:
                for plant in available_plant_metrics:
                    d = adf[[micro, plant]].copy().dropna()
                    if len(d) < 10:
                        continue
                    x = d[micro].to_numpy(dtype=float)
                    y = d[plant].to_numpy(dtype=float)
                    ap = assoc_perm(x, y, rng, max(49, args.n_permutations // 2))

                    if z_assoc is not None:
                        z_sub = z_assoc[d.index, :]
                        xr = residualize(x, z_sub)
                        yr = residualize(y, z_sub)
                        ap_adj = assoc_perm(xr, yr, rng, max(49, args.n_permutations // 2))
                    else:
                        ap_adj = {"spearman_r": np.nan, "spearman_p": np.nan, "perm_p": np.nan, "null_mean": np.nan, "null_q025": np.nan, "null_q975": np.nan, "null_sd": np.nan, "observed": np.nan}

                    assoc_rows.append({
                        "threshold": threshold,
                        "n_pcs": n_pcs,
                        "microbial_summary": micro,
                        "plant_metric": plant,
                        "n": int(len(d)),
                        "spearman_r": float(ap["spearman_r"]),
                        "spearman_p": float(ap["spearman_p"]),
                        "perm_p": float(ap["perm_p"]),
                        "adj_spearman_r": float(ap_adj["spearman_r"]) if np.isfinite(ap_adj["spearman_r"]) else np.nan,
                        "adj_perm_p": float(ap_adj["perm_p"]) if np.isfinite(ap_adj["perm_p"]) else np.nan,
                        "covariates_used": "|".join(assoc_covars_used) if assoc_covars_used else "none",
                    })

            robustness_rows.append({
                "threshold": threshold,
                "n_pcs": n_pcs,
                "n_samples": len(keep_ids),
                "mean_procrustes_corr": float(np.nanmean([m["procrustes_corr"] for m in pair_metrics])),
                "mean_mantel_spearman_r": float(np.nanmean([m["mantel_spearman_r"] for m in pair_metrics])),
                "mean_rv_coeff": float(np.nanmean([m["rv_coeff"] for m in pair_metrics])),
                "mean_embedding_distance_pearson_r": float(np.nanmean([m["embedding_distance_pearson_r"] for m in pair_metrics])),
                "mean_variance_explained_across_kingdoms": float(np.nanmean(list(var_exp.values()))),
            })

            log_checkpoint(outdir, "scenario_complete", {
                "threshold": threshold,
                "n_pcs": n_pcs,
                "pairs": 6,
                "assoc_tests": len([r for r in assoc_rows if r["threshold"] == threshold and r["n_pcs"] == n_pcs]),
            })

    # Write required output files
    pd.DataFrame(robustness_rows).to_csv(outdir / "robustness_summary.csv", index=False)
    pd.DataFrame(coupling_rows).to_csv(outdir / "coupling_metric_stability.csv", index=False)
    pd.DataFrame(prevalence_rows).to_csv(outdir / "prevalence_threshold_sensitivity.csv", index=False)
    pd.DataFrame(env_rows).to_csv(outdir / "environmental_adjustment_summary.csv", index=False)
    pd.DataFrame(null_rows).to_csv(outdir / "null_model_results.csv", index=False)

    # optional compact association file for downstream docs (lightweight)
    if assoc_rows:
        pd.DataFrame(assoc_rows).to_csv(outdir / "association_stability.csv", index=False)

    write_warnings(outdir, warning_lines)

    repo_root = Path(__file__).resolve().parents[2]
    try:
        git_hash = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_hash = "unknown"

    input_paths = [Path(args.metadata), Path(args.amf), Path(args.bac), Path(args.euk), Path(args.its)]
    outputs = [
        outdir / "robustness_summary.csv",
        outdir / "coupling_metric_stability.csv",
        outdir / "prevalence_threshold_sensitivity.csv",
        outdir / "environmental_adjustment_summary.csv",
        outdir / "null_model_results.csv",
        outdir / "warnings.log",
        outdir / "checkpoints.log",
    ]

    runtime = {
        "timestamp_utc": now_utc(),
        "runtime_seconds": round(time.time() - started, 3),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "git_commit": git_hash,
        "args": vars(args),
        "full_overlap_n": len(keep_ids),
        "input_file_sizes": {p.name: p.stat().st_size for p in input_paths},
        "input_file_hashes_sha256": {p.name: file_hash(p) for p in input_paths},
        "output_file_sizes": {p.name: p.stat().st_size for p in outputs if p.exists()},
        "warnings_count": len(list(dict.fromkeys(warning_lines))),
        "parse_warnings_or_errors": list(dict.fromkeys(warning_lines)),
    }
    (outdir / "runtime_metadata.json").write_text(json.dumps(runtime, indent=2), encoding="utf-8")
    log_checkpoint(outdir, "complete", {"runtime_seconds": runtime["runtime_seconds"]})


if __name__ == "__main__":
    main()
