from __future__ import annotations

import argparse

from src.experiment import run_experiment


def main():
    parser = argparse.ArgumentParser(
        description="Run ER patient-volume forecasting experiments."
    )
    parser.add_argument(
        "--data",
        default="data/processed/daily_er_volume.csv",
        help="Raw or daily aggregated CSV",
    )
    parser.add_argument("--output", default="results/latest")
    parser.add_argument("--figures", default="figures/latest")
    parser.add_argument("--horizon", type=int, default=30)
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Use the compact model set for faster execution",
    )
    parser.add_argument(
        "--optional-models",
        action="store_true",
        help="Include XGBoost, LightGBM and CatBoost when installed",
    )
    args = parser.parse_args()

    artifacts = run_experiment(
        data_path=args.data,
        output_dir=args.output,
        figures_dir=args.figures,
        horizon=args.horizon,
        include_extended=not args.fast,
        include_optional=args.optional_models,
    )
    print("Best model:", artifacts["best_model"])
    print(artifacts["results"].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
