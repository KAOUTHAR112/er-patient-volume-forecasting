from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_STATE = 42
OUTPUT = Path("data/demo/daily_er_volume_demo.csv")

rng = np.random.default_rng(RANDOM_STATE)
dates = pd.date_range("2024-01-01", periods=365, freq="D")
weekday = dates.weekday
weekly_effect = np.where(weekday >= 5, -1.2, 0.6)
annual_effect = 1.5 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
noise = rng.normal(0, 2.2, len(dates))
patients = np.maximum(np.rint(16 + weekly_effect + annual_effect + noise), 1).astype(int)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame({"Date": dates, "patients": patients}).to_csv(OUTPUT, index=False)
print(f"Synthetic demo data saved to {OUTPUT}")
print("These values are artificial and must not be presented as hospital results.")
