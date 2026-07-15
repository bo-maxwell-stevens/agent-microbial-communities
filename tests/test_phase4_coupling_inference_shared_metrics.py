from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd


SCRIPT_PATH = Path("scripts/analysis/phase4_coupling_inference.py")


def _load_phase4_module():
    spec = importlib.util.spec_from_file_location("phase4_coupling_inference", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _fixture_distance_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    idx = pd.Index(["S1", "S2", "S3", "S4"])
    d1 = np.array(
        [
            [0.0, 0.2, 0.7, 0.9],
            [0.2, 0.0, 0.5, 0.6],
            [0.7, 0.5, 0.0, 0.3],
            [0.9, 0.6, 0.3, 0.0],
        ]
    )
    d2 = np.array(
        [
            [0.0, 0.1, 0.8, 0.4],
            [0.1, 0.0, 0.6, 0.5],
            [0.8, 0.6, 0.0, 0.2],
            [0.4, 0.5, 0.2, 0.0],
        ]
    )
    return (
        pd.DataFrame(d1, index=idx, columns=idx),
        pd.DataFrame(d2, index=idx, columns=idx),
    )


def _fixture_embedding_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    idx = pd.Index(["S1", "S2", "S3", "S4"])
    e1 = np.array([[1.0, 0.0], [0.4, 0.2], [0.0, 1.0], [0.9, 0.5]], dtype=float)
    e2 = np.array([[0.8, 0.1], [0.2, 0.5], [0.1, 1.1], [1.0, 0.3]], dtype=float)
    cols = ["axis_1", "axis_2"]
    return (
        pd.DataFrame(e1, index=idx, columns=cols),
        pd.DataFrame(e2, index=idx, columns=cols),
    )


def test_phase4_has_private_array_helpers_and_no_public_local_duplicates() -> None:
    source = SCRIPT_PATH.read_text()
    tree = ast.parse(source)
    fn_names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}

    required_private = {
        "_condense_array",
        "_mantel_spearman_array",
        "_procrustes_disparity_array",
    }
    assert required_private.issubset(fn_names)

    forbidden_public_duplicates = {
        "condensed_upper",
        "spearman_fast",
        "compute_mantel_spearman",
        "compute_procrustes",
    }
    assert forbidden_public_duplicates.isdisjoint(fn_names)


def test_observed_mantel_uses_shared_metric_once_and_loop_uses_private_array_helper(monkeypatch) -> None:
    m = _load_phase4_module()
    d1_df, d2_df = _fixture_distance_frames()

    calls = {"shared": 0, "array": 0}

    def fake_shared(dx: pd.DataFrame, dy: pd.DataFrame) -> float:
        calls["shared"] += 1
        return 0.25

    def fake_spearman_from_condensed(_x: np.ndarray, _y: np.ndarray) -> float:
        calls["array"] += 1
        return 0.1

    monkeypatch.setattr(m, "mantel_spearman", fake_shared)
    monkeypatch.setattr(m, "_spearman_from_condensed", fake_spearman_from_condensed)

    obs, p = m.mantel_permutation_pvalue(
        d1_df,
        d2_df,
        rng=np.random.default_rng(7),
        n_permutations=3,
    )

    assert obs == 0.25
    assert p == 0.25  # (hits=0 + 1)/(3 + 1)
    assert calls["shared"] == 1
    assert calls["array"] == 3


def test_bootstrap_loops_use_private_array_helpers_not_shared_functions(monkeypatch) -> None:
    m = _load_phase4_module()
    idx = pd.Index(["S1", "S2", "S3"])
    distance_df = pd.DataFrame(
        [[0.0, 1.0, 0.2], [1.0, 0.0, 0.3], [0.2, 0.3, 0.0]],
        index=idx,
        columns=idx,
    )
    embedding_df = pd.DataFrame(
        [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]],
        index=idx,
        columns=["axis_1", "axis_2"],
    )

    def fake_prepare(
        _table: pd.DataFrame,
        _threshold: float,
        _branch: str,
        include_labelled: bool = True,
    ):
        out = {
            "distance": distance_df.to_numpy(),
            "embedding": embedding_df.to_numpy(),
            "distance_metric": "euclidean",
            "ordination_method": "pca",
            "n_features": 2,
        }
        if include_labelled:
            out["distance_df"] = distance_df
            out["embedding_df"] = embedding_df
        return out

    def fail_shared_mantel(_dx: pd.DataFrame, _dy: pd.DataFrame) -> float:
        raise AssertionError("shared mantel_spearman must not be called inside bootstrap loop")

    def fail_shared_proc(_ex: pd.DataFrame, _ey: pd.DataFrame) -> float:
        raise AssertionError("shared procrustes_disparity must not be called inside bootstrap loop")

    calls = {"array_mantel": 0, "array_proc": 0}

    def fake_array_mantel(_dx: np.ndarray, _dy: np.ndarray) -> float:
        calls["array_mantel"] += 1
        return 0.11

    def fake_array_proc(_ex: np.ndarray, _ey: np.ndarray) -> float:
        calls["array_proc"] += 1
        return 0.22

    monkeypatch.setattr(m, "prepare_branch_outputs", fake_prepare)
    monkeypatch.setattr(m, "mantel_spearman", fail_shared_mantel)
    monkeypatch.setattr(m, "procrustes_disparity", fail_shared_proc)
    monkeypatch.setattr(m, "_mantel_spearman_array", fake_array_mantel)
    monkeypatch.setattr(m, "_procrustes_disparity_array", fake_array_proc)

    t = pd.DataFrame({"f1": [1.0, 2.0, 3.0]}, index=idx)
    mantel_vals, proc_vals = m.bootstrap_metrics(
        t,
        t,
        threshold=0.05,
        branch="CLR",
        rng=np.random.default_rng(11),
        n_bootstraps=5,
    )

    assert calls["array_mantel"] == 5
    assert calls["array_proc"] == 5
    assert np.all(mantel_vals == 0.11)
    assert np.all(proc_vals == 0.22)


def test_private_array_helpers_match_shared_metrics_on_validated_inputs() -> None:
    m = _load_phase4_module()
    d1_df, d2_df = _fixture_distance_frames()
    e1_df, e2_df = _fixture_embedding_frames()

    shared_mantel = m.mantel_spearman(d1_df, d2_df)
    array_mantel = m._mantel_spearman_array(d1_df.to_numpy(), d2_df.to_numpy())
    assert array_mantel == shared_mantel

    shared_proc = m.procrustes_disparity(e1_df, e2_df)
    array_proc = m._procrustes_disparity_array(e1_df.to_numpy(), e2_df.to_numpy())
    assert array_proc == shared_proc


def test_permutation_enforces_label_order_at_boundary() -> None:
    m = _load_phase4_module()
    idx = pd.Index(["A", "B", "C", "D"])
    d = pd.DataFrame(
        [
            [0.0, 0.2, 0.3, 0.7],
            [0.2, 0.0, 0.4, 0.6],
            [0.3, 0.4, 0.0, 0.5],
            [0.7, 0.6, 0.5, 0.0],
        ],
        index=idx,
        columns=idx,
    )

    perm = ["C", "A", "D", "B"]
    d_perm = d.loc[perm, perm]

    try:
        m.mantel_permutation_pvalue(
            d,
            d_perm,
            rng=np.random.default_rng(5),
            n_permutations=9,
        )
        assert False, "Expected ValueError for mismatched sample ordering"
    except ValueError as exc:
        assert "identical sample ordering" in str(exc)


def test_seed_and_iteration_constants_unchanged() -> None:
    m = _load_phase4_module()
    assert m.RANDOM_SEED == 20260601
    assert m.N_PERMUTATIONS == 999
    assert m.N_BOOTSTRAPS == 120


def test_main_keeps_shared_observed_procrustes_call() -> None:
    source = SCRIPT_PATH.read_text()
    assert "obs_proc = procrustes_disparity(out1[\"embedding_df\"], out2[\"embedding_df\"])" in source
