import asyncio
from datetime import datetime, timezone
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

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


def test_ingest_telemetry_dispatches_alert_for_overheat(monkeypatch):
    import main
    from models import Telemetry

    sent = {}

    async def fake_send_alert(**payload):
        sent.update(payload)
        return {"status": "sent"}

    monkeypatch.setattr(main.service_client, "send_alert", fake_send_alert)

    telemetry = Telemetry(
        timestamp=datetime.now(timezone.utc),
        machine_id="TEST-002",
        data={"spindle": {"temperature_c": 95.0}},
    )
    result = asyncio.run(main.ingest_telemetry("TEST-002", telemetry, x_api_key="dev-key"))

    assert result.status == "success"
    assert sent["machine_id"] == "TEST-002"
    assert sent["severity"] == "critical"
    assert sent["metric"] == "spindle.temperature_c"


def test_aggregate_endpoint_uses_data_aggregator(monkeypatch):
    import main
    from models import AggregateRequest, Telemetry

    telemetry = Telemetry(
        timestamp=datetime.now(timezone.utc),
        machine_id="TEST-003",
        data={"spindle": {"temperature_c": 45.0}},
    )
    asyncio.run(main.ingest_telemetry("TEST-003", telemetry, x_api_key="dev-key"))

    async def fake_aggregate(*, machine_id, points, metric, windows):
        return {"buckets": [{"machine_id": machine_id, "count": len(points), "window": windows[0]}]}

    monkeypatch.setattr(main.service_client, "aggregate", fake_aggregate)

    response = asyncio.run(main.aggregate_machine("TEST-003", AggregateRequest(windows=["1min"]), x_api_key="dev-key"))
    assert response.status == "success"
    assert response.data["buckets"][0]["machine_id"] == "TEST-003"
    assert response.data["buckets"][0]["count"] == 1


def test_alert_endpoint_accepts_warning_alias(monkeypatch):
    import main
    from models import AlertRequest

    sent = {}

    async def fake_send_alert(**payload):
        sent.update(payload)
        return {"status": "sent"}

    monkeypatch.setattr(main.service_client, "send_alert", fake_send_alert)

    req = AlertRequest(severity="warning", message="Legacy warning alert")
    response = asyncio.run(main.send_alert("CNC-004", req, x_api_key="dev-key"))

    assert response.status == "success"
    assert sent["machine_id"] == "CNC-004"
    assert sent["severity"] == "medium"


def test_aggregate_accepts_window_minutes_legacy(monkeypatch):
    import main
    from models import AggregateRequest, Telemetry

    telemetry = Telemetry(
        timestamp=datetime.now(timezone.utc),
        machine_id="TEST-005",
        data={"spindle": {"temperature_c": 41.0}},
    )
    asyncio.run(main.ingest_telemetry("TEST-005", telemetry, x_api_key="dev-key"))

    captured = {}

    async def fake_aggregate(*, machine_id, points, metric, windows):
        captured["machine_id"] = machine_id
        captured["windows"] = windows
        return {"buckets": []}

    monkeypatch.setattr(main.service_client, "aggregate", fake_aggregate)
    response = asyncio.run(
        main.aggregate_machine("TEST-005", AggregateRequest(window_minutes=5), x_api_key="dev-key")
    )

    assert response.status == "success"
    assert captured["machine_id"] == "TEST-005"
    assert captured["windows"] == ["5min"]


def test_aggregate_rejects_unsupported_window_minutes():
    from models import AggregateRequest

    with pytest.raises(ValidationError):
        AggregateRequest(window_minutes=7)
