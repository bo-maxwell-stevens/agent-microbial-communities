import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def create_directory(path):
    """Ensure target directory exists."""
    if not os.path.exists(path):
        os.makedirs(path)

def plot_heatmap(data, title, fname, output_dir):
    """Generate a heatmap from the given dataframe."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(data, annot=True, cmap="viridis", cbar=True)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, fname))
    plt.close()

def plot_grouped_bar(data, x, y, hue, title, fname, output_dir):
    """Generate grouped bar plots."""
    plt.figure(figsize=(12, 6))
    sns.barplot(data=data, x=x, y=y, hue=hue)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, fname))
    plt.close()

def main():
    base_dir = "results/phase2_confirmatory_coupling"
    figures_dir = os.path.join(base_dir, "figures")
    create_directory(figures_dir)

    # Read core summary CSV
    summary_path = os.path.join(base_dir, "phase2_coupling_summary.csv")
    if not os.path.exists(summary_path):
        print(f"Summary file not found: {summary_path}")
        return

    # Load data
    try:
        summary_df = pd.read_csv(summary_path)
    except Exception as e:
        print(f"Error reading summary file: {e}")
        return

    # Validate required columns exist
    required_columns = ["procrustes_fit", "mantel_spearman", "pair", "branch", "threshold"]
    for col in required_columns:
        if col not in summary_df.columns:
            print(f"Missing required column: {col}")
            return

    # Generate heatmaps for `procrustes_fit` and `mantel_spearman`
    for metric in ["procrustes_fit", "mantel_spearman"]:
        pivot_table = summary_df.pivot_table(index="pair", columns="branch", values=metric, aggfunc="mean")
        plot_heatmap(
            data=pivot_table,
            title=f"Heatmap of {metric} by Domain Pair and Transformation",
            fname=f"heatmap_{metric}.png",
            output_dir=figures_dir
        )

    # Generate grouped bar plots
    plot_grouped_bar(
        data=summary_df,
        x="pair",
        y="mantel_spearman",
        hue="branch",
        title="Grouped Bar Plot of Mantel Spearman",
        fname="grouped_bar_mantel.png",
        output_dir=figures_dir
    )

    plot_grouped_bar(
        data=summary_df,
        x="pair",
        y="procrustes_fit",
        hue="branch",
        title="Grouped Bar Plot of Procrustes Fit",
        fname="grouped_bar_procrustes.png",
        output_dir=figures_dir
    )

if __name__ == "__main__":
    main()