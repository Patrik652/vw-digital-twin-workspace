import asyncio

import pytest


def test_health():
    try:
        import main
    except Exception as exc:  # pragma: no cover - import safety
        pytest.fail(f"API import failed: {exc}")

    assert any(getattr(route, "path", "") == "/health" for route in main.app.routes)
    result = asyncio.run(main.health())
    assert result["status"] == "ok"


def test_alert_skips_without_webhook():
    from main import create_alert
    from models import AlertRequest

    request = AlertRequest(
        machine_id="CNC-001",
        severity="high",
        message="Temperature high",
        metric="spindle.temperature_c",
        value=88.0,
    )

    response = asyncio.run(create_alert(request))
    assert response.status == "skipped"
