"""Pydantic models for data-aggregator service."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Window = Literal["1min", "5min", "1hour"]


class MetricPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    metric: str
    timestamp: datetime
    value: float


class AggregateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    points: list[MetricPoint] = Field(default_factory=list)
    windows: list[Window] = Field(default_factory=list)


class AggregateBucket(BaseModel):
    model_config = ConfigDict(extra="forbid")

    machine_id: str
    metric: str
    window: Window
    bucket_start: datetime
    count: int
    min_value: float
    max_value: float
    avg_value: float


class AggregateResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    buckets: list[AggregateBucket]
