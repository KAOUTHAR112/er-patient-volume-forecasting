import pandas as pd

from src.data import prepare_daily_volume


def test_raw_patient_data_is_aggregated_without_identifiers(tmp_path):
    raw = pd.DataFrame(
        {
            "Patient Id": ["A", "B", "C"],
            "Patient Last Name": ["One", "Two", "Three"],
            "Patient Admission Date": [
                "01-01-2024 08:00",
                "01-01-2024 09:00",
                "03-01-2024 10:00",
            ],
        }
    )
    path = tmp_path / "raw.csv"
    raw.to_csv(path, index=False)

    daily = prepare_daily_volume(path)

    assert list(daily.columns) == ["Date", "patients"]
    assert daily["patients"].tolist() == [2, 0, 1]
