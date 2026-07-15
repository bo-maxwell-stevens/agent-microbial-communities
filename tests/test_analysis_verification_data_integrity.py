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


p2 = _load_module("scripts/04_cross_kingdom_coupling.py", "phase2_mod")
p5b = _load_module("scripts/analysis/phase5b_environmental_drivers.py", "phase5b_mod")
p5c = _load_module("scripts/analysis/phase5c_plant_diversity_hypotheses.py", "phase5c_mod")


def test_phase2_align_samples_order_and_missing_guard():
    table = pd.DataFrame(
        {
            "f1": [1, 2, 3],
            "f2": [0, 4, 5],
        },
        index=["S2", "S1", "S3"],
    )
    aligned = p2.align_samples(table, ["S1", "S2", "S3"])
    assert list(aligned.index) == ["S1", "S2", "S3"]

    try:
        p2.align_samples(table, ["S1", "S2", "S4"])
    except ValueError as exc:
        assert "Requested samples are missing from table" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing cohort sample")


def test_prevalence_binary_clr_invariants():
    tbl = pd.DataFrame(
        {
            "f1": [1, 0, 1, 0],
            "f2": [0, 0, 0, 0],
            "f3": [2, 1, 0, 0],
        },
        index=["S1", "S2", "S3", "S4"],
    )
    filtered, _ = p2.filter_prevalence(tbl, threshold=0.5)
    # f2 has 0 prevalence and must be dropped
    assert "f2" not in filtered.columns

    binary = p2.to_presence_absence(filtered)
    vals = set(np.unique(binary.to_numpy()))
    assert vals.issubset({0.0, 1.0})

    with pytest.raises(ValueError, match="zero library size"):
        p2.to_relative_abundance(filtered)

    rel = p2.to_relative_abundance(filtered.loc[["S1", "S2", "S3"]])
    clr = p2.clr_transform(rel)
    assert np.isfinite(clr.to_numpy()).all()


def test_distance_matrices_basic_properties():
    tbl = pd.DataFrame(
        {
            "f1": [1, 0, 1],
            "f2": [0, 1, 1],
            "f3": [1, 1, 0],
        },
        index=["S1", "S2", "S3"],
    )
    b = p2.to_presence_absence(tbl)
    d_j = p2.jaccard_distance(b).to_numpy()
    assert d_j.shape == (3, 3)
    assert np.allclose(d_j, d_j.T, atol=1e-12)
    assert np.allclose(np.diag(d_j), 0.0, atol=1e-12)

    rel = p2.to_relative_abundance(tbl)
    clr = p2.clr_transform(rel)
    d_e = p2.euclidean_distance(clr).to_numpy()
    assert d_e.shape == (3, 3)
    assert np.allclose(d_e, d_e.T, atol=1e-12)
    assert np.allclose(np.diag(d_e), 0.0, atol=1e-12)


def test_mantel_and_procrustes_helper_bounds():
    emb_x = pd.DataFrame([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]], index=["S1", "S2", "S3"])
    emb_y = pd.DataFrame([[0.0, 0.0], [1.0, 0.1], [0.0, 0.9]], index=["S1", "S2", "S3"])
    d_x = p2.euclidean_distance(emb_x).to_numpy()
    d_y = p2.euclidean_distance(emb_y).to_numpy()
    r = p2.compute_mantel_spearman(d_x, d_y)
    assert -1.0 <= r <= 1.0

    disp = p2.compute_procrustes(emb_x, emb_y)
    assert np.isfinite(disp)
    assert disp >= 0.0


def test_permutation_floor_and_adjusted_r2_bounds_phase5b():
    rng = np.random.default_rng(7)
    Y = rng.normal(size=(18, 3))
    X = rng.normal(size=(18, 4))

    p, pseudo_f = p5b.permutation_pvalue(Y, X, n_perm=999, seed=17)
    assert 1.0 / 1000.0 <= p <= 1.0
    assert np.isfinite(pseudo_f)

    r2, adj_r2, pseudo_f2 = p5b.fit_multivariate_r2(Y, X)
    assert np.isfinite(r2)
    assert np.isfinite(adj_r2)
    assert np.isfinite(pseudo_f2)
    assert -1.0 <= adj_r2 <= 1.0


def test_predictor_policy_guards_phase5b_and_phase5c():
    # Forbidden predictor must fail policy checks
    try:
        p5b.validate_predictor_policy(["pH_KCl", "N_pct", "PC1"])
    except ValueError as exc:
        assert "Forbidden predictors" in str(exc)
    else:
        raise AssertionError("Expected p5b policy check to fail for forbidden predictor")

    try:
        p5c.validate_predictor_policy(["pH_KCl", "N_pct", "PC2"], model_scope="primary", model_id="X")
    except ValueError as exc:
        assert "Forbidden predictors" in str(exc)
    else:
        raise AssertionError("Expected p5c policy check to fail for forbidden predictor")


def test_hypothesis_model_mapping_A_to_G():
    models = p5c.HYPOTHESIS_MODELS
    assert set(models.keys()) == {"A", "B", "C", "D", "E", "F", "G"}
    assert models["A"]["hypothesis_name"] == "abiotic_base"
    assert "alpha" in models["B"]["predictors"]
    assert "dark" in models["C"]["predictors"]
    assert "pool" in models["D"]["predictors"]
    assert "compl" in models["E"]["predictors"]


def test_no_duplicate_sample_ids_in_cohort_and_otu_tables():
    cohort = pd.read_csv(REPO_ROOT / "results/phase2_confirmatory_coupling/sample_cohort_used.csv")
    assert cohort["Sample_ID"].astype(str).is_unique

    for domain in ["AMF", "BAC", "EUK", "ITS"]:
        df = pd.read_csv(REPO_ROOT / f"data/{domain}_OTU_table_final.tsv", sep="\t", index_col=0)
        ids = df.index.astype(str)
        assert ids.is_unique, f"Duplicate sample IDs in {domain} OTU table"


def test_forbidden_metadata_columns_absent_from_otu_feature_columns():
    forbidden = {
        "PC1", "PC2", "PC3", "PC4", "beta", "beta.perc", "compl.perc", "gamma",
        "lat", "lon", "alpha", "dark", "pool", "compl", "pH_KCl", "N_pct", "C_pct",
    }
    for domain in ["AMF", "BAC", "EUK", "ITS"]:
        df = pd.read_csv(REPO_ROOT / f"data/{domain}_OTU_table_final.tsv", sep="\t", index_col=0)
        overlap = forbidden.intersection(set(map(str, df.columns)))
        assert not overlap, f"Forbidden metadata-like columns found in {domain} OTU table: {sorted(overlap)}"
