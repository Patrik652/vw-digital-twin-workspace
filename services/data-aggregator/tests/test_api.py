import asyncio
from datetime import datetime, timezone

import pytest


def test_health():
    try:
        import main
    except Exception as exc:  # pragma: no cover - import safety
        pytest.fail(f"API import failed: {exc}")

    assert any(getattr(route, "path", "") == "/health" for route in main.app.routes)
    result = asyncio.run(main.health())
    assert result["status"] == "ok"


def test_aggregate_rollup():
    from main import aggregate
    from models import AggregateRequest, MetricPoint

    points = [
        MetricPoint(
            machine_id="CNC-001",
            metric="spindle.temperature_c",
            timestamp=datetime(2026, 2, 4, 10, 0, 5, tzinfo=timezone.utc),
            value=40.0,
        ),
        MetricPoint(
            machine_id="CNC-001",
            metric="spindle.temperature_c",
            timestamp=datetime(2026, 2, 4, 10, 0, 50, tzinfo=timezone.utc),
            value=50.0,
        ),
    ]
    req = AggregateRequest(points=points, windows=["1min"])

    response = asyncio.run(aggregate(req))
    assert len(response.buckets) == 1

    bucket = response.buckets[0]
    assert bucket.count == 2
    assert bucket.min_value == 40.0
    assert bucket.max_value == 50.0
    assert bucket.avg_value == 45.0
