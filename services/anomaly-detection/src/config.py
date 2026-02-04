"""Configuration for anomaly detection service."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class DetectorConfig:
    """Detector configuration values."""

    window_size: int = int(os.getenv("ANOMALY_WINDOW_SIZE", "30"))
    zscore_threshold: float = float(os.getenv("ANOMALY_ZSCORE_THRESHOLD", "3.0"))
    iforest_contamination: float = float(
        os.getenv("ANOMALY_IFOREST_CONTAMINATION", "0.02")
    )
    rule_temp_high_c: float = float(os.getenv("RULE_SPINDLE_TEMP_HIGH", "70"))
    rule_tool_wear_high: float = float(os.getenv("RULE_TOOL_WEAR_HIGH", "80"))
    rule_vibration_high: float = float(os.getenv("RULE_VIBRATION_HIGH", "5"))
    rule_coolant_low: float = float(os.getenv("RULE_COOLANT_FLOW_LOW", "2"))
    rule_min_rpm_running: float = float(os.getenv("RULE_MIN_RPM_RUNNING", "500"))
