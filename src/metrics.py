from __future__ import annotations

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def operational_accuracy(y_true, y_pred, tolerance: float = 2.0) -> float:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    return float(np.mean(np.abs(true - pred) <= tolerance) * 100)


def mape(y_true, y_pred) -> float:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    mask = true != 0
    if not mask.any():
        return float("nan")
    return float(np.mean(np.abs((true[mask] - pred[mask]) / true[mask])) * 100)


def smape(y_true, y_pred) -> float:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    denominator = (np.abs(true) + np.abs(pred)) / 2
    mask = denominator != 0
    if not mask.any():
        return float("nan")
    return float(np.mean(np.abs(true[mask] - pred[mask]) / denominator[mask]) * 100)


def evaluate_predictions(model_name, y_true, y_pred, train_time=None, prediction_time=None) -> dict:
    true = np.asarray(y_true, dtype=float)
    pred = np.maximum(np.asarray(y_pred, dtype=float), 0)
    return {
        "model": model_name,
        "MAE": mean_absolute_error(true, pred),
        "RMSE": np.sqrt(mean_squared_error(true, pred)),
        "MAPE_%": mape(true, pred),
        "sMAPE_%": smape(true, pred),
        "R2": r2_score(true, pred),
        "Operational_Accuracy_±2_%": operational_accuracy(true, pred),
        "Train_Time_sec": train_time,
        "Prediction_Time_sec": prediction_time,
    }
