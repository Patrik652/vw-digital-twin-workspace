"""Pydantic models for alerting service."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AlertRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    severity: Literal["low", "medium", "high", "critical"]
    source: str = "anomaly-detection"
    message: str
    metric: str | None = None
    value: float | None = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AlertResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["queued", "sent", "skipped"]
    detail: str
