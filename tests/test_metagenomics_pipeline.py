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


def test_feature_columns_exclude_metadata():
    data = make_demo_data()
    assert get_feature_columns(data) == ["taxon_a", "taxon_b", "taxon_c"]


def test_kruskal_wallis_returns_expected_columns():
    results = run_kruskal_wallis(make_demo_data())
    assert set(results.columns) == {
        "feature",
        "kruskal_wallis_statistic",
        "p_value",
        "mean_crc",
        "mean_control",
    }
    assert len(results) == 3


def test_train_models_returns_valid_metrics():
    results, fitted_models, feature_names = train_models(make_demo_data(), test_size=0.25)
    assert set(results) == {"Random Forest", "SVM"}
    assert set(fitted_models) == {"Random Forest", "SVM"}
    assert feature_names == ["taxon_a", "taxon_b", "taxon_c"]
    for metrics in results.values():
        assert 0.0 <= metrics["auc"] <= 1.0
        assert 0.0 <= metrics["accuracy"] <= 1.0
        assert "classification_report" in metrics
