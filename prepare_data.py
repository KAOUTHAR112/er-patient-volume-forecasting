from __future__ import annotations

import argparse

from src.data import prepare_daily_volume, save_daily_volume


def main():
    parser = argparse.ArgumentParser(
        description="Aggregate raw emergency-department admissions by day."
    )
    parser.add_argument("--input", required=True, help="Raw admissions CSV or daily CSV")
    parser.add_argument(
        "--output",
        default="data/processed/daily_er_volume.csv",
        help="Output aggregated CSV",
    )
    args = parser.parse_args()

    daily = prepare_daily_volume(args.input)
    output = save_daily_volume(daily, args.output)
    print(f"Saved {len(daily)} daily rows to {output}")
    print("Only Date and patients are retained; personal identifiers are excluded.")


if __name__ == "__main__":
    main()
