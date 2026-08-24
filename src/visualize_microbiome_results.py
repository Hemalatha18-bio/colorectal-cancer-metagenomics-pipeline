"""Visualize outputs from the public metagenomics demonstration pipeline."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_microbial_abundance(input_file, output_file, label_column="label", sample_column="SampleID"):
    data = pd.read_csv(input_file)
    excluded = {label_column}
    if sample_column in data.columns:
        excluded.add(sample_column)
    features = [column for column in data.columns if column not in excluded]

    grouped = data.groupby(label_column)[features].mean().T
    grouped = grouped.rename(columns={0: "Control", 1: "Colorectal Cancer"})

    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    grouped.plot(kind="bar", figsize=(10, 6))
    plt.xlabel("Microbial Feature")
    plt.ylabel("Mean Abundance")
    plt.title("Microbial Abundance by Group (Example Data)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()


def plot_model_metrics(metrics_file, output_file):
    with open(metrics_file, "r", encoding="utf-8") as handle:
        metrics = json.load(handle)

    results = pd.DataFrame(
        {
            "Model": list(metrics.keys()),
            "AUC": [metrics[name]["auc"] for name in metrics],
            "Accuracy": [metrics[name]["accuracy"] for name in metrics],
        }
    )

    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    ax = results.set_index("Model")[["AUC", "Accuracy"]].plot(kind="bar", figsize=(8, 5))
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_title("Model Performance on Example Data")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()


def plot_feature_importance(importance_file, output_file, top_n=10):
    importance = pd.read_csv(importance_file)
    required = {"feature", "importance"}
    if not required.issubset(importance.columns):
        raise ValueError("Feature-importance file must contain 'feature' and 'importance' columns.")

    importance = importance.sort_values("importance", ascending=False).head(top_n)
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(9, 5))
    plt.bar(importance["feature"], importance["importance"])
    plt.xlabel("Microbial Feature")
    plt.ylabel("Random Forest Importance")
    plt.title("Top Random Forest Feature Importances (Example Data)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output, dpi=300, bbox_inches="tight")
    plt.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Create figures from pipeline outputs.")
    parser.add_argument("--input", default="data/example_abundance_table.csv")
    parser.add_argument("--metrics", default="results/model_metrics.json")
    parser.add_argument("--importance", default="results/random_forest_feature_importance.csv")
    parser.add_argument("--output-dir", default="figures")
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--sample-column", default="SampleID")
    parser.add_argument("--top-n", type=int, default=10)
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    print("Generating figures from public-demo outputs...")
    plot_microbial_abundance(
        args.input,
        output_dir / "example_microbiome_abundance.png",
        args.label_column,
        args.sample_column,
    )
    plot_model_metrics(args.metrics, output_dir / "model_performance.png")
    plot_feature_importance(
        args.importance,
        output_dir / "microbial_feature_importance.png",
        args.top_n,
    )
    print(f"Figures saved under {output_dir}")


if __name__ == "__main__":
    main()
