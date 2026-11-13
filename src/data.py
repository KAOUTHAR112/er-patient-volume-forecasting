from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .config import DATE_COLUMN_CANDIDATES, TARGET

SENSITIVE_COLUMNS = {
    "Patient Id",
    "Patient First Inital",
    "Patient First Initial",
    "Patient Last Name",
    "Patient Name",
    "First Name",
    "Last Name",
}


def find_date_column(df: pd.DataFrame, candidates: Iterable[str] = DATE_COLUMN_CANDIDATES) -> str:
    """Return the first supported date column."""
    for column in candidates:
        if column in df.columns:
            return column
    raise ValueError(
        "Aucune colonne de date reconnue. Colonnes disponibles: "
        f"{list(df.columns)}"
    )


def _normalise_daily_frame(df: pd.DataFrame) -> pd.DataFrame:
    daily = df.copy()
    daily["Date"] = pd.to_datetime(daily["Date"], errors="coerce")
    daily[TARGET] = pd.to_numeric(daily[TARGET], errors="coerce")
    daily = daily.dropna(subset=["Date", TARGET]).sort_values("Date")
    daily["Date"] = daily["Date"].dt.floor("D")
    daily = daily.groupby("Date", as_index=False)[TARGET].sum()
    return _complete_date_index(daily)


def _complete_date_index(daily: pd.DataFrame) -> pd.DataFrame:
    if daily.empty:
        raise ValueError("Le jeu de données ne contient aucune date exploitable.")
    full_dates = pd.date_range(daily["Date"].min(), daily["Date"].max(), freq="D")
    result = (
        daily.set_index("Date")
        .reindex(full_dates)
        .rename_axis("Date")
        .reset_index()
    )
    result[TARGET] = result[TARGET].fillna(0).round().astype(int)
    return result[["Date", TARGET]]


def prepare_daily_volume(input_path: str | Path) -> pd.DataFrame:
    """Load a raw admissions CSV or an already aggregated daily CSV.

    The returned frame contains only ``Date`` and ``patients``. Individual-level
    identifiers and clinical attributes are never propagated to model outputs.
    """
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {path}")

    df = pd.read_csv(path)
    if {"Date", TARGET}.issubset(df.columns):
        return _normalise_daily_frame(df[["Date", TARGET]])

    date_column = find_date_column(df)
    dates = pd.to_datetime(df[date_column], dayfirst=True, errors="coerce")
    valid = pd.DataFrame({"Date": dates}).dropna()
    valid["Date"] = valid["Date"].dt.floor("D")
    daily = valid.groupby("Date").size().reset_index(name=TARGET)
    return _complete_date_index(daily)


def save_daily_volume(daily: pd.DataFrame, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    daily[["Date", TARGET]].to_csv(output, index=False)
    return output
