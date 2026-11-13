from __future__ import annotations

import time

import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

from .config import SEASONAL_PERIOD
from .metrics import evaluate_predictions

STATISTICAL_SPECS = {
    "ARIMA(0,1,1)": {"kind": "ARIMA", "order": (0, 1, 1)},
    "ARIMA(1,0,1)": {"kind": "ARIMA", "order": (1, 0, 1)},
    "ARIMA(1,1,0)": {"kind": "ARIMA", "order": (1, 1, 0)},
    "ARIMA(1,1,1)": {"kind": "ARIMA", "order": (1, 1, 1)},
    "ARIMA(2,0,2)": {"kind": "ARIMA", "order": (2, 0, 2)},
    "ARIMA(2,1,1)": {"kind": "ARIMA", "order": (2, 1, 1)},
    "SARIMAX(1,0,1)x(1,0,1,7)": {
        "kind": "SARIMAX",
        "order": (1, 0, 1),
        "seasonal_order": (1, 0, 1, SEASONAL_PERIOD),
    },
    "SARIMAX(1,1,1)x(1,0,1,7)": {
        "kind": "SARIMAX",
        "order": (1, 1, 1),
        "seasonal_order": (1, 0, 1, SEASONAL_PERIOD),
    },
    "SARIMAX(2,1,1)x(1,0,1,7)": {
        "kind": "SARIMAX",
        "order": (2, 1, 1),
        "seasonal_order": (1, 0, 1, SEASONAL_PERIOD),
    },
}


def fit_statistical_model(series, spec: dict):
    if spec["kind"] == "ARIMA":
        return ARIMA(series, order=spec["order"]).fit()
    return SARIMAX(
        series,
        order=spec["order"],
        seasonal_order=spec["seasonal_order"],
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False, maxiter=200)


def evaluate_statistical_models(y_train, y_test):
    rows, predictions = [], {}
    for name, spec in STATISTICAL_SPECS.items():
        try:
            start = time.time()
            fitted = fit_statistical_model(y_train, spec)
            train_time = time.time() - start
            start = time.time()
            prediction = np.maximum(np.asarray(fitted.forecast(steps=len(y_test))), 0)
            prediction_time = time.time() - start
            rows.append(
                evaluate_predictions(
                    name,
                    y_test,
                    prediction,
                    train_time=train_time,
                    prediction_time=prediction_time,
                )
            )
            predictions[name] = prediction
        except Exception as exc:
            print(f"{name} ignoré: {exc}")
    return rows, predictions


def forecast_statistical(series, model_name: str, horizon: int):
    spec = STATISTICAL_SPECS[model_name]
    fitted = fit_statistical_model(series, spec)
    return np.maximum(np.asarray(fitted.forecast(steps=horizon)), 0)
