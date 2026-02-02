import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_machine_model():
    try:
        from models import Machine
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Models import failed: {exc}")

    m = Machine(id="CNC-001", name="VMC-1", location="Plant A")
    assert m.id == "CNC-001"
