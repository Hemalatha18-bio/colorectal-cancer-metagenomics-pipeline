"""
Visualization script for metagenomic biomarker discovery project.

This script creates example visualizations for microbial abundance,
model performance, and feature importance.

Author: Hemalatha Ponnam
"""

import pandas as pd
import matplotlib.pyplot as plt


def plot_microbial_abundance():
    """
    Plot example average microbial abundance by group.
    """

    data = pd.read_csv("data/example_abundance_table.csv")

    feature_columns = [
        col for col in data.columns
        if col not in ["SampleID", "label"]
    ]

    grouped = data.groupby("label")[feature_columns].mean().T
    grouped.columns = ["Control", "Colorectal Cancer"]

    grouped.plot(kind="bar", figsize=(10, 6))
    plt.xlabel("Microbial Feature")
    plt.ylabel("Mean Relative Abundance")
    plt.title("Example Microbial Abundance by Group")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("figures/example_microbiome_abundance.png", dpi=300)
    plt.show()


def plot_model_auc():
    """
    Plot example AUC comparison for microbiome classifiers.
    """

    results = pd.DataFrame({
        "Model": ["Random Forest", "SVM"],
        "AUC": [0.92, 0.90]
    })

    plt.figure(figsize=(7, 5))
    plt.bar(results["Model"], results["AUC"])
    plt.ylim(0, 1)
    plt.xlabel("Machine Learning Model")
    plt.ylabel("AUC Score")
    plt.title("Example Model Performance")
    plt.tight_layout()
    plt.savefig("figures/model_auc_comparison.png", dpi=300)
    plt.show()


def plot_feature_importance():
    """
    Plot example microbial feature importance.
    """

    importance = pd.DataFrame({
        "Feature": [
            "Fusobacterium",
            "Faecalibacterium",
            "Escherichia",
            "Prevotella",
            "Bacteroides"
        ],
        "Importance": [0.31, 0.22, 0.18, 0.15, 0.10]
    })

    plt.figure(figsize=(8, 5))
    plt.bar(importance["Feature"], importance["Importance"])
    plt.xlabel("Microbial Feature")
    plt.ylabel("Example Feature Importance")
    plt.title("Example Microbial Biomarker Importance")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("figures/microbial_feature_importance.png", dpi=300)
    plt.show()


def main():
    print("Generating microbiome visualizations...")
    plot_microbial_abundance()
    plot_model_auc()
    plot_feature_importance()
    print("Figures saved in the figures/ folder.")


if __name__ == "__main__":
    main()
