import os
import pandas as pd

def validate_csv(summary_path, output_path):
    """Perform validation checks on the summary CSV."""
    messages = []

    if not os.path.exists(summary_path):
        messages.append(f"Error: Summary file not found at {summary_path}")
        with open(output_path, "w") as f:
            f.write("\n".join(messages))
        return

    try:
        df = pd.read_csv(summary_path)
    except Exception as e:
        messages.append(f"Error: Unable to read CSV file: {e}")
        with open(output_path, "w") as f:
            f.write("\n".join(messages))
        return

    # Check for required columns
    required_columns = ["procrustes_fit", "mantel_spearman", "pair", "branch", "threshold"]
    for col in required_columns:
        if col not in df.columns:
            messages.append(f"Error: Missing required column: {col}")

    # Check numeric columns
    for col in ["procrustes_fit", "mantel_spearman"]:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                messages.append(f"Error: Column {col} is not numeric")

    # Check for missing values
    if df.isnull().any().any():
        missing_columns = df.columns[df.isnull().any()].tolist()
        messages.append(f"Error: Missing values in columns: {', '.join(missing_columns)}")

    # Write validation summary
    if not messages:
        messages.append("Validation passed: All checks succeeded.")

    with open(output_path, "w") as f:
        f.write("\n".join(messages))


def main():
    base_dir = "results/phase2_confirmatory_coupling"
    summary_path = os.path.join(base_dir, "phase2_coupling_summary.csv")
    validation_output_path = os.path.join(base_dir, "validation_summary.txt")

    validate_csv(summary_path, validation_output_path)


if __name__ == "__main__":
    main()