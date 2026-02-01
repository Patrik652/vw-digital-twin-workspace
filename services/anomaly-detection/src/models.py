"""Pydantic models for anomaly detection service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class SpindleTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rpm: float = Field(0.0, ge=0, le=24000)
    load_percent: float = Field(0.0, ge=0, le=100)
    temperature_c: float = Field(20.0, ge=0, le=120)
    vibration_mm_s: float = Field(0.0, ge=0, le=20)


class AxisState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    position_mm: float = 0.0
    velocity_mm_min: float = 0.0


class AxesTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    x: AxisState
    y: AxisState
    z: AxisState


class ToolTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    type: Literal["end_mill", "drill", "tap", "boring_bar"]
    diameter_mm: float = Field(..., gt=0)
    wear_percent: float = Field(0.0, ge=0, le=100)
    runtime_minutes: float = Field(0.0, ge=0)


class CoolantTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    flow_rate_lpm: float = Field(0.0, ge=0, le=20)
    temperature_c: float = Field(20.0, ge=0, le=60)
    pressure_bar: float = Field(0.0, ge=0, le=10)


class PowerTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_kw: float = Field(0.0, ge=0)
    spindle_kw: float = Field(0.0, ge=0)
    servo_kw: float = Field(0.0, ge=0)


class StatusTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: Literal["AUTO", "MDI", "JOG", "REF"]
    program: str
    block: str
    cycle_time_s: int = Field(0, ge=0)


class Telemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    machine_id: str
    spindle: SpindleTelemetry
    axes: AxesTelemetry
    tool: ToolTelemetry
    coolant: CoolantTelemetry
    power: PowerTelemetry
    status: StatusTelemetry


class TelemetryBatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    telemetry: List[Telemetry]


class Anomaly(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    machine_id: str
    metric: str
    value: float
    severity: Literal["low", "medium", "high"]
    detector: Literal["zscore", "isolation_forest", "rule"]
    reason: str


class DetectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    anomalies: List[Anomaly]
    model_not_ready: bool = False
    processed: int = 0
