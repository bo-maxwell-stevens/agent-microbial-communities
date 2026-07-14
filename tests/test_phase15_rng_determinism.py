import subprocess
import sys

import numpy as np
import pandas as pd

from src.phase1_ecological_exploration.diagnostics import (
    compare_ordinations,
    derive_stable_seed,
    procrustes_permutation_test,
)


def _coords(seed: int, n: int = 24, d: int = 3) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    data = rng.normal(size=(n, d))
    return pd.DataFrame(data, index=[f"s{i}" for i in range(n)], columns=[f"c{j}" for j in range(d)])


def _ordination_results() -> dict:
    return {
        "jaccard_pcoa": {"coordinates": _coords(11)},
        "bray_curtis_pcoa": {"coordinates": _coords(22)},
        "clr_pca": {
            "clr_0.01": {"coordinates": _coords(33)},
            "clr_0.05": {"coordinates": _coords(44)},
        },
    }


def _diag_map(diags):
    return {(d["ordination_a"], d["ordination_b"]): d for d in diags}


def test_same_seed_gives_identical_permutation_diagnostics():
    a = _coords(100)
    b = _coords(200)

    d1 = procrustes_permutation_test(a, b, n_permutations=199, random_state=12345)
    d2 = procrustes_permutation_test(a, b, n_permutations=199, random_state=12345)

    assert d1["p_value"] == d2["p_value"]
    assert d1["null_disparity_mean"] == d2["null_disparity_mean"]
    assert d1["null_disparity_std"] == d2["null_disparity_std"]
    assert d1["disparity"] == d2["disparity"]


def test_different_seeds_can_change_permutation_diagnostics():
    a = _coords(100)
    b = _coords(200)

    d1 = procrustes_permutation_test(a, b, n_permutations=199, random_state=12345)
    d2 = procrustes_permutation_test(a, b, n_permutations=199, random_state=54321)

    changed = (
        d1["p_value"] != d2["p_value"]
        or d1["null_disparity_mean"] != d2["null_disparity_mean"]
        or d1["null_disparity_std"] != d2["null_disparity_std"]
    )
    assert changed


def test_iteration_order_does_not_change_named_comparison_results():
    ord_results = _ordination_results()

    order_a = [
        ("jaccard_pcoa", "bray_curtis_pcoa"),
        ("jaccard_pcoa", "clr_0.01"),
        ("bray_curtis_pcoa", "clr_0.05"),
    ]
    order_b = list(reversed(order_a))

    d1 = compare_ordinations(
        ord_results,
        method_pairs=order_a,
        use_permutation_test=True,
        random_state=4242,
        n_permutations=199,
    )
    d2 = compare_ordinations(
        ord_results,
        method_pairs=order_b,
        use_permutation_test=True,
        random_state=4242,
        n_permutations=199,
    )

    m1 = _diag_map(d1)
    m2 = _diag_map(d2)
    assert set(m1) == set(m2)

    for key in m1:
        assert m1[key]["random_seed"] == m2[key]["random_seed"]
        assert m1[key]["p_value"] == m2[key]["p_value"]
        assert m1[key]["null_disparity_mean"] == m2[key]["null_disparity_mean"]
        assert m1[key]["null_disparity_std"] == m2[key]["null_disparity_std"]


def test_derived_seed_is_stable_across_python_processes():
    code = (
        "from src.phase1_ecological_exploration.diagnostics import derive_stable_seed;"
        "print(derive_stable_seed(42,'AMF','clr_0.01','jaccard_pcoa_vs_clr_0.01'))"
    )
    v1 = subprocess.check_output([sys.executable, "-c", code], text=True).strip()
    v2 = subprocess.check_output([sys.executable, "-c", code], text=True).strip()

    assert v1 == v2
    assert int(v1) == derive_stable_seed(42, "AMF", "clr_0.01", "jaccard_pcoa_vs_clr_0.01")
