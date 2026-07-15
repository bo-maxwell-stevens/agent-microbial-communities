import math

import numpy as np
import pandas as pd
import pytest
from scipy.stats import spearmanr

from src.coupling_metrics import (
    condense_distance_matrix,
    mantel_spearman,
    procrustes_disparity,
)


def _dist_df(values: np.ndarray, labels: list[str]) -> pd.DataFrame:
    return pd.DataFrame(values, index=labels, columns=labels)


def test_condense_distance_matrix_upper_triangle_ordering_known_matrix():
    labels = ["S1", "S2", "S3", "S4"]
    d = _dist_df(
        np.array(
            [
                [0.0, 1.0, 2.0, 3.0],
                [1.0, 0.0, 4.0, 5.0],
                [2.0, 4.0, 0.0, 6.0],
                [3.0, 5.0, 6.0, 0.0],
            ]
        ),
        labels,
    )
    got = condense_distance_matrix(d)
    assert np.array_equal(got, np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0]))


def test_condense_distance_matrix_mismatched_labels_raise():
    d = pd.DataFrame(
        [[0.0, 1.0], [1.0, 0.0]],
        index=["S1", "S2"],
        columns=["S2", "S1"],
    )
    with pytest.raises(ValueError, match="row and column labels"):
        condense_distance_matrix(d)


def test_condense_distance_matrix_non_square_raises():
    d = pd.DataFrame(
        [[0.0, 1.0, 2.0], [1.0, 0.0, 3.0]],
        index=["S1", "S2"],
        columns=["S1", "S2", "S3"],
    )
    with pytest.raises(ValueError, match="square"):
        condense_distance_matrix(d)


def test_procrustes_disparity_identical_ordinations_zero():
    emb = pd.DataFrame(
        [[0.0, 1.0], [1.0, 0.0], [2.0, 3.0]],
        index=["S1", "S2", "S3"],
    )
    got = procrustes_disparity(emb, emb.copy())
    assert got == pytest.approx(0.0, abs=1e-12)


def test_procrustes_disparity_dimension_mismatch_raises():
    x = pd.DataFrame([[0.0, 1.0], [1.0, 0.0]], index=["S1", "S2"])
    y = pd.DataFrame([[0.0, 1.0, 2.0], [1.0, 0.0, 3.0]], index=["S1", "S2"])
    with pytest.raises(ValueError, match="same number of columns"):
        procrustes_disparity(x, y)


def test_mantel_spearman_hand_checkable_example_matches_scipy():
    labels = ["S1", "S2", "S3", "S4"]
    x = _dist_df(
        np.array(
            [
                [0.0, 1.0, 2.0, 3.0],
                [1.0, 0.0, 4.0, 5.0],
                [2.0, 4.0, 0.0, 6.0],
                [3.0, 5.0, 6.0, 0.0],
            ]
        ),
        labels,
    )
    y = _dist_df(
        np.array(
            [
                [0.0, 10.0, 20.0, 30.0],
                [10.0, 0.0, 40.0, 50.0],
                [20.0, 40.0, 0.0, 60.0],
                [30.0, 50.0, 60.0, 0.0],
            ]
        ),
        labels,
    )
    expected, _ = spearmanr(condense_distance_matrix(x), condense_distance_matrix(y))
    got = mantel_spearman(x, y)
    assert got == pytest.approx(float(expected), abs=1e-12)


def test_mantel_spearman_identical_distance_matrices_is_one():
    labels = ["S1", "S2", "S3"]
    x = _dist_df(
        np.array(
            [
                [0.0, 1.0, 2.0],
                [1.0, 0.0, 3.0],
                [2.0, 3.0, 0.0],
            ]
        ),
        labels,
    )
    got = mantel_spearman(x, x.copy())
    assert got == pytest.approx(1.0, abs=1e-12)


def test_mantel_spearman_reversed_distance_ordering_negative_one():
    labels = ["S1", "S2", "S3", "S4"]
    x = _dist_df(
        np.array(
            [
                [0.0, 1.0, 2.0, 3.0],
                [1.0, 0.0, 4.0, 5.0],
                [2.0, 4.0, 0.0, 6.0],
                [3.0, 5.0, 6.0, 0.0],
            ]
        ),
        labels,
    )
    y_vals = np.array([6.0, 5.0, 4.0, 3.0, 2.0, 1.0])
    y = _dist_df(
        np.array(
            [
                [0.0, y_vals[0], y_vals[1], y_vals[2]],
                [y_vals[0], 0.0, y_vals[3], y_vals[4]],
                [y_vals[1], y_vals[3], 0.0, y_vals[5]],
                [y_vals[2], y_vals[4], y_vals[5], 0.0],
            ]
        ),
        labels,
    )
    got = mantel_spearman(x, y)
    assert got == pytest.approx(-1.0, abs=1e-12)


def test_mantel_spearman_constant_vectors_return_nan_explicitly():
    labels = ["S1", "S2", "S3"]
    const = _dist_df(
        np.array(
            [
                [0.0, 1.0, 1.0],
                [1.0, 0.0, 1.0],
                [1.0, 1.0, 0.0],
            ]
        ),
        labels,
    )
    got = mantel_spearman(const, const.copy())
    assert math.isnan(got)


def test_mantel_spearman_label_ordering_is_enforced():
    x = pd.DataFrame(
        [[0.0, 1.0, 2.0], [1.0, 0.0, 3.0], [2.0, 3.0, 0.0]],
        index=["S1", "S2", "S3"],
        columns=["S1", "S2", "S3"],
    )
    y = pd.DataFrame(
        [[0.0, 1.0, 2.0], [1.0, 0.0, 3.0], [2.0, 3.0, 0.0]],
        index=["S1", "S3", "S2"],
        columns=["S1", "S3", "S2"],
    )
    with pytest.raises(ValueError, match="sample ordering"):
        mantel_spearman(x, y)
