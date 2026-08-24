"""Public demonstration pipeline for colorectal-cancer metagenomics analysis.

The repository uses an example microbial abundance table. Statistical testing and
machine-learning code are intended to demonstrate workflow structure and software
engineering practices, not clinical or biological validation.
"""

import argparse
import json
from pathlib import Path

import pandas as pd
from scipy.stats import kruskal
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


def load_abundance_table(file_path, label_column="label"):
    """Load and validate a microbial abundance table."""
    data = pd.read_csv(file_path)
    if data.empty:
        raise ValueError("Input abundance table is empty.")
    if label_column not in data.columns:
        raise ValueError(f"Required label column '{label_column}' was not found.")
    return data


def get_feature_columns(data, label_column="label", sample_column="SampleID"):
    excluded = {label_column}
    if sample_column in data.columns:
        excluded.add(sample_column)
    return [column for column in data.columns if column not in excluded]


def run_kruskal_wallis(data, label_column="label", sample_column="SampleID"):
    """Run a two-group Kruskal-Wallis test for each microbial feature."""
    features = get_feature_columns(data, label_column, sample_column)
    results = []

    for feature in features:
        crc = data.loc[data[label_column] == 1, feature].dropna()
        control = data.loc[data[label_column] == 0, feature].dropna()
        if crc.empty or control.empty:
            continue

        statistic, p_value = kruskal(crc, control)
        results.append(
            {
                "feature": feature,
                "kruskal_wallis_statistic": float(statistic),
                "p_value": float(p_value),
                "mean_crc": float(crc.mean()),
                "mean_control": float(control.mean()),
            }
        )

    return pd.DataFrame(results).sort_values("p_value") if results else pd.DataFrame()


def build_models():
    """Construct leakage-safe model pipelines."""
    return {
        "Random Forest": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    RandomForestClassifier(n_estimators=200, random_state=42),
                ),
            ]
        ),
        "SVM": Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                ("classifier", SVC(kernel="rbf", probability=True, random_state=42)),
            ]
        ),
    }


def train_models(
    data,
    label_column="label",
    sample_column="SampleID",
    test_size=0.25,
):
    """Split first, then fit preprocessing and models only on training data."""
    feature_names = get_feature_columns(data, label_column, sample_column)
    X = data[feature_names]
    y = data[label_column]

    if y.nunique() != 2:
        raise ValueError("The public demo currently expects exactly two label classes.")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y,
    )

    model_results = {}
    fitted_models = {}

    for model_name, model in build_models().items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        model_results[model_name] = {
            "auc": float(roc_auc_score(y_test, probabilities)),
            "accuracy": float(accuracy_score(y_test, predictions)),
            "classification_report": classification_report(
                y_test, predictions, output_dict=True, zero_division=0
            ),
        }
        fitted_models[model_name] = model

        print(
            f"{model_name}: AUC={model_results[model_name]['auc']:.3f}, "
            f"accuracy={model_results[model_name]['accuracy']:.3f}"
        )

    return model_results, fitted_models, feature_names


def get_random_forest_feature_importance(model, feature_names):
    """Extract feature importances from the fitted Random Forest pipeline."""
    classifier = model.named_steps["classifier"]
    importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": classifier.feature_importances_}
    )
    return importance_df.sort_values("importance", ascending=False)


def save_json(data, output_file):
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the public metagenomics biomarker-analysis demonstration."
    )
    parser.add_argument(
        "--input", default="data/example_abundance_table.csv", help="Input CSV file."
    )
    parser.add_argument("--label-column", default="label")
    parser.add_argument("--sample-column", default="SampleID")
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument(
        "--metrics-output", default="results/model_metrics.json"
    )
    parser.add_argument(
        "--stats-output", default="results/kruskal_wallis_results.csv"
    )
    parser.add_argument(
        "--importance-output",
        default="results/random_forest_feature_importance.csv",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print("Loading microbial abundance table...")
    data = load_abundance_table(args.input, args.label_column)

    print("Running Kruskal-Wallis feature tests...")
    stats_results = run_kruskal_wallis(
        data, args.label_column, args.sample_column
    )
    stats_path = Path(args.stats_output)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_results.to_csv(stats_path, index=False)

    print("Training leakage-safe model pipelines...")
    model_results, fitted_models, feature_names = train_models(
        data,
        label_column=args.label_column,
        sample_column=args.sample_column,
        test_size=args.test_size,
    )
    save_json(model_results, args.metrics_output)

    print("Extracting Random Forest feature importance...")
    importance_df = get_random_forest_feature_importance(
        fitted_models["Random Forest"], feature_names
    )
    importance_path = Path(args.importance_output)
    importance_path.parent.mkdir(parents=True, exist_ok=True)
    importance_df.to_csv(importance_path, index=False)

    print("Public demonstration pipeline completed successfully.")


if __name__ == "__main__":
    main()
