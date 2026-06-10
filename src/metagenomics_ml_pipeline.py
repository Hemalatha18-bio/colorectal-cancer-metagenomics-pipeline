"""
Metagenomic Biomarker Discovery Pipeline for Colorectal Cancer

This script demonstrates a simplified microbiome analysis workflow:
1. Load microbial abundance table
2. Perform basic statistical comparison
3. Train Random Forest and SVM classifiers
4. Evaluate model performance
5. Export feature importance results

Author: Hemalatha Ponnam
"""

import pandas as pd
import numpy as np

from scipy.stats import kruskal
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, roc_auc_score


def load_abundance_table(file_path):
    """
    Load microbial abundance table.

    Expected format:
    - Rows = samples
    - Columns = microbial taxa/features
    - One column named 'label'
      label = 1 for colorectal cancer group
      label = 0 for control group
    """
    data = pd.read_csv(file_path)
    return data


def run_kruskal_wallis(data, label_column="label", sample_column="SampleID"):
    """
    Run Kruskal-Wallis test for each microbial feature.
    """

    feature_columns = [
        col for col in data.columns
        if col not in [label_column, sample_column]
    ]

    results = []

    for feature in feature_columns:
        group_1 = data[data[label_column] == 1][feature]
        group_0 = data[data[label_column] == 0][feature]

        statistic, p_value = kruskal(group_1, group_0)

        results.append({
            "Feature": feature,
            "Kruskal_Wallis_Statistic": statistic,
            "P_Value": p_value,
            "Mean_CRC": group_1.mean(),
            "Mean_Control": group_0.mean()
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("P_Value")

    return results_df


def prepare_ml_data(data, label_column="label", sample_column="SampleID"):
    """
    Prepare feature matrix and labels for machine learning.
    """

    X = data.drop(columns=[label_column, sample_column])
    y = data[label_column]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y, X.columns


def train_models(X, y):
    """
    Train Random Forest and SVM classifiers.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ),
        "SVM": SVC(
            kernel="rbf",
            probability=True,
            random_state=42
        )
    }

    model_results = {}

    for model_name, model in models.items():
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        auc = roc_auc_score(y_test, y_prob)
        report = classification_report(y_test, y_pred)

        model_results[model_name] = {
            "model": model,
            "auc": auc,
            "classification_report": report
        }

        print("\n==============================")
        print(f"Model: {model_name}")
        print(f"AUC: {auc:.3f}")
        print(report)

    return model_results


def get_random_forest_feature_importance(model, feature_names):
    """
    Extract feature importance from Random Forest model.
    """

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": model.feature_importances_
    })

    importance_df = importance_df.sort_values(
        "Importance",
        ascending=False
    )

    return importance_df


def main():
    """
    Run the example metagenomics analysis workflow.
    """

    file_path = "data/example_abundance_table.csv"

    print("Loading microbial abundance table...")
    data = load_abundance_table(file_path)

    print("Running biomarker statistics...")
    stats_results = run_kruskal_wallis(data)
    print(stats_results)

    stats_results.to_csv(
        "results/kruskal_wallis_results.csv",
        index=False
    )

    print("Preparing machine learning data...")
    X, y, feature_names = prepare_ml_data(data)

    print("Training machine learning models...")
    model_results = train_models(X, y)

    rf_model = model_results["Random Forest"]["model"]

    print("Extracting Random Forest feature importance...")
    importance_df = get_random_forest_feature_importance(
        rf_model,
        feature_names
    )

    print(importance_df)

    importance_df.to_csv(
        "results/random_forest_feature_importance.csv",
        index=False
    )

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
