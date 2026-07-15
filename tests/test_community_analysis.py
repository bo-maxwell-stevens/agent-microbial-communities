import ast
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform

from src.community_analysis import (
    PSEUDOCOUNT,
    branch_distance,
    clr_transform,
    combined_pair_distance,
    pca_table,
    pcoa_coords,
    prevalence_filter_table,
    to_presence_absence,
    to_relative_abundance,
)


def _toy_table() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "f1": [1.0, 0.0, 3.0, 0.0],
            "f2": [0.0, 0.0, 1.0, 0.0],
            "f3": [0.0, 2.0, 0.0, 0.0],
            "f4": [5.0, 0.0, 0.0, 0.0],
        },
        index=["s1", "s2", "s3", "s4"],
    )


def test_prevalence_filter_exact_threshold_boundary():
    table = _toy_table()
    out = prevalence_filter_table(table, threshold=0.25)
    assert list(out.columns) == ["f1", "f2", "f3", "f4"]


def test_prevalence_filter_no_feature_behavior_keeps_top1_feature():
    table = _toy_table()
    out = prevalence_filter_table(table, threshold=0.80)
    prevalence = (table.reindex(sorted(table.columns), axis=1) > 0).mean(axis=0)
    expected_top = prevalence.sort_values(ascending=False).head(1).index.tolist()
    assert out.shape == (table.shape[0], 1)
    assert list(out.columns) == expected_top


def test_to_presence_absence_conversion():
    out = to_presence_absence(_toy_table())
    assert set(np.unique(out.to_numpy())) <= {0.0, 1.0}


def test_relative_abundance_normal_and_zero_library_behavior():
    table = _toy_table().copy()
    table.loc["s4", :] = 0.0
    rel = to_relative_abundance(table)
    assert np.isclose(rel.loc["s1"].sum(), 1.0)
    assert np.isclose(rel.loc["s4"].sum(), 0.0)
    assert np.isfinite(rel.to_numpy()).all()


def test_clr_uses_exact_phase5_pseudocount_and_returns_finite():
    rel = to_relative_abundance(_toy_table())
    clr = clr_transform(rel, pseudocount=PSEUDOCOUNT)
    expected = np.log(rel.to_numpy() + PSEUDOCOUNT)
    expected -= np.log(np.exp(expected.mean(axis=1, keepdims=True)))
    assert np.allclose(clr.to_numpy(), expected)
    assert np.isfinite(clr.to_numpy()).all()


def test_pca_table_deterministic_and_preserves_labels():
    rel = to_relative_abundance(_toy_table())
    clr = clr_transform(rel)
    p1 = pca_table(clr)
    p2 = pca_table(clr)
    assert p1.index.equals(clr.index)
    assert np.allclose(p1.to_numpy(), p2.to_numpy())


def test_branch_distance_shape_labels_metric_behavior():
    table = _toy_table()
    d_pa = branch_distance(table, "presence/absence")
    assert d_pa.shape[0] == (len(table.index) * (len(table.index) - 1)) // 2
    pa = to_presence_absence(table)
    expected = pdist(pa.to_numpy(dtype=np.float64), metric="jaccard")
    assert np.allclose(d_pa, expected)


def test_combined_pair_distance_alignment_behavior():
    a = _toy_table()
    b = _toy_table().iloc[::-1].copy().iloc[::-1]  # same label order preserved
    combo = combined_pair_distance(a, b, "presence/absence")
    da = squareform(branch_distance(a, "presence/absence"), checks=False)
    db = squareform(branch_distance(b, "presence/absence"), checks=False)
    expected = squareform(0.5 * (da + db), checks=False)
    assert np.allclose(combo, expected)


def test_pcoa_determinism_and_shape():
    d = branch_distance(_toy_table(), "presence/absence")
    c1 = pcoa_coords(d)
    c2 = pcoa_coords(d)
    assert c1.shape[0] == _toy_table().shape[0]
    assert np.allclose(c1, c2)


def test_shared_helpers_match_legacy_phase5b_formulas():
    table = _toy_table()
    prevalence = (table > 0).mean(axis=0)
    kept = prevalence[prevalence >= 0.25].sort_values(ascending=False).index.tolist()
    legacy_filtered = table.reindex(columns=sorted(kept))
    assert prevalence_filter_table(table, 0.25).equals(legacy_filtered)


def test_shared_helpers_match_legacy_phase5c_formulas():
    table = _toy_table()
    rel = table.div(table.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)
    legacy_clr = np.log(rel.to_numpy(dtype=np.float64, copy=True) + 1e-6)
    legacy_clr -= np.log(np.exp(legacy_clr.mean(axis=1, keepdims=True)))
    out = clr_transform(to_relative_abundance(table), pseudocount=1e-6)
    assert np.allclose(out.to_numpy(), legacy_clr)


def test_phase5_scripts_no_longer_define_removed_local_helpers():
    helpers = {
        "load_otu_table",
        "prevalence_filter_table",
        "to_presence_absence",
        "to_relative_abundance",
        "clr_transform",
        "pca_table",
        "branch_distance",
        "combined_pair_distance",
        "pcoa_coords",
    }
    for script in [
        Path("scripts/analysis/phase5b_environmental_drivers.py"),
        Path("scripts/analysis/phase5c_plant_diversity_hypotheses.py"),
    ]:
        tree = ast.parse(script.read_text())
        defined = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        assert helpers.isdisjoint(defined), f"{script} still defines {helpers & defined}"
