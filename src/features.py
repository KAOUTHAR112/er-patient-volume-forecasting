from __future__ import annotations

import numpy as np
import pandas as pd

from .config import LAGS, ROLLING_WINDOWS, TARGET


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["day"] = result["Date"].dt.day
    result["month"] = result["Date"].dt.month
    result["year"] = result["Date"].dt.year
    result["weekday"] = result["Date"].dt.weekday
    result["weekofyear"] = result["Date"].dt.isocalendar().week.astype(int)
    result["quarter"] = result["Date"].dt.quarter
    result["is_weekend"] = result["weekday"].isin([5, 6]).astype(int)
    result["dayofyear"] = result["Date"].dt.dayofyear

    result["weekday_sin"] = np.sin(2 * np.pi * result["weekday"] / 7)
    result["weekday_cos"] = np.cos(2 * np.pi * result["weekday"] / 7)
    result["month_sin"] = np.sin(2 * np.pi * result["month"] / 12)
    result["month_cos"] = np.cos(2 * np.pi * result["month"] / 12)
    result["dayofyear_sin"] = np.sin(2 * np.pi * result["dayofyear"] / 365.25)
    result["dayofyear_cos"] = np.cos(2 * np.pi * result["dayofyear"] / 365.25)
    return result


def add_lag_rolling_features(df: pd.DataFrame, target: str = TARGET) -> pd.DataFrame:
    """Create features using past target values only."""
    result = df.copy()
    for lag in LAGS:
        result[f"lag_{lag}"] = result[target].shift(lag)

    shifted = result[target].shift(1)
    for window in ROLLING_WINDOWS:
        rolling = shifted.rolling(window)
        result[f"rolling_mean_{window}"] = rolling.mean()
        result[f"rolling_std_{window}"] = rolling.std()
        result[f"rolling_min_{window}"] = rolling.min()
        result[f"rolling_max_{window}"] = rolling.max()

    result["diff_1"] = result[target].shift(1) - result[target].shift(2)
    result["diff_7"] = result[target].shift(7) - result[target].shift(14)
    return result


def add_morocco_holiday_feature(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    try:
        import holidays

        years = sorted(result["Date"].dt.year.unique())
        calendar = holidays.country_holidays("MA", years=years)
        result["is_holiday"] = result["Date"].dt.date.isin(calendar).astype(int)
    except Exception:
        result["is_holiday"] = 0
    return result


def build_feature_frame(daily: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    result = daily.copy()
    result["Date"] = pd.to_datetime(result["Date"])
    result = add_calendar_features(result)
    result = add_lag_rolling_features(result)
    result = add_morocco_holiday_feature(result)
    feature_columns = [c for c in result.columns if c not in {"Date", TARGET}]
    # Drop rows only when engineered predictors are incomplete. This keeps a
    # future row whose target is unknown during recursive forecasting.
    result = result.dropna(subset=feature_columns).reset_index(drop=True)
    return result, feature_columns
