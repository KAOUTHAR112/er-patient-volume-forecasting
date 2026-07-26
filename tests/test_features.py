import pandas as pd

from src.features import build_feature_frame


def test_lag_and_rolling_features_use_past_values_only():
    daily = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=50, freq="D"),
            "patients": range(1, 51),
        }
    )
    model_df, _ = build_feature_frame(daily)
    first = model_df.iloc[0]
    source_index = daily.index[daily["Date"] == first["Date"]][0]

    assert first["lag_1"] == daily.loc[source_index - 1, "patients"]
    expected_mean = daily.loc[source_index - 7 : source_index - 1, "patients"].mean()
    assert first["rolling_mean_7"] == expected_mean


def test_future_row_is_kept_when_target_is_unknown():
    daily = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=50, freq="D"),
            "patients": list(range(1, 50)) + [float("nan")],
        }
    )
    model_df, _ = build_feature_frame(daily)
    assert model_df.iloc[-1]["Date"] == daily.iloc[-1]["Date"]
    assert pd.isna(model_df.iloc[-1]["patients"])
