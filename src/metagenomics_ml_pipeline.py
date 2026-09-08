"""Public demonstration pipeline for colorectal-cancer metagenomics analysis.

The repository uses an example microbial abundance table. Statistical testing and
machine-learning code demonstrate workflow structure and software engineering
practices rather than clinical or biological validation.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kruskal
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from statsmodels.stats.multitest import multipletests


def get_feature_columns(data, label_column="label", sample_column="SampleID"):
    excluded = {label_column}
    if sample_column in data.columns:
        excluded.add(sample_column)
    return [column for column in data.columns if column not in excluded]


def validate_analysis_data(data, label_column="label", sample_column="SampleID"):
    """Validate labels and numeric microbial feature columns."""
    if data.empty:
        raise ValueError("Input abundance table is empty.")
    if label_column not in data.columns:
        raise ValueError(f"Required label column '{label_column}' was not found.")

    feature_names = get_feature_columns(data, label_column, sample_column)
    if not feature_names:
        raise ValueError("At least one microbial feature column is required.")

    if data[label_column].isna().any():
        raise ValueError("Label column contains missing values.")

    classes = set(pd.unique(data[label_column]))
    if classes != {0, 1}:
        raise ValueError("The public demo expects binary labels encoded as 0 and 1.")

    class_counts = data[label_column].value_counts()
    if int(class_counts.min()) < 2:
        raise ValueError("Each label class must contain at least two samples.")

    non_numeric = [
        column
        for column in feature_names
        if not pd.api.types.is_numeric_dtype(data[column])
    ]
    if non_numeric:
        raise ValueError(
            "Microbial feature columns must be numeric. Non-numeric columns: "
            + ", ".join(non_numeric)
        )

    if data[feature_names].isna().any().any():
        raise ValueError("Microbial feature matrix contains missing values.")

    if not np.isfinite(data[feature_names].to_numpy(dtype=float)).all():
        raise ValueError("Microbial feature matrix contains non-finite values.")

    return feature_names


def load_abundance_table(file_path, label_column="label", sample_column="SampleID"):
    """Load and validate a microbial abundance table."""
    data = pd.read_csv(file_path)
    validate_analysis_data(data, label_column, sample_column)
    return data


def run_kruskal_wallis(data, label_column="label", sample_column="SampleID"):
    """Run per-feature Kruskal-Wallis tests with Benjamini-Hochberg FDR correction."""
    features = validate_analysis_data(data, label_column, sample_column)
    results = []

    for feature in features:
        crc = data.loc[data[label_column] == 1, feature]
        control = data.loc[data[label_column] == 0, feature]
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

    results_df = pd.DataFrame(results)
    reject, q_values, _, _ = multipletests(
        results_df["p_value"].to_numpy(), alpha=0.05, method="fdr_bh"
    )
    results_df["q_value"] = q_values.astype(float)
    results_df["significant_fdr_0_05"] = reject.astype(bool)

    return results_df.sort_values(["q_value", "p_value"]).reset_index(drop=True)


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


def _validate_evaluation_settings(data, label_column, test_size, cv_splits, cv_repeats):
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")
    if cv_splits < 2:
        raise ValueError("cv_splits must be at least 2.")
    if cv_repeats < 1:
        raise ValueError("cv_repeats must be at least 1.")

    min_class_count = int(data[label_column].value_counts().min())
    if cv_splits > min_class_count:
        raise ValueError(
            f"cv_splits cannot exceed the smallest class size ({min_class_count})."
        )

    test_count = math.ceil(len(data) * test_size)
    train_count = len(data) - test_count
    if test_count < 2 or train_count < 2:
        raise ValueError("test_size leaves too few samples for a stratified split.")


def train_models(
    data,
    label_column="label",
    sample_column="SampleID",
    test_size=0.25,
    cv_splits=3,
    cv_repeats=2,
):
    """Evaluate models with one hold-out split plus repeated stratified CV."""
    feature_names = validate_analysis_data(data, label_column, sample_column)
    _validate_evaluation_settings(data, label_column, test_size, cv_splits, cv_repeats)

    X = data[feature_names]
    y = data[label_column]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y,
    )

    cv = RepeatedStratifiedKFold(
        n_splits=cv_splits,
        n_repeats=cv_repeats,
        random_state=42,
    )

    model_results = {}
    fitted_models = {}

    for model_name, model in build_models().items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        cv_scores = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring={"auc": "roc_auc", "accuracy": "accuracy"},
            return_train_score=False,
        )

        model_results[model_name] = {
            "auc": float(roc_auc_score(y_test, probabilities)),
            "accuracy": float(accuracy_score(y_test, predictions)),
            "classification_report": classification_report(
                y_test, predictions, output_dict=True, zero_division=0
            ),
            "cv_auc_mean": float(np.mean(cv_scores["test_auc"])),
            "cv_auc_std": float(np.std(cv_scores["test_auc"])),
            "cv_accuracy_mean": float(np.mean(cv_scores["test_accuracy"])),
            "cv_accuracy_std": float(np.std(cv_scores["test_accuracy"])),
            "cv_folds": int(len(cv_scores["test_auc"])),
        }
        fitted_models[model_name] = model

        print(
            f"{model_name}: hold-out AUC={model_results[model_name]['auc']:.3f}, "
            f"CV AUC={model_results[model_name]['cv_auc_mean']:.3f} "
            f"+/- {model_results[model_name]['cv_auc_std']:.3f}"
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
    parser.add_argument("--cv-splits", type=int, default=3)
    parser.add_argument("--cv-repeats", type=int, default=2)
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
    print("Loading and validating microbial abundance table...")
    data = load_abundance_table(args.input, args.label_column, args.sample_column)

    print("Running Kruskal-Wallis feature tests with Benjamini-Hochberg FDR correction...")
    stats_results = run_kruskal_wallis(
        data, args.label_column, args.sample_column
    )
    stats_path = Path(args.stats_output)
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    stats_results.to_csv(stats_path, index=False)

    print("Evaluating leakage-safe model pipelines with hold-out and repeated stratified CV...")
    model_results, fitted_models, feature_names = train_models(
        data,
        label_column=args.label_column,
        sample_column=args.sample_column,
        test_size=args.test_size,
        cv_splits=args.cv_splits,
        cv_repeats=args.cv_repeats,
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
