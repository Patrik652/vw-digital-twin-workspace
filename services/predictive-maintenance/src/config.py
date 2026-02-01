"""Configuration for predictive maintenance service."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class PredictorConfig:
    """Predictor configuration values."""

    safety_factor: float = float(os.getenv("PM_SAFETY_FACTOR", "0.9"))
    max_tool_life_minutes: float = float(os.getenv("PM_MAX_TOOL_LIFE_MIN", "300"))
    spindle_temp_limit_c: float = float(os.getenv("PM_SPINDLE_TEMP_LIMIT", "80"))
    spindle_vibration_limit: float = float(os.getenv("PM_SPINDLE_VIBRATION_LIMIT", "6"))
