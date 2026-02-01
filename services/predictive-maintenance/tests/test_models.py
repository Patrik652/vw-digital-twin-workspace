import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_tool_rul_request_fields():
    try:
        from models import ToolRULRequest
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Models import failed: {exc}")

    req = ToolRULRequest(machine_id="CNC-001", wear_percent=50, runtime_minutes=120, cutting_speed_m_min=200)
    assert req.machine_id == "CNC-001"
