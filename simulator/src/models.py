"""Pydantic models for CNC simulator telemetry."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SpindleTelemetry(BaseModel):
    """Spindle-related telemetry metrics."""

    model_config = ConfigDict(extra="forbid")

    rpm: float = Field(0.0, ge=0, le=24000)
    load_percent: float = Field(0.0, ge=0, le=100)
    temperature_c: float = Field(20.0, ge=0, le=120)
    vibration_mm_s: float = Field(0.0, ge=0, le=20)


class AxisState(BaseModel):
    """Axis position and velocity state."""

    model_config = ConfigDict(extra="forbid")

    position_mm: float = 0.0
    velocity_mm_min: float = 0.0


class AxesTelemetry(BaseModel):
    """X/Y/Z axes telemetry."""

    model_config = ConfigDict(extra="forbid")

    x: AxisState = Field(default_factory=AxisState)
    y: AxisState = Field(default_factory=AxisState)
    z: AxisState = Field(default_factory=AxisState)


class ToolTelemetry(BaseModel):
    """Tool state and wear telemetry."""

    model_config = ConfigDict(extra="forbid")

    id: str = "T01"
    type: Literal["end_mill", "drill", "tap", "boring_bar"] = "end_mill"
    diameter_mm: float = Field(10.0, gt=0)
    wear_percent: float = Field(0.0, ge=0, le=100)
    runtime_minutes: float = Field(0.0, ge=0)


class CoolantTelemetry(BaseModel):
    """Coolant system telemetry."""

    model_config = ConfigDict(extra="forbid")

    flow_rate_lpm: float = Field(0.0, ge=0, le=20)
    temperature_c: float = Field(20.0, ge=0, le=60)
    pressure_bar: float = Field(0.0, ge=0, le=10)


class PowerTelemetry(BaseModel):
    """Power consumption telemetry."""

    model_config = ConfigDict(extra="forbid")

    total_kw: float = Field(0.0, ge=0)
    spindle_kw: float = Field(0.0, ge=0)
    servo_kw: float = Field(0.0, ge=0)


class StatusTelemetry(BaseModel):
    """Machine status telemetry."""

    model_config = ConfigDict(extra="forbid")

    mode: Literal["AUTO", "MDI", "JOG", "REF"] = "AUTO"
    program: str = "O0001"
    block: str = "N0001"
    cycle_time_s: int = Field(0, ge=0)


class Telemetry(BaseModel):
    """Full telemetry payload for a CNC machine."""

    model_config = ConfigDict(extra="forbid")

    timestamp: datetime
    machine_id: str
    spindle: SpindleTelemetry
    axes: AxesTelemetry
    tool: ToolTelemetry
    coolant: CoolantTelemetry
    power: PowerTelemetry
    status: StatusTelemetry

    @classmethod
    def example(cls) -> "Telemetry":
        """Return a realistic example telemetry snapshot."""

        return cls(
            timestamp=datetime.now(timezone.utc),
            machine_id="CNC-001",
            spindle=SpindleTelemetry(
                rpm=12000, load_percent=45.2, temperature_c=38.5, vibration_mm_s=0.8
            ),
            axes=AxesTelemetry(
                x=AxisState(position_mm=150.234, velocity_mm_min=5000),
                y=AxisState(position_mm=75.891, velocity_mm_min=5000),
                z=AxisState(position_mm=-25.5, velocity_mm_min=2000),
            ),
            tool=ToolTelemetry(
                id="T01",
                type="end_mill",
                diameter_mm=10,
                wear_percent=23.5,
                runtime_minutes=145,
            ),
            coolant=CoolantTelemetry(
                flow_rate_lpm=12.5, temperature_c=22.3, pressure_bar=4.2
            ),
            power=PowerTelemetry(total_kw=8.5, spindle_kw=5.2, servo_kw=2.8),
            status=StatusTelemetry(
                mode="AUTO", program="O1234", block="N0150", cycle_time_s=234
            ),
        )
