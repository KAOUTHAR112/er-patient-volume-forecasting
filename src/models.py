from __future__ import annotations

from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNet, Lasso, LinearRegression, Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

from .config import RANDOM_STATE


def _scaled(model):
    return Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("model", model),
        ]
    )


def get_ml_models(include_extended: bool = True, include_optional: bool = False) -> dict:
    """Return classical ML regressors only—no LSTM and no ETS/Holt-Winters."""
    models = {
        "Linear Regression": _scaled(LinearRegression()),
        "Ridge": _scaled(Ridge(alpha=1.0)),
        "Random Forest": RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Extra Trees": ExtraTreesRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            n_estimators=250,
            learning_rate=0.03,
            max_depth=3,
            random_state=RANDOM_STATE,
        ),
    }

    if include_extended:
        models.update(
            {
                "Lasso": _scaled(Lasso(alpha=0.01, max_iter=10_000, random_state=RANDOM_STATE)),
                "ElasticNet": _scaled(
                    ElasticNet(
                        alpha=0.01,
                        l1_ratio=0.5,
                        max_iter=10_000,
                        random_state=RANDOM_STATE,
                    )
                ),
                "KNN": _scaled(KNeighborsRegressor(n_neighbors=7)),
                "SVR RBF": _scaled(SVR(kernel="rbf", C=10, gamma="scale", epsilon=0.1)),
                "HistGradientBoosting": HistGradientBoostingRegressor(
                    max_iter=300,
                    learning_rate=0.03,
                    max_leaf_nodes=31,
                    random_state=RANDOM_STATE,
                ),
                "MLP Regressor": _scaled(
                    MLPRegressor(
                        hidden_layer_sizes=(64, 32),
                        alpha=0.001,
                        learning_rate_init=0.001,
                        max_iter=800,
                        random_state=RANDOM_STATE,
                    )
                ),
            }
        )

    if include_optional:
        try:
            from xgboost import XGBRegressor

            models["XGBoost"] = XGBRegressor(
                n_estimators=500,
                learning_rate=0.03,
                max_depth=3,
                subsample=0.8,
                colsample_bytree=0.8,
                objective="reg:squarederror",
                random_state=RANDOM_STATE,
                n_jobs=-1,
            )
        except ImportError:
            pass

        try:
            from lightgbm import LGBMRegressor

            models["LightGBM"] = LGBMRegressor(
                n_estimators=500,
                learning_rate=0.03,
                random_state=RANDOM_STATE,
                n_jobs=-1,
                verbosity=-1,
            )
        except ImportError:
            pass

        try:
            from catboost import CatBoostRegressor

            models["CatBoost"] = CatBoostRegressor(
                iterations=500,
                learning_rate=0.03,
                depth=4,
                random_seed=RANDOM_STATE,
                verbose=False,
            )
        except ImportError:
            pass

    return models
