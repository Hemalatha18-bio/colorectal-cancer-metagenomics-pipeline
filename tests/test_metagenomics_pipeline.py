import numpy as np
import pandas as pd
import pytest

from src.metagenomics_ml_pipeline import (
    get_feature_columns,
    load_abundance_table,
    run_kruskal_wallis,
    train_models,
)


def make_demo_data():
    return pd.DataFrame(
        {
            "SampleID": [f"S{i}" for i in range(12)],
            "taxon_a": [0.1, 0.9, 0.2, 0.8, 0.1, 0.9, 0.2, 0.8, 0.1, 0.9, 0.2, 0.8],
            "taxon_b": [0.8, 0.2, 0.7, 0.3, 0.8, 0.2, 0.7, 0.3, 0.8, 0.2, 0.7, 0.3],
            "taxon_c": [0.3, 0.7, 0.4, 0.6, 0.3, 0.7, 0.4, 0.6, 0.3, 0.7, 0.4, 0.6],
            "label": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        }
    )


def test_load_abundance_table_requires_label(tmp_path):
    path = tmp_path / "missing_label.csv"
    pd.DataFrame({"SampleID": ["S1"], "taxon_a": [0.1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Required label column"):
        load_abundance_table(path)


def test_load_abundance_table_rejects_empty_table(tmp_path):
    path = tmp_path / "empty.csv"
    pd.DataFrame(columns=["SampleID", "taxon_a", "label"]).to_csv(path, index=False)
    with pytest.raises(ValueError, match="empty"):
        load_abundance_table(path)


def test_load_abundance_table_rejects_missing_features(tmp_path):
    path = tmp_path / "missing.csv"
    data = make_demo_data()
    data.loc[0, "taxon_a"] = np.nan
    data.to_csv(path, index=False)
    with pytest.raises(ValueError, match="missing values"):
        load_abundance_table(path)


def test_load_abundance_table_rejects_non_numeric_features(tmp_path):
    path = tmp_path / "text.csv"
    data = make_demo_data()
    data["taxon_a"] = ["x"] * len(data)
    data.to_csv(path, index=False)
    with pytest.raises(ValueError, match="must be numeric"):
        load_abundance_table(path)


def test_feature_columns_exclude_metadata():
    data = make_demo_data()
    assert get_feature_columns(data) == ["taxon_a", "taxon_b", "taxon_c"]


def test_kruskal_wallis_returns_fdr_corrected_columns():
    results = run_kruskal_wallis(make_demo_data())
    assert set(results.columns) == {
        "feature",
        "kruskal_wallis_statistic",
        "p_value",
        "mean_crc",
        "mean_control",
        "q_value",
        "significant_fdr_0_05",
    }
    assert len(results) == 3
    assert results["p_value"].between(0.0, 1.0).all()
    assert results["q_value"].between(0.0, 1.0).all()
    assert results["significant_fdr_0_05"].dtype == bool


def test_fdr_q_values_are_not_smaller_than_raw_p_values():
    results = run_kruskal_wallis(make_demo_data())
    assert (results["q_value"] >= results["p_value"] - 1e-12).all()


def test_train_models_rejects_non_binary_labels():
    data = make_demo_data()
    data.loc[0, "label"] = 2
    with pytest.raises(ValueError, match="binary labels"):
        train_models(data)


def test_train_models_rejects_too_many_cv_splits():
    with pytest.raises(ValueError, match="smallest class size"):
        train_models(make_demo_data(), cv_splits=7)


def test_train_models_returns_valid_holdout_and_cv_metrics():
    results, fitted_models, feature_names = train_models(
        make_demo_data(),
        test_size=0.25,
        cv_splits=3,
        cv_repeats=2,
    )
    assert set(results) == {"Random Forest", "SVM"}
    assert set(fitted_models) == {"Random Forest", "SVM"}
    assert feature_names == ["taxon_a", "taxon_b", "taxon_c"]
    for metrics in results.values():
        assert 0.0 <= metrics["auc"] <= 1.0
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert 0.0 <= metrics["cv_auc_mean"] <= 1.0
        assert metrics["cv_auc_std"] >= 0.0
        assert 0.0 <= metrics["cv_accuracy_mean"] <= 1.0
        assert metrics["cv_accuracy_std"] >= 0.0
        assert metrics["cv_folds"] == 6
        assert "classification_report" in metrics
