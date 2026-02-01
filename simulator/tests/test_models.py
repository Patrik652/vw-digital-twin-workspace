import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_telemetry_schema_defaults():
    try:
        from models import Telemetry
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Telemetry import failed: {exc}")

    t = Telemetry.example()
    assert 0 <= t.spindle.rpm <= 24000
    assert 0 <= t.tool.wear_percent <= 100
    assert t.machine_id
