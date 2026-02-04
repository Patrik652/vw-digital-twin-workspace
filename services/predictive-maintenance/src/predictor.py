"""Prediction logic for predictive maintenance."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from config import PredictorConfig
from models import (
    MaintenancePrediction,
    MaintenanceScheduleResponse,
    SpindleHealthResponse,
    ToolRULResponse,
)


def predict_tool_rul(
    wear_percent: float,
    runtime_minutes: float,
    cutting_speed_m_min: float,
    machine_id: str = "",
    config: PredictorConfig | None = None,
) -> ToolRULResponse:
    cfg = config or PredictorConfig()
    wear_factor = max(0.0, min(100.0, wear_percent)) / 100.0
    speed_factor = max(0.0, cutting_speed_m_min) / 300.0
    base_life = cfg.max_tool_life_minutes * cfg.safety_factor
    consumed = (
        (runtime_minutes * 0.6) + (wear_factor * base_life) + (speed_factor * 20.0)
    )
    remaining = max(0.0, base_life - consumed)
    confidence = max(0.3, 1.0 - wear_factor)
    return ToolRULResponse(
        machine_id=machine_id, minutes_remaining=remaining, confidence=confidence
    )


def predict_spindle_health(
    machine_id: str,
    vibration_mm_s: float,
    temperature_c: float,
    trend_slope: float,
    config: PredictorConfig | None = None,
) -> SpindleHealthResponse:
    cfg = config or PredictorConfig()
    vib_ratio = min(1.0, vibration_mm_s / cfg.spindle_vibration_limit)
    temp_ratio = min(1.0, temperature_c / cfg.spindle_temp_limit_c)
    trend_penalty = min(1.0, max(0.0, trend_slope) * 0.1)
    health_score = max(
        0.0, 100.0 * (1.0 - (0.5 * vib_ratio + 0.4 * temp_ratio + 0.1 * trend_penalty))
    )
    days_to_maintenance = max(0.0, health_score / 5.0)
    return SpindleHealthResponse(
        machine_id=machine_id,
        health_score=health_score,
        days_to_maintenance=days_to_maintenance,
    )


def build_maintenance_schedule(
    machine_id: str,
    tool_rul: ToolRULResponse,
    spindle_health: SpindleHealthResponse,
) -> MaintenanceScheduleResponse:
    now = datetime.now(timezone.utc)
    predictions = []

    tool_urgency = (
        "high"
        if tool_rul.minutes_remaining < 30
        else "medium" if tool_rul.minutes_remaining < 120 else "low"
    )
    predictions.append(
        MaintenancePrediction(
            component="Tool",
            action="Replace",
            urgency=tool_urgency,
            estimated_time=(
                now + timedelta(minutes=tool_rul.minutes_remaining)
            ).isoformat(),
            confidence=tool_rul.confidence,
        )
    )

    spindle_urgency = (
        "high"
        if spindle_health.health_score < 40
        else "medium" if spindle_health.health_score < 70 else "low"
    )
    predictions.append(
        MaintenancePrediction(
            component="Spindle Bearings",
            action="Inspect",
            urgency=spindle_urgency,
            estimated_time=(
                now + timedelta(days=spindle_health.days_to_maintenance)
            ).isoformat(),
            confidence=0.7,
        )
    )

    return MaintenanceScheduleResponse(machine_id=machine_id, predictions=predictions)
