import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_rule_based_flags_overheat():
    try:
        from detector import Detector
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Detector import failed: {exc}")

    det = Detector()
    telemetry = {
        "machine_id": "CNC-001",
        "spindle": {"temperature_c": 75, "rpm": 12000, "vibration_mm_s": 0.5},
        "tool": {"wear_percent": 10},
        "coolant": {"flow_rate_lpm": 5},
    }
    anomalies = det.detect_rule_based(telemetry)
    assert anomalies
