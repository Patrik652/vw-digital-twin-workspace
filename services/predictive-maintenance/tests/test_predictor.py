import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_rul_decreases_with_wear():
    try:
        from predictor import predict_tool_rul
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Predictor import failed: {exc}")

    low = predict_tool_rul(wear_percent=10, runtime_minutes=50, cutting_speed_m_min=150)
    high = predict_tool_rul(wear_percent=80, runtime_minutes=50, cutting_speed_m_min=150)
    assert high.minutes_remaining < low.minutes_remaining
