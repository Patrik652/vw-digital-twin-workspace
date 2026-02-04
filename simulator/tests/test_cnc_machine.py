import pytest


def test_spindle_rpm_in_range():
    try:
        from cnc_machine import CNCMachine
    except Exception as exc:  # pragma: no cover - import safety
        pytest.fail(f"CNCMachine import failed: {exc}")

    cnc = CNCMachine(machine_id="CNC-001")
    cnc.start()
    telemetry = cnc.generate_telemetry()

    assert 0 <= telemetry.spindle.rpm <= 24000


def test_tool_wear_increases(monkeypatch):
    from cnc_machine import CNCMachine

    cnc = CNCMachine(machine_id="CNC-001")
    cnc.start()

    monkeypatch.setattr(cnc, "_elapsed_since_last_cycle", lambda: 120.0)

    first = cnc.generate_telemetry().tool.wear_percent
    second = cnc.generate_telemetry().tool.wear_percent

    assert second > first


def test_telemetry_schema():
    from cnc_machine import CNCMachine

    cnc = CNCMachine(machine_id="CNC-001")
    telemetry = cnc.generate_telemetry().model_dump()

    assert telemetry["machine_id"] == "CNC-001"
    assert isinstance(telemetry["timestamp"], object)
    assert {"rpm", "temperature_c", "vibration_mm_s"}.issubset(
        telemetry["spindle"].keys()
    )
    assert {"wear_percent", "runtime_minutes"}.issubset(telemetry["tool"].keys())
    assert {"mode", "cycle_time_s"}.issubset(telemetry["status"].keys())
