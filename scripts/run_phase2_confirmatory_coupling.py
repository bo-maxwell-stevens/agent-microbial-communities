"""
Run Phase 2 Confirmatory Coupling Analysis

Final corrections: restore metric functions and ensure diagnostics.
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize
from scipy.stats import spearmanr
from scipy.spatial import procrustes
from pathlib import Path

# Paths
DATA_DIR = "data"
RESULTS_DIR = "results/phase2_confirmatory_coupling"
COHORT_FILE = f"{RESULTS_DIR}/sample_cohort_used.csv"

# Functions

def load_otu_table(name):
    path = f"{DATA_DIR}/{name}_OTU_table_final.tsv"
    return pd.read_csv(path, sep="\t", index_col=0)


def preprocess_table(filtered_matrix, cohort_sample_ids):
    assert list(filtered_matrix.index) == cohort_sample_ids, "Row mismatch after filtering."
    clr_matrix = normalize(np.log1p(filtered_matrix + 1), axis=0)
    return clr_matrix


def generate_embeddings(matrix, cohort_sample_ids):
    pca = PCA(n_components=min(10, matrix.shape[1], len(cohort_sample_ids) - 1))
    embeddings = pd.DataFrame(pca.fit_transform(matrix), index=cohort_sample_ids)
    return embeddings


def compute_procrustes(X, Y):
    try:
        _, _, disparity = procrustes(X, Y)
        return {"procrustes_fit": float(disparity)}
    except Exception as e:
        return {"procrustes_fit": np.nan, "error": str(e)}

def compute_mantel(X, Y):
    """Perform Mantel test using pairwise distances."""
    try:
        dist_X = pairwise_distances(X)
        dist_Y = pairwise_distances(Y)
        spearman, _ = spearmanr(dist_X.ravel(), dist_Y.ravel())
        return {"mantel_spearman": spearman}
    except Exception as e:
        return {"mantel_spearman": np.nan, "error": str(e)}


def main():
    print("Running Phase 2 confirmatory coupling analysis...")
    cohort = pd.read_csv(COHORT_FILE)["Sample_ID"].tolist()
    tables = {name: load_otu_table(name).loc[cohort] for name in ["AMF", "EUK", "ITS"]}

    pairs = [("EUK", "ITS"), ("AMF", "ITS"), ("AMF", "EUK")]
    results = []

    for threshold in [0.05, 0.10]:
        for branch in ["presence/absence", "CLR"]:
            for name1, name2 in pairs:
                table1 = tables[name1]
                table2 = tables[name2]

                filtered1 = table1.loc[:, table1.mean(axis=0) > threshold]
                filtered2 = table2.loc[:, table2.mean(axis=0) > threshold]

                clr1 = preprocess_table(filtered1, cohort)
                clr2 = preprocess_table(filtered2, cohort)

                embeddings1 = generate_embeddings(clr1, cohort)
                embeddings2 = generate_embeddings(clr2, cohort)

                metrics = {}
                metrics.update(compute_procrustes(embeddings1, embeddings2))
                metrics.update(compute_mantel(embeddings1, embeddings2))

                results.append({
                    "pair": f"{name1}↔{name2}",
                    "branch": branch,
                    "threshold": threshold,
                    **metrics
                })

    pd.DataFrame(results).to_csv(f"{RESULTS_DIR}/phase2_coupling_summary.csv", index=False)
    print("Phase 2 analysis completed.")

if __name__ == "__main__":
    main()
