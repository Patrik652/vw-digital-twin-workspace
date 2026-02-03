import asyncio
from datetime import datetime, timezone
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_health():
    try:
        import main
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"API import failed: {exc}")

    assert any(getattr(route, "path", "") == "/health" for route in main.app.routes)
    result = asyncio.run(main.health())
    assert result["status"] == "ok"


def test_ingest_telemetry_stores_latest():
    try:
        import main
        from models import Telemetry
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"API import failed: {exc}")

    telemetry = Telemetry(timestamp=datetime.now(timezone.utc), machine_id="TEST-001", data={"rpm": 12000})
    result = asyncio.run(main.ingest_telemetry("TEST-001", telemetry, x_api_key="dev-key"))

    assert result.status == "success"
    latest = main.store.latest_telemetry("TEST-001")
    assert latest is not None
    assert latest.machine_id == "TEST-001"
