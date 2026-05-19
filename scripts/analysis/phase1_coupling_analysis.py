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

import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

PLANT_METRICS = ["alpha", "gamma", "dark", "compl", "pool", "compl.perc", "beta", "beta.perc"]
ENV_COVARIATES = [
    "pH_KCl",
    "N_pct",
    "C_pct",
    "P_Mehlich3_mg_100g",
    "K_Mehlich3_mg_100g",
    "hfp.300",
    "bio1now.100",
    "bio12now.100",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase 1 reduced-space multi-kingdom coupling analysis")
    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
    p.add_argument("--amf", default="data/AMF_OTU_table_final.tsv")
    p.add_argument("--bac", default="data/BAC_OTU_table_final.tsv")
    p.add_argument("--euk", default="data/EUK_OTU_table_final.tsv")
    p.add_argument("--its", default="data/ITS_OTU_table_final.tsv")
    p.add_argument("--output-dir", default="results/phase1_coupling")
    p.add_argument("--prevalence-thresholds", nargs="+", type=float, default=[0.05, 0.10])
    p.add_argument("--n-pcs", type=int, default=5)
    p.add_argument("--pseudocount", type=float, default=1e-6)
    p.add_argument("--n-permutations", type=int, default=199)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--max-retries", type=int, default=2, help="Retries for transient long-step failures")
    p.add_argument("--retry-base-seconds", type=float, default=1.0)
    return p.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_checkpoint(outdir: Path, stage: str, payload: dict | None = None) -> None:
    entry = {"timestamp_utc": now_utc(), "stage": stage, "payload": payload or {}}
    ck = outdir / "checkpoints.log"
    with ck.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def write_warnings(outdir: Path, warnings_list: list[str]) -> None:
    deduped = list(dict.fromkeys([w.strip() for w in warnings_list if w and str(w).strip()]))
    lines = [f"[{now_utc()}] {w}" for w in deduped]
    (outdir / "warnings.log").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def append_warning(warnings_list: list[str], msg: str) -> None:
    warnings_list.append(msg)


def with_retry(func, *, desc: str, max_retries: int, base_seconds: float, warnings_list: list[str]):
    last_err = None
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:  # noqa: BLE001
            last_err = e
            if attempt >= max_retries:
                raise
            wait = base_seconds * (2**attempt)
            append_warning(
                warnings_list,
                f"Retrying step '{desc}' after error ({type(e).__name__}: {e}); attempt {attempt+1}/{max_retries}, sleeping {wait:.1f}s",
            )
            time.sleep(wait)
    raise RuntimeError(f"Unreachable retry state for {desc}: {last_err}")


def choose_meta_sample_col(meta: pd.DataFrame) -> str:
    for c in ["canonical", "SampleID_y", "SampleID", "sample_id"]:
        if c in meta.columns:
            return c
    raise ValueError("No metadata sample-id column found (expected canonical or SampleID_y)")


def coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    out = df.apply(pd.to_numeric, errors="coerce").fillna(0.0)
    return out.astype(np.float32)


def read_otu(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t")
    sample_col = df.columns[0]
    df = df.rename(columns={sample_col: "sample_id"})
    df["sample_id"] = df["sample_id"].astype(str)
    numeric = coerce_numeric(df.drop(columns=["sample_id"]))
    out = pd.concat([df[["sample_id"]], numeric], axis=1)
    return out


def overlap_filter(meta: pd.DataFrame, tables: dict[str, pd.DataFrame], sample_col: str) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], list[str]]:
    ids = set(meta[sample_col].astype(str).tolist())
    for t in tables.values():
        ids &= set(t["sample_id"].astype(str).tolist())
    keep = sorted(ids)
    m = meta[meta[sample_col].astype(str).isin(keep)].copy()
    m["sample_id"] = m[sample_col].astype(str)
    m = m.set_index("sample_id").loc[keep].reset_index()
    out = {}
    for k, t in tables.items():
        tt = t[t["sample_id"].astype(str).isin(keep)].copy()
        tt = tt.set_index("sample_id").loc[keep].reset_index()
        out[k] = tt
    return m, out, keep


def prevalence_filter(table: pd.DataFrame, threshold: float) -> tuple[pd.DataFrame, dict[str, int]]:
    x = table.drop(columns=["sample_id"])
    prevalence = (x > 0).mean(axis=0)
    kept_cols = prevalence[prevalence >= threshold].index.tolist()
    if len(kept_cols) == 0:
        kept_cols = prevalence.sort_values(ascending=False).head(1).index.tolist()
    filtered = pd.concat([table[["sample_id"]], x[kept_cols]], axis=1)
    summary = {
        "features_before": int(x.shape[1]),
        "features_after": int(len(kept_cols)),
    }
    return filtered, summary


def relative_abundance(table: pd.DataFrame) -> pd.DataFrame:
    x = table.drop(columns=["sample_id"]).astype(np.float32)
    rs = x.sum(axis=1)
    rs = rs.replace(0, np.nan)
    ra = x.div(rs, axis=0).fillna(0.0)
    return pd.concat([table[["sample_id"]], ra], axis=1)


def clr_transform(table: pd.DataFrame, pseudocount: float) -> pd.DataFrame:
    x = table.drop(columns=["sample_id"]).astype(np.float64)
    x = x + pseudocount
    gm = np.exp(np.log(x).mean(axis=1))
    clr = np.log(x.div(gm, axis=0))
    clr = clr.replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return pd.concat([table[["sample_id"]], clr.astype(np.float32)], axis=1)


def pca_embed(table: pd.DataFrame, n_pcs: int) -> tuple[np.ndarray, np.ndarray]:
    x = table.drop(columns=["sample_id"]).to_numpy(dtype=np.float64)
    if x.shape[1] == 0:
        raise ValueError("No features available for PCA")
    max_pc = max(1, min(n_pcs, x.shape[0] - 1 if x.shape[0] > 1 else 1, x.shape[1]))
    x = StandardScaler(with_mean=True, with_std=True).fit_transform(x)
    pca = PCA(n_components=max_pc, svd_solver="auto", random_state=0)
    emb = pca.fit_transform(x)
    return emb, pca.explained_variance_ratio_


def rv_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    xx = x @ x.T
    yy = y @ y.T
    num = float(np.trace(xx @ yy))
    den = float(np.sqrt(np.trace(xx @ xx) * np.trace(yy @ yy)))
    return num / den if den > 0 else np.nan


def has_repeated_groups(groups: pd.Series | None) -> bool:
    if groups is None:
        return False
    g = groups.dropna().astype(str)
    if g.empty:
        return False
    vc = g.value_counts()
    return bool((vc >= 2).any())


def permute_index(n: int, rng: np.random.Generator, groups: pd.Series | None = None) -> np.ndarray:
    idx = np.arange(n)
    if groups is None:
        rng.shuffle(idx)
        return idx
    g = groups.astype(str).fillna("NA")
    out = idx.copy()
    for grp in g.unique():
        pos = np.where(g.to_numpy() == grp)[0]
        if len(pos) > 1:
            out[pos] = rng.permutation(pos)
    return out


def perm_pvalue(obs: float, null: list[float], two_sided: bool = True) -> float:
    if len(null) == 0 or np.isnan(obs):
        return np.nan
    arr = np.asarray(null)
    if two_sided:
        ge = np.sum(np.abs(arr) >= abs(obs))
    else:
        ge = np.sum(arr >= obs)
    return float((ge + 1) / (len(arr) + 1))


def coupling_metrics(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, n_perm: int, groups: pd.Series | None) -> dict[str, float]:
    _, _, disparity = procrustes(a, b)
    proc_corr = float(1.0 - disparity)

    da = pdist(a, metric="euclidean")
    db = pdist(b, metric="euclidean")
    mantel_r, _ = spearmanr(da, db)
    rv = rv_coefficient(a, b)

    proc_null: list[float] = []
    mantel_null: list[float] = []
    rv_null: list[float] = []
    for _ in range(n_perm):
        idx = permute_index(a.shape[0], rng, groups)
        bp = b[idx, :]
        _, _, disp_p = procrustes(a, bp)
        proc_null.append(1.0 - disp_p)
        dbp = pdist(bp, metric="euclidean")
        r_p, _ = spearmanr(da, dbp)
        mantel_null.append(float(r_p))
        rv_null.append(rv_coefficient(a, bp))

    return {
        "procrustes_corr": proc_corr,
        "procrustes_p_perm": perm_pvalue(proc_corr, proc_null, two_sided=True),
        "mantel_spearman_r": float(mantel_r),
        "mantel_p_perm": perm_pvalue(float(mantel_r), mantel_null, two_sided=True),
        "rv_coeff": float(rv),
        "rv_p_perm": perm_pvalue(float(rv), rv_null, two_sided=True),
    }


def residualize(y: np.ndarray, z: np.ndarray) -> np.ndarray:
    z2 = np.column_stack([np.ones(z.shape[0]), z])
    beta, *_ = np.linalg.lstsq(z2, y, rcond=None)
    return y - z2 @ beta


def assoc_with_permutation(x: np.ndarray, y: np.ndarray, rng: np.random.Generator, n_perm: int, groups: pd.Series | None = None) -> tuple[float, float, float]:
    r, p = spearmanr(x, y)
    null: list[float] = []
    n = len(x)
    for _ in range(n_perm):
        idx = permute_index(n, rng, groups)
        rp, _ = spearmanr(x, y[idx])
        null.append(float(rp))
    return float(r), float(p), perm_pvalue(float(r), null, two_sided=True)


def select_block_column(meta: pd.DataFrame, warnings_list: list[str]) -> str | None:
    for c in ["site.id", "region"]:
        if c in meta.columns and has_repeated_groups(meta[c]):
            return c
    append_warning(warnings_list, "Blocking not possible: no repeated groups in site.id/region. Using unblocked permutations.")
    return None


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

    log_checkpoint(outdir, "start", {"args": vars(args)})

    meta = pd.read_csv(args.metadata)
    sample_col = choose_meta_sample_col(meta)

    tables = {
        "AMF": read_otu(args.amf),
        "BAC": read_otu(args.bac),
        "EUK": read_otu(args.euk),
        "ITS": read_otu(args.its),
    }
    log_checkpoint(outdir, "inputs_loaded", {"sample_col": sample_col})

    meta_ov, tab_ov, keep_ids = overlap_filter(meta, tables, sample_col)
    log_checkpoint(outdir, "overlap_computed", {"full_overlap_n": len(keep_ids)})

    block_col = select_block_column(meta_ov, warnings_list)
    groups = meta_ov[block_col] if block_col else None

    # Save intermediate summary before expensive steps
    (outdir / "intermediate_summary.json").write_text(
        json.dumps(
            {
                "timestamp_utc": now_utc(),
                "full_overlap_n": len(keep_ids),
                "sample_col": sample_col,
                "block_column_candidate": block_col or "none",
                "datasets_n": {
                    "META": int(meta.shape[0]),
                    "AMF": int(tables["AMF"].shape[0]),
                    "BAC": int(tables["BAC"].shape[0]),
                    "EUK": int(tables["EUK"].shape[0]),
                    "ITS": int(tables["ITS"].shape[0]),
                },
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    thresholds = sorted(set([float(t) for t in args.prevalence_thresholds]))
    primary_t = thresholds[0]

    filtering_rows: list[dict] = []
    prevalence_sensitivity_rows: list[dict] = []
    pca_rows: list[dict] = []

    def preprocess_for_threshold(t: float):
        filtered: dict[str, pd.DataFrame] = {}
        clr_tables: dict[str, pd.DataFrame] = {}
        embeddings: dict[str, np.ndarray] = {}
        variances: dict[str, np.ndarray] = {}
        for k, df in tab_ov.items():
            fdf, fs = prevalence_filter(df, t)
            filtering_rows.append({"threshold": t, "kingdom": k, **fs, "n_samples": int(fdf.shape[0])})
            rdf = relative_abundance(fdf)
            cdf = clr_transform(rdf, args.pseudocount)
            emb, var = pca_embed(cdf, args.n_pcs)
            filtered[k] = fdf
            clr_tables[k] = cdf
            embeddings[k] = emb
            variances[k] = var
            for i, v in enumerate(var, start=1):
                pca_rows.append({"threshold": t, "kingdom": k, "pc": i, "variance_explained": float(v)})
        return filtered, clr_tables, embeddings, variances

    _, _, emb_primary, _ = with_retry(
        lambda: preprocess_for_threshold(primary_t),
        desc=f"preprocess threshold {primary_t}",
        max_retries=args.max_retries,
        base_seconds=args.retry_base_seconds,
        warnings_list=warnings_list,
    )
    log_checkpoint(outdir, "primary_preprocess_done", {"threshold": primary_t})

    coupling_rows: list[dict] = []
    for a, b in itertools.combinations(["AMF", "BAC", "EUK", "ITS"], 2):
        metrics = with_retry(
            lambda a=a, b=b: coupling_metrics(emb_primary[a], emb_primary[b], rng, args.n_permutations, groups),
            desc=f"coupling {a}-{b}",
            max_retries=args.max_retries,
            base_seconds=args.retry_base_seconds,
            warnings_list=warnings_list,
        )
        coupling_rows.append(
            {
                "threshold": primary_t,
                "kingdom_a": a,
                "kingdom_b": b,
                **metrics,
                "n_samples": len(keep_ids),
                "block_column": block_col or "none",
            }
        )

    summaries = pd.DataFrame({"sample_id": keep_ids})
    for k, emb in emb_primary.items():
        summaries[f"{k}_PC1"] = emb[:, 0]

    disp_vals = []
    for i in range(len(keep_ids)):
        vecs = [emb_primary[k][i, :] for k in ["AMF", "BAC", "EUK", "ITS"]]
        d = []
        for u, v in itertools.combinations(vecs, 2):
            d.append(float(np.linalg.norm(u - v)))
        disp_vals.append(float(np.mean(d)))
    summaries["cross_kingdom_dispersion"] = disp_vals

    assoc_rows: list[dict] = []
    assoc_df = summaries.merge(meta_ov, on="sample_id", how="left")
    numeric_covars = [c for c in ENV_COVARIATES if c in assoc_df.columns]

    for micro_var in [c for c in summaries.columns if c != "sample_id"]:
        for plant_var in [m for m in PLANT_METRICS if m in assoc_df.columns]:
            d = assoc_df[[micro_var, plant_var] + numeric_covars].copy()
            d = d.dropna(subset=[micro_var, plant_var])
            if len(d) < 8:
                assoc_rows.append(
                    {
                        "microbial_summary": micro_var,
                        "plant_metric": plant_var,
                        "n": int(len(d)),
                        "spearman_r": np.nan,
                        "spearman_p": np.nan,
                        "spearman_perm_p": np.nan,
                        "partial_spearman_r": np.nan,
                        "partial_spearman_perm_p": np.nan,
                        "block_column": block_col or "none",
                        "note": "insufficient_n",
                    }
                )
                continue

            x = d[micro_var].to_numpy(dtype=float)
            y = d[plant_var].to_numpy(dtype=float)

            gsub = None
            if block_col and block_col in assoc_df.columns:
                gsub = assoc_df.loc[d.index, block_col]

            r, p_nominal, p_perm = assoc_with_permutation(x, y, rng, args.n_permutations, gsub)

            partial_r = np.nan
            partial_p_perm = np.nan
            if numeric_covars:
                z = (
                    d[numeric_covars]
                    .apply(pd.to_numeric, errors="coerce")
                    .fillna(d[numeric_covars].mean(numeric_only=True))
                    .to_numpy(dtype=float)
                )
                if z.ndim == 2 and z.shape[1] > 0:
                    xr = residualize(x, z)
                    yr = residualize(y, z)
                    pr, _, pp = assoc_with_permutation(xr, yr, rng, args.n_permutations, gsub)
                    partial_r = pr
                    partial_p_perm = pp

            assoc_rows.append(
                {
                    "microbial_summary": micro_var,
                    "plant_metric": plant_var,
                    "n": int(len(d)),
                    "spearman_r": r,
                    "spearman_p": p_nominal,
                    "spearman_perm_p": p_perm,
                    "partial_spearman_r": partial_r,
                    "partial_spearman_perm_p": partial_p_perm,
                    "block_column": block_col or "none",
                    "note": "",
                }
            )

    for t in thresholds:
        _, _, emb_t, _ = with_retry(
            lambda t=t: preprocess_for_threshold(t),
            desc=f"sensitivity preprocess threshold {t}",
            max_retries=args.max_retries,
            base_seconds=args.retry_base_seconds,
            warnings_list=warnings_list,
        )
        pair_metrics = []
        for a, b in itertools.combinations(["AMF", "BAC", "EUK", "ITS"], 2):
            cm = coupling_metrics(emb_t[a], emb_t[b], rng, max(49, args.n_permutations // 2), groups)
            pair_metrics.append(cm)
        prevalence_sensitivity_rows.append(
            {
                "threshold": t,
                "mean_procrustes_corr": float(np.nanmean([m["procrustes_corr"] for m in pair_metrics])),
                "mean_mantel_r": float(np.nanmean([m["mantel_spearman_r"] for m in pair_metrics])),
                "mean_rv": float(np.nanmean([m["rv_coeff"] for m in pair_metrics])),
                "n_samples": len(keep_ids),
            }
        )

    cohort_rows = [{"dataset": "META", "n_samples": int(meta.shape[0])}]
    for k, df in tables.items():
        cohort_rows.append({"dataset": k, "n_samples": int(df.shape[0])})
    cohort_rows.append({"dataset": "FULL_OVERLAP", "n_samples": int(len(keep_ids))})

    pd.DataFrame(cohort_rows).to_csv(outdir / "cohort_summary.csv", index=False)
    with (outdir / "cohort_summary.json").open("w", encoding="utf-8") as f:
        json.dump({"full_overlap_n": len(keep_ids), "sample_ids": keep_ids}, f, indent=2)

    pd.DataFrame(filtering_rows).drop_duplicates().to_csv(outdir / "filtering_summary.csv", index=False)
    pd.DataFrame(pca_rows).drop_duplicates().to_csv(outdir / "pca_variance_explained.csv", index=False)
    pd.DataFrame(coupling_rows).to_csv(outdir / "kingdom_coupling_metrics.csv", index=False)
    pd.DataFrame(assoc_rows).to_csv(outdir / "plant_associations.csv", index=False)
    pd.DataFrame(prevalence_sensitivity_rows).to_csv(outdir / "prevalence_sensitivity.csv", index=False)

    repo_root = Path(__file__).resolve().parents[2]
    try:
        git_hash = subprocess.check_output(["git", "-C", str(repo_root), "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        git_hash = "unknown"

    inputs = [Path(args.metadata), Path(args.amf), Path(args.bac), Path(args.euk), Path(args.its)]
    run_meta = {
        "timestamp_utc": now_utc(),
        "runtime_seconds": round(time.time() - started, 3),
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "git_commit": git_hash,
        "args": vars(args),
        "block_column_used": block_col or "none",
        "warnings_count": len(list(dict.fromkeys(warnings_list))),
        "input_file_sizes": {p.name: p.stat().st_size for p in inputs},
        "input_file_hashes_sha256": {p.name: file_hash(p) for p in inputs},
    }
    (outdir / "run_metadata.json").write_text(json.dumps(run_meta, indent=2), encoding="utf-8")

    write_warnings(outdir, warnings_list)
    log_checkpoint(outdir, "complete", {"runtime_seconds": run_meta["runtime_seconds"]})


if __name__ == "__main__":
    main()
