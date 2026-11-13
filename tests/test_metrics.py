import pytest

from src.metrics import evaluate_predictions, operational_accuracy


def test_operational_accuracy():
    assert operational_accuracy([10, 10, 10], [8, 11, 14]) == pytest.approx(66.6666667)


def test_evaluation_has_expected_metrics():
    row = evaluate_predictions("test", [10, 12], [11, 10])
    assert row["MAE"] == pytest.approx(1.5)
    assert "RMSE" in row
    assert "Operational_Accuracy_±2_%" in row
