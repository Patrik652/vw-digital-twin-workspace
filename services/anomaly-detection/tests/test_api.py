import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_health():
    try:
        from main import app
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"API import failed: {exc}")

    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
