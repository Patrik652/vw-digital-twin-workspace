import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_failure_injection_tracks_active():
    try:
        from failure_modes import FailureManager, ToolWearAccelerated
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Failure modes import failed: {exc}")

    manager = FailureManager()
    failure = ToolWearAccelerated(multiplier=3.0)
    manager.inject(failure)
    assert len(manager.active_failures()) == 1
