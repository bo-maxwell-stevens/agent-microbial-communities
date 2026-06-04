from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(rel: str) -> pd.DataFrame:
    return pd.read_csv(REPO_ROOT / rel)


def test_expected_phase_output_files_exist():
    required = [
        "results/phase2_confirmatory_coupling/phase2_coupling_summary.csv",
        "results/phase4_coupling_inference/phase4_summary.csv",
        "results/phase4_coupling_inference/phase4_mantel_inference.csv",
        "results/phase5_bac_integration/phase5_bac_coupling_summary.csv",
        "results/phase5_bac_integration/phase5_bac_mantel_inference.csv",
        "results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv",
        "results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv",
        "results/phase5c_plant_diversity/phase5c_model_comparison.csv",
        "results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv",
        "results/phase5d_synthesis/final_pair_synthesis.csv",
        "results/manuscript_verification/manuscript_numeric_claim_audit.csv",
        "results/manuscript_verification/pair_scope_audit.csv",
    ]
    for rel in required:
        assert (REPO_ROOT / rel).exists(), f"Missing required file: {rel}"


def test_expected_row_counts_and_columns_contract():
    contracts = {
        "results/phase2_confirmatory_coupling/phase2_coupling_summary.csv": (12, {"pair", "branch", "threshold", "procrustes_fit", "mantel_spearman"}),
        "results/phase4_coupling_inference/phase4_summary.csv": (6, {"pair", "branch", "rank_overall"}),
        "results/phase4_coupling_inference/phase4_mantel_inference.csv": (12, {"pair", "branch", "mantel_perm_pvalue", "n_permutations"}),
        "results/phase5_bac_integration/phase5_bac_coupling_summary.csv": (12, {"pair", "branch", "rank_overall"}),
        "results/phase5_bac_integration/phase5_bac_mantel_inference.csv": (24, {"pair", "branch", "mantel_perm_pvalue", "n_permutations"}),
        "results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv": (16, {"pair", "branch", "adjusted_r2", "permutation_p", "permutations"}),
        "results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv": (96, {"pair", "branch", "predictor", "delta_adj_r2", "permutations"}),
        "results/phase5c_plant_diversity/phase5c_model_comparison.csv": (112, {"pair", "branch", "hypothesis_id", "adjusted_r2", "delta_adjusted_r2_vs_base", "permutations"}),
        "results/phase5c_plant_diversity/phase5c_hypothesis_summary.csv": (12, {"hypothesis_id", "hypothesis_name", "overall_rank"}),
        "results/phase5d_synthesis/final_pair_synthesis.csv": (8, {"pair", "branch", "interpretation label"}),
    }
    for rel, (n_rows, cols) in contracts.items():
        df = _read(rel)
        assert len(df) == n_rows, f"Unexpected row count for {rel}: {len(df)} != {n_rows}"
        missing = cols.difference(df.columns)
        assert not missing, f"Missing columns in {rel}: {sorted(missing)}"


def test_pair_scope_counts_across_outputs():
    p5a_pairs = set(_read("results/phase5_bac_integration/phase5_bac_coupling_summary.csv")["pair"].astype(str))
    p5b_pairs = set(_read("results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv")["pair"].astype(str))
    p5c_pairs = set(_read("results/phase5c_plant_diversity/phase5c_model_comparison.csv")["pair"].astype(str))
    p5d_pairs = set(_read("results/phase5d_synthesis/final_pair_synthesis.csv")["pair"].astype(str))

    assert len(p5a_pairs) == 6
    assert len(p5b_pairs) == 4
    assert len(p5c_pairs) == 4
    assert len(p5d_pairs) == 4
    assert p5b_pairs == p5c_pairs == p5d_pairs


def test_manuscript_contains_top_ranked_pair_label():
    rank = _read("results/phase5_bac_integration/phase5_bac_rank_summary.csv")
    top_pair = rank.sort_values("rank_overall", ascending=True).iloc[0]["pair"]
    manuscript = (REPO_ROOT / "manuscript/manuscript_v22.md").read_text(errors="ignore")
    assert str(top_pair) in manuscript


def test_permutation_counts_are_999_for_current_manuscript_outputs():
    # This intentionally enforces the current verification requirement.
    checks = [
        ("results/phase4_coupling_inference/phase4_mantel_inference.csv", "n_permutations"),
        ("results/phase5_bac_integration/phase5_bac_mantel_inference.csv", "n_permutations"),
        ("results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv", "permutations"),
        ("results/phase5b_environmental_drivers/phase5b_predictor_ranking.csv", "permutations"),
        ("results/phase5c_plant_diversity/phase5c_model_comparison.csv", "permutations"),
        ("results/phase5c_plant_diversity/phase5c_predictor_effects.csv", "permutations"),
    ]
    for rel, col in checks:
        df = _read(rel)
        vals = set(df[col].dropna().astype(int).tolist())
        assert vals == {999}, f"{rel} has non-999 permutation counts: {sorted(vals)}"


def test_if_999_permutations_present_p_floor_is_0_001_or_greater():
    checks = [
        ("results/phase4_coupling_inference/phase4_mantel_inference.csv", "n_permutations", "mantel_perm_pvalue"),
        ("results/phase5_bac_integration/phase5_bac_mantel_inference.csv", "n_permutations", "mantel_perm_pvalue"),
        ("results/phase5b_environmental_drivers/phase5b_dbRDA_summary.csv", "permutations", "permutation_p"),
        ("results/phase5c_plant_diversity/phase5c_model_comparison.csv", "permutations", "permutation_p"),
    ]
    for rel, perm_col, p_col in checks:
        df = _read(rel)
        if (df[perm_col] == 999).any():
            subset = df[df[perm_col] == 999]
            assert (subset[p_col] >= 0.001 - 1e-12).all(), f"{rel} has p-values below 999 floor"


def test_numeric_claim_audit_artifact_has_core_columns():
    df = _read("results/manuscript_verification/manuscript_numeric_claim_audit.csv")
    required = {
        "manuscript_section",
        "claim_text",
        "reported_value",
        "source_output",
        "verified_value",
        "status",
        "notes",
    }
    missing = required.difference(df.columns)
    assert not missing, f"Missing columns in manuscript numeric audit: {sorted(missing)}"
    assert len(df) > 0
    assert set(df["status"]).intersection({"verified", "mismatch", "not_found", "needs_human_review"})
