"""Pydantic models for Digital Twin API."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, ConfigDict


class Machine(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    location: str
    model: Optional[str] = None


class MachineStatus(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: Literal["AUTO", "MDI", "JOG", "REF"] = "AUTO"
    program: str = "O0001"
    block: str = "N0001"
    cycle_time_s: int = 0


class Telemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    machine_id: str
    data: Dict[str, Any]


class CommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: Literal["start", "stop", "pause", "set_speed", "tool_change"]
    params: Dict[str, Any] = Field(default_factory=dict)


class ResponseMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    request_id: str


class SuccessResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["success"] = "success"
    data: Any
    metadata: ResponseMetadata


class ErrorDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    details: Dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["error"] = "error"
    error: ErrorDetail


class PredictionRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    payload: Dict[str, Any]


class AnomalyRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    payload: Dict[str, Any]


class AlertRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    severity: Literal["low", "medium", "high", "critical", "warning"]
    message: str
    source: str = "digital-twin-api"
    metric: Optional[str] = None
    value: Optional[float] = None


class AggregateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str = "spindle.temperature_c"
    windows: List[Literal["1min", "5min", "1hour"]] = Field(default_factory=lambda: ["1min"])
    window_minutes: Optional[Literal[1, 5, 60]] = None
