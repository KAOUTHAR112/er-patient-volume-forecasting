from src.models import get_ml_models
from src.statistical import STATISTICAL_SPECS


def test_excluded_model_families_are_absent():
    names = list(get_ml_models(include_extended=True).keys()) + list(STATISTICAL_SPECS.keys())
    joined = " ".join(names).lower()
    assert "lstm" not in joined
    assert "holt" not in joined
    assert "ets" not in joined
    assert "exponential smoothing" not in joined
