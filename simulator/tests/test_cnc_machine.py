import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_generate_telemetry_schema():
    try:
        from cnc_machine import CNCMachine
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"CNCMachine import failed: {exc}")

    cnc = CNCMachine(machine_id="CNC-001")
    telemetry = cnc.generate_telemetry()
    assert telemetry.machine_id == "CNC-001"
    assert 0 <= telemetry.spindle.rpm <= 24000
    assert 0 <= telemetry.tool.wear_percent <= 100
