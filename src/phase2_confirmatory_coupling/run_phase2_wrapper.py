"""
Thin wrapper script for Phase 2 confirmatory coupling analysis.

Distributes reusable functions to module imports.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from helpers import preprocess_table, generate_embeddings
from metrics import compute_procrustes, compute_mantel

# Cohort fixed at n=84
COHORT_FILE = "results/phase2_confirmatory_coupling/sample_cohort_used.csv"


def main():
    print("Running confirmatory coupling analysis...")
    # Full-run logic goes here (delegated to helpers/metrics)
    pass

if __name__ == "__main__":
    main()
