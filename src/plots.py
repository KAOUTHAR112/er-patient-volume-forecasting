from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def save_daily_series(daily: pd.DataFrame, output: str | Path) -> None:
    plt.figure(figsize=(14, 5))
    plt.plot(daily["Date"], daily["patients"])
    plt.title("Daily emergency-department patient volume")
    plt.xlabel("Date")
    plt.ylabel("Patients")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def save_model_comparison(results: pd.DataFrame, output: str | Path, top_n: int = 15) -> None:
    plot_df = results.nsmallest(top_n, "MAE").sort_values("MAE", ascending=True)
    plt.figure(figsize=(11, 7))
    plt.barh(plot_df["model"], plot_df["MAE"])
    plt.title(f"Top {len(plot_df)} models by MAE")
    plt.xlabel("MAE")
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def save_predictions(dates, y_true, y_pred, model_name: str, output: str | Path) -> None:
    plt.figure(figsize=(14, 5))
    plt.plot(dates, y_true, label="Actual")
    plt.plot(dates, y_pred, label="Predicted")
    plt.title(f"Test-set predictions — {model_name}")
    plt.xlabel("Date")
    plt.ylabel("Patients")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def save_residuals(dates, y_true, y_pred, model_name: str, output: str | Path) -> None:
    residuals = np.asarray(y_true) - np.asarray(y_pred)
    plt.figure(figsize=(14, 4))
    plt.plot(dates, residuals)
    plt.axhline(0, linestyle="--")
    plt.title(f"Residuals — {model_name}")
    plt.xlabel("Date")
    plt.ylabel("Residual")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()


def save_future_forecast(history, future, model_name: str, output: str | Path) -> None:
    plt.figure(figsize=(14, 5))
    plt.plot(history["Date"].tail(90), history["patients"].tail(90), label="Historical")
    plt.plot(future["Date"], future["forecast_patients"], label="Forecast")
    plt.title(f"Future forecast — {model_name}")
    plt.xlabel("Date")
    plt.ylabel("Patients")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output, dpi=160)
    plt.close()
