import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_power_calculation():
    try:
        from spindle import Spindle
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Spindle import failed: {exc}")

    spindle = Spindle()
    kw = spindle.power_kw(rpm=12000, torque_nm=10)
    assert 10.0 < kw < 15.0


def test_vibration_increases_with_wear():
    try:
        from spindle import Spindle
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Spindle import failed: {exc}")

    spindle = Spindle()
    low = spindle.vibration_mm_s(wear_percent=10)
    high = spindle.vibration_mm_s(wear_percent=80)
    assert high > low


def test_thermal_expansion_reasonable():
    try:
        from spindle import Spindle
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Spindle import failed: {exc}")

    spindle = Spindle()
    delta = spindle.thermal_expansion_mm(length_mm=100.0, delta_temp_c=20.0)
    assert 0.02 <= delta <= 0.03
