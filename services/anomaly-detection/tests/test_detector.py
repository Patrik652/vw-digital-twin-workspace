import pytest


def test_zscore_detection():
    try:
        from config import DetectorConfig
        from detector import Detector
    except Exception as exc:  # pragma: no cover - import safety
        pytest.fail(f"Detector import failed: {exc}")

    det = Detector(config=DetectorConfig(window_size=10, zscore_threshold=2.0))

    for _ in range(9):
        assert det.detect_zscore("spindle.temperature_c", 40.0, "CNC-001") == []

    anomalies = det.detect_zscore("spindle.temperature_c", 100.0, "CNC-001")

    assert anomalies
    assert anomalies[0].detector == "zscore"


def test_rule_based_detection():
    from detector import Detector

    det = Detector()
    telemetry = {
        "machine_id": "CNC-001",
        "spindle": {
            "temperature_c": 75,
            "rpm": 12000,
            "vibration_mm_s": 7,
        },
        "tool": {"wear_percent": 85},
        "coolant": {"flow_rate_lpm": 1.0},
    }

    anomalies = det.detect_rule_based(telemetry)

    assert anomalies
    metrics = {anomaly.metric for anomaly in anomalies}
    assert "spindle.temperature_c" in metrics
    assert "tool.wear_percent" in metrics
