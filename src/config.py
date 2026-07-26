from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RANDOM_STATE = 42
TARGET = "patients"
DATE_COLUMN_CANDIDATES = (
    "Patient Admission Date",
    "Admission Date",
    "DateTime",
    "datetime",
    "date",
    "Date",
)
TEST_RATIO = 0.20
SEASONAL_PERIOD = 7
FORECAST_HORIZON = 30
LAGS = (1, 2, 3, 7, 14, 21, 28)
ROLLING_WINDOWS = (3, 7, 14, 28)
