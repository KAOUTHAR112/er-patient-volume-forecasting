from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

from .config import FORECAST_HORIZON, RANDOM_STATE, TARGET, TEST_RATIO
from .data import prepare_daily_volume
from .features import build_feature_frame
from .metrics import evaluate_predictions
from .models import get_ml_models
from .plots import (
    save_daily_series,
    save_future_forecast,
    save_model_comparison,
    save_predictions,
    save_residuals,
)
from .statistical import STATISTICAL_SPECS, evaluate_statistical_models, forecast_statistical


def _baseline_predictions(x_test, y_train):
    return {
        "Naive Mean": np.repeat(y_train.mean(), len(x_test)),
        "Naive Last Value": np.repeat(y_train.iloc[-1], len(x_test)),
        "Seasonal Naive Lag-7": x_test["lag_7"].to_numpy(),
        "Moving Average 7": x_test["rolling_mean_7"].to_numpy(),
    }


def _recursive_ml_forecast(model, history, feature_columns, horizon):
    current = history[["Date", TARGET]].copy()
    rows = []
    for _ in range(horizon):
        next_date = current["Date"].max() + pd.Timedelta(days=1)
        candidate = pd.concat(
            [current, pd.DataFrame({"Date": [next_date], TARGET: [np.nan]})],
            ignore_index=True,
        )
        features, _ = build_feature_frame(candidate)
        next_x = features.iloc[[-1]][feature_columns]
        prediction = float(max(model.predict(next_x)[0], 0))
        rows.append({"Date": next_date, "forecast_patients": prediction})
        current = pd.concat(
            [current, pd.DataFrame({"Date": [next_date], TARGET: [prediction]})],
            ignore_index=True,
        )
    return pd.DataFrame(rows)


def time_series_cv_summary(model_df, feature_columns, models, n_splits=5):
    splitter = TimeSeriesSplit(n_splits=n_splits)
    rows = []
    for model_name, model in models.items():
        fold_rows = []
        for fold, (train_idx, val_idx) in enumerate(splitter.split(model_df), start=1):
            x_train = model_df.iloc[train_idx][feature_columns]
            y_train = model_df.iloc[train_idx][TARGET]
            x_val = model_df.iloc[val_idx][feature_columns]
            y_val = model_df.iloc[val_idx][TARGET]
            model.fit(x_train, y_train)
            prediction = np.maximum(model.predict(x_val), 0)
            metrics = evaluate_predictions(f"fold_{fold}", y_val, prediction)
            fold_rows.append(metrics)
        fold_df = pd.DataFrame(fold_rows)
        rows.append(
            {
                "model": model_name,
                "CV_MAE_mean": fold_df["MAE"].mean(),
                "CV_MAE_std": fold_df["MAE"].std(),
                "CV_RMSE_mean": fold_df["RMSE"].mean(),
                "CV_RMSE_std": fold_df["RMSE"].std(),
                "CV_Operational_Accuracy_±2_mean": fold_df[
                    "Operational_Accuracy_±2_%"
                ].mean(),
            }
        )
    return pd.DataFrame(rows).sort_values("CV_MAE_mean")


def run_experiment(
    data_path,
    output_dir="results/latest",
    figures_dir="figures/latest",
    test_ratio=TEST_RATIO,
    horizon=FORECAST_HORIZON,
    include_extended=True,
    include_optional=False,
):
    output_dir = Path(output_dir)
    figures_dir = Path(figures_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    daily = prepare_daily_volume(data_path)
    model_df, feature_columns = build_feature_frame(daily)
    split_index = int(len(model_df) * (1 - test_ratio))
    if split_index <= 0 or split_index >= len(model_df):
        raise ValueError("Le jeu de données est trop court pour le split demandé.")

    train_df = model_df.iloc[:split_index].copy()
    test_df = model_df.iloc[split_index:].copy()
    x_train, y_train = train_df[feature_columns], train_df[TARGET]
    x_test, y_test = test_df[feature_columns], test_df[TARGET]
    y_train_ts = train_df.set_index("Date")[TARGET]

    rows, predictions, fitted_ml = [], {}, {}

    for name, prediction in _baseline_predictions(x_test, y_train).items():
        rows.append(evaluate_predictions(name, y_test, prediction))
        predictions[name] = np.asarray(prediction)

    statistical_rows, statistical_predictions = evaluate_statistical_models(y_train_ts, y_test)
    rows.extend(statistical_rows)
    predictions.update(statistical_predictions)

    models = get_ml_models(
        include_extended=include_extended,
        include_optional=include_optional,
    )
    for name, model in models.items():
        try:
            start = time.time()
            model.fit(x_train, y_train)
            train_time = time.time() - start
            start = time.time()
            prediction = np.maximum(model.predict(x_test), 0)
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
            predictions[name] = np.asarray(prediction)
            fitted_ml[name] = model
        except Exception as exc:
            print(f"{name} ignoré: {exc}")

    results = pd.DataFrame(rows).sort_values("MAE").reset_index(drop=True)
    results.to_csv(output_dir / "model_comparison.csv", index=False)

    best_name = str(results.iloc[0]["model"])
    best_prediction = predictions[best_name]
    y_test_values = y_test.to_numpy()[-len(best_prediction):]
    test_dates = test_df["Date"].to_numpy()[-len(best_prediction):]

    save_daily_series(daily, figures_dir / "daily_volume.png")
    save_model_comparison(results, figures_dir / "model_comparison_mae.png")
    save_predictions(
        test_dates,
        y_test_values,
        best_prediction,
        best_name,
        figures_dir / "best_model_predictions.png",
    )
    save_residuals(
        test_dates,
        y_test_values,
        best_prediction,
        best_name,
        figures_dir / "best_model_residuals.png",
    )

    if best_name in STATISTICAL_SPECS:
        forecast_values = forecast_statistical(
            daily.set_index("Date")[TARGET], best_name, horizon
        )
        future_dates = pd.date_range(
            daily["Date"].max() + pd.Timedelta(days=1), periods=horizon, freq="D"
        )
        future = pd.DataFrame(
            {"Date": future_dates, "forecast_patients": forecast_values}
        )
    elif best_name in fitted_ml:
        full_model = get_ml_models(
            include_extended=include_extended,
            include_optional=include_optional,
        )[best_name]
        full_model.fit(model_df[feature_columns], model_df[TARGET])
        future = _recursive_ml_forecast(
            full_model, daily, feature_columns, horizon
        )
    else:
        fallback = get_ml_models(include_extended=False)["Random Forest"]
        fallback.fit(model_df[feature_columns], model_df[TARGET])
        future = _recursive_ml_forecast(fallback, daily, feature_columns, horizon)
        best_name = f"{best_name} (forecast fallback: Random Forest)"

    future.to_csv(output_dir / "future_forecast.csv", index=False)
    save_future_forecast(
        daily, future, best_name, figures_dir / "future_forecast.png"
    )

    cv_candidates = {
        name: get_ml_models(include_extended=False)[name]
        for name in ["Random Forest", "Extra Trees", "Gradient Boosting"]
    }
    cv_summary = time_series_cv_summary(
        model_df, feature_columns, cv_candidates, n_splits=5
    )
    cv_summary.to_csv(output_dir / "timeseries_cv_summary.csv", index=False)

    metadata = {
        "random_state": RANDOM_STATE,
        "rows_raw_daily": int(len(daily)),
        "rows_model": int(len(model_df)),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "test_ratio": test_ratio,
        "feature_count": len(feature_columns),
        "best_model": best_name,
        "forecast_horizon": horizon,
        "excluded_model_families": ["LSTM", "Holt-Winters", "ETS"],
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return {
        "daily": daily,
        "model_frame": model_df,
        "feature_columns": feature_columns,
        "results": results,
        "cv_summary": cv_summary,
        "future_forecast": future,
        "best_model": best_name,
        "test_dates": test_dates,
        "y_test": y_test_values,
        "best_prediction": best_prediction,
    }
