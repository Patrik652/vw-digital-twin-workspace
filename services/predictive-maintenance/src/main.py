"""FastAPI application for predictive maintenance."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI

from models import (
    MaintenanceScheduleResponse,
    PredictionRecord,
    SpindleHealthRequest,
    SpindleHealthResponse,
    ToolRULRequest,
    ToolRULResponse,
)
from predictor import build_maintenance_schedule, predict_spindle_health, predict_tool_rul

app = FastAPI(title="Predictive Maintenance Service", version="0.1.0")

_recent_predictions: List[PredictionRecord] = []


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict:
    return {"status": "ready"}


@app.post("/predict/tool-rul")
async def predict_tool(req: ToolRULRequest) -> ToolRULResponse:
    result = predict_tool_rul(
        wear_percent=req.wear_percent,
        runtime_minutes=req.runtime_minutes,
        cutting_speed_m_min=req.cutting_speed_m_min,
        machine_id=req.machine_id,
    )
    _recent_predictions.append(PredictionRecord(machine_id=req.machine_id, result_type="tool_rul", payload=result.model_dump()))
    return result


@app.post("/predict/spindle-health")
async def predict_spindle(req: SpindleHealthRequest) -> SpindleHealthResponse:
    result = predict_spindle_health(
        machine_id=req.machine_id,
        vibration_mm_s=req.vibration_mm_s,
        temperature_c=req.temperature_c,
        trend_slope=req.trend_slope,
    )
    _recent_predictions.append(
        PredictionRecord(machine_id=req.machine_id, result_type="spindle_health", payload=result.model_dump())
    )
    return result


@app.post("/predict/maintenance-schedule")
async def predict_schedule(req: ToolRULRequest) -> MaintenanceScheduleResponse:
    tool_rul = predict_tool_rul(
        wear_percent=req.wear_percent,
        runtime_minutes=req.runtime_minutes,
        cutting_speed_m_min=req.cutting_speed_m_min,
        machine_id=req.machine_id,
    )
    spindle = predict_spindle_health(
        machine_id=req.machine_id,
        vibration_mm_s=1.0,
        temperature_c=40.0,
        trend_slope=0.0,
    )
    schedule = build_maintenance_schedule(req.machine_id, tool_rul, spindle)
    _recent_predictions.append(
        PredictionRecord(machine_id=req.machine_id, result_type="maintenance_schedule", payload=schedule.model_dump())
    )
    return schedule


@app.get("/predictions/{machine_id}")
async def predictions(machine_id: str) -> List[PredictionRecord]:
    return [p for p in _recent_predictions if p.machine_id == machine_id][-100:]
