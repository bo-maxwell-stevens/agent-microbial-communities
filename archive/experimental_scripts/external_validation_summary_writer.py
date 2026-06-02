"""
Standalone utility to write validation summaries.
"""
import os

RESULTS_DIR = "results/phase3_environmental_partitioning/"

def write_validation_summary(excluded_cols, retained_cols):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(f"{RESULTS_DIR}/validation_summary.txt", "w") as summary_file:
        if excluded_cols:
            summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
        else:
            summary_file.write("No microbial/taxonomic columns were excluded.\n")

        if retained_cols:
            summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
        else:
            summary_file.write("No columns were retained.\n")