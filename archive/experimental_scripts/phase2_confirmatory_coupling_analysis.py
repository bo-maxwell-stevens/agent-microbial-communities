#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist
from scipy.stats import pearsonr, spearmanr
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Extend Phase 1 foundation
KINGDOMS = ["AMF", "BAC", "EUK", "ITS"]
ENV_COVARIATES = [
    "pH_KCl", "N_pct", "C_pct", "P_Mehlich3_mg_100g", "K_Mehlich3_mg_100g",
    "hfp.300", "bio1now.100", "bio12now.100", "region", "PC1", "PC2", "PC3", "PC4",
]

# Add Phase 2-specific flag for stricter guardrails on adjustment
ADJUSTMENT_GUARDRAIL_DELTA_THRESHOLD = 0.1  # Example cutoff for magnitude deltas

### Implementation starts here ###
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Phase-2 confirmatory analysis for robust kingdom coupling signals")
    p.add_argument("--metadata", default="data/Final_data_with_diversity_prefixed.csv")
    p.add_argument("--output-dir", default="results/phase2_confirmatory_coupling")
    p.add_argument("--prevalence-thresholds", nargs="+", type=float, default=[0.05, 0.10, 0.20])
    p.add_argument("--n-pcs-options", nargs="+", type=int, default=[5, 10, 20])
    p.add_argument("--seed", type=int, default=42)
    return p.parse_args()

def directional_consistency_check(raw: dict[str, float], adjusted: dict[str, float]) -> bool:
    """Check if directional consistency is preserved between raw and adjusted metrics."""
    for k, v_raw in raw.items():
        adj = adjusted.get(k, np.nan)
        if np.isfinite(adj) and np.isfinite(v_raw):
            if (adj > 0 and v_raw > 0) or (adj < 0 and v_raw < 0):
                continue
            else:
                return False
    return True

def coupling_metrics_extended(a: np.ndarray, b: np.ndarray, threshold: float) -> dict[str, float]:
    """Compute raw, adjusted, and directional coupling metrics."""
    raw = coupling_metrics(a, b)
    adj = residualize(a, b)
    return {**raw, **adj}

def ensure_adjustment_guardrails(adj_delta: float) -> bool:
    """Prevent unstable adjustment dynamics."""
    return adj_delta < np.abs(ADJUSTMENT_GUARDRAIL_DELTA_THRESHOLD)# INSERT MAIN

if __name__ ="__"....Do ulg