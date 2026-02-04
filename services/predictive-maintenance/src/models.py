"""Pydantic models for predictive maintenance service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field


class ToolRULRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    wear_percent: float = Field(..., ge=0, le=100)
    runtime_minutes: float = Field(..., ge=0)
    cutting_speed_m_min: float = Field(..., ge=0)


class ToolRULResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    minutes_remaining: float = Field(..., ge=0)
    confidence: float = Field(..., ge=0, le=1)


class SpindleHealthRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    vibration_mm_s: float = Field(..., ge=0)
    temperature_c: float = Field(..., ge=0)
    trend_slope: float = Field(0.0)


class SpindleHealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    health_score: float = Field(..., ge=0, le=100)
    days_to_maintenance: float = Field(..., ge=0)


class MaintenancePrediction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    component: str
    action: str
    urgency: Literal["low", "medium", "high"]
    estimated_time: str
    confidence: float = Field(..., ge=0, le=1)


class MaintenanceScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    predictions: List[MaintenancePrediction]


class PredictionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    result_type: str
    payload: dict
