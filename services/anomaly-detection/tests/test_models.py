import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_anomaly_model_fields():
    try:
        from models import Anomaly
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Models import failed: {exc}")

    a = Anomaly(
        machine_id="CNC-001",
        metric="spindle.temperature_c",
        value=75.0,
        severity="high",
        detector="rule",
        reason="temp high",
    )
    assert a.machine_id == "CNC-001"
