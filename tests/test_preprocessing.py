import numpy as np
import pandas as pd
import pytest

from src.preprocessing import (
    align_samples,
    filter_prevalence,
    to_presence_absence,
    to_relative_abundance,
    hellinger_transform,
    clr_transform,
    bray_curtis_distance,
    jaccard_distance,
    euclidean_distance,
)
from src.phase1_ecological_exploration.diagnostics import compare_ordinations


def test_align_samples_preserves_requested_order():
    table = pd.DataFrame(
        [[1, 2], [3, 4], [5, 6]],
        index=["s1", "s2", "s3"],
        columns=["f1", "f2"],
    )
    out = align_samples(table, ["s3", "s1"])
    assert out.index.tolist() == ["s3", "s1"]
    assert out.columns.tolist() == ["f1", "f2"]


def test_align_samples_missing_requested_samples_raise():
    table = pd.DataFrame([[1]], index=["s1"], columns=["f1"])
    with pytest.raises(ValueError, match="missing"):
        align_samples(table, ["s2"])


def test_duplicate_ids_raise():
    dup_rows = pd.DataFrame([[1], [2]], index=["s1", "s1"], columns=["f1"])
    with pytest.raises(ValueError, match="Duplicate sample IDs"):
        to_presence_absence(dup_rows)

    dup_cols = pd.DataFrame([[1, 2]], index=["s1"], columns=["f1", "f1"])
    with pytest.raises(ValueError, match="Duplicate feature IDs"):
        to_presence_absence(dup_cols)


def test_zero_library_rows_raise():
    table = pd.DataFrame([[0, 0], [1, 1]], index=["s1", "s2"], columns=["f1", "f2"])
    with pytest.raises(ValueError, match="zero library"):
        to_relative_abundance(table)


def test_prevalence_threshold_boundaries_and_exact_retention():
    # 84 samples, threshold 0.01 => ceil(0.84)=1
    i84 = [f"s{i}" for i in range(84)]
    a84 = pd.DataFrame({"keep": [1] + [0] * 83, "drop": [0] * 84}, index=i84)
    f84, info84 = filter_prevalence(a84, 0.01)
    assert info84["min_occurrences"] == 1
    assert f84.columns.tolist() == ["keep"]

    # 120 samples, threshold 0.01 => ceil(1.2)=2
    i120 = [f"s{i}" for i in range(120)]
    a120 = pd.DataFrame(
        {
            "exact": [1, 1] + [0] * 118,
            "below": [1] + [0] * 119,
        },
        index=i120,
    )
    f120, info120 = filter_prevalence(a120, 0.01)
    assert info120["min_occurrences"] == 2
    assert f120.columns.tolist() == ["exact"]


def test_relative_binary_hellinger_values_and_row_sums():
    table = pd.DataFrame(
        [[1, 1, 2], [2, 0, 2]],
        index=["s1", "s2"],
        columns=["f1", "f2", "f3"],
    )
    rel = to_relative_abundance(table)
    assert np.allclose(rel.sum(axis=1).values, np.array([1.0, 1.0]))

    binary = to_presence_absence(table)
    assert binary.loc["s2", "f2"] == 0.0
    assert binary.loc["s1", "f2"] == 1.0

    hell = hellinger_transform(table)
    assert np.allclose(hell.values, np.sqrt(rel.values))


def test_clr_centered_log_property_preserved():
    table = pd.DataFrame(
        [[1, 3, 6], [2, 2, 2]],
        index=["s1", "s2"],
        columns=["f1", "f2", "f3"],
    )
    clr = clr_transform(table, pseudocount=0.5)
    assert clr.index.tolist() == ["s1", "s2"]
    assert clr.columns.tolist() == ["f1", "f2", "f3"]
    assert np.allclose(clr.mean(axis=1).values, np.array([0.0, 0.0]), atol=1e-12)


def test_distance_known_examples_and_labels():
    bray_input = pd.DataFrame([[1, 1], [1, 3]], index=["a", "b"], columns=["x", "y"])
    bray = bray_curtis_distance(bray_input)
    assert bray.index.tolist() == ["a", "b"]
    assert bray.columns.tolist() == ["a", "b"]
    assert bray.loc["a", "b"] == pytest.approx(2 / 6)

    jac_input = pd.DataFrame([[1, 0, 1], [1, 1, 0]], index=["a", "b"], columns=["x", "y", "z"])
    jac = jaccard_distance(jac_input)
    assert jac.loc["a", "b"] == pytest.approx(2 / 3)

    euc_input = pd.DataFrame([[0, 0], [3, 4]], index=["a", "b"], columns=["x", "y"])
    euc = euclidean_distance(euc_input)
    assert euc.loc["a", "b"] == pytest.approx(5.0)


def _fake_ordination_results():
    idx = [f"s{i}" for i in range(8)]
    coords_a = pd.DataFrame(
        np.array([[i, i % 3, i % 2] for i in range(8)], dtype=float),
        index=idx,
        columns=["PC1", "PC2", "PC3"],
    )
    coords_b = pd.DataFrame(
        np.array([[7 - i, (i + 1) % 3, (i + 2) % 2] for i in range(8)], dtype=float),
        index=idx,
        columns=["PC1", "PC2", "PC3"],
    )
    return {
        "jaccard_pcoa": {"coordinates": coords_a, "success": True},
        "bray_curtis_pcoa": {"coordinates": coords_b, "success": True},
    }


def test_diagnostics_deterministic_with_same_seed():
    results = _fake_ordination_results()
    d1 = compare_ordinations(results, use_permutation_test=True, random_state=42, n_permutations=50)
    d2 = compare_ordinations(results, use_permutation_test=True, random_state=42, n_permutations=50)
    assert d1 == d2


def test_diagnostics_change_with_different_seed():
    results = _fake_ordination_results()
    d1 = compare_ordinations(results, use_permutation_test=True, random_state=42, n_permutations=200)
    d2 = compare_ordinations(results, use_permutation_test=True, random_state=99, n_permutations=200)
    assert (
        d1[0]["p_value"],
        d1[0].get("null_disparity_mean"),
        d1[0].get("null_disparity_std"),
    ) != (
        d2[0]["p_value"],
        d2[0].get("null_disparity_mean"),
        d2[0].get("null_disparity_std"),
    )
