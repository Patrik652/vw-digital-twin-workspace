"""Failure mode injection for CNC simulator."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass
class FailureMode:
    """Base class for injectable failure modes."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "failure"
    progression_rate: float = 0.01  # per minute
    severity: float = 0.0
    injected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def tick(self, delta_minutes: float) -> None:
        self.severity = min(1.0, self.severity + self.progression_rate * delta_minutes)

    def get_impact(self) -> Dict[str, float]:
        return {}


@dataclass
class ToolWearAccelerated(FailureMode):
    multiplier: float = 2.0

    def __post_init__(self) -> None:
        self.name = "TOOL_WEAR_ACCELERATED"

    def get_impact(self) -> Dict[str, float]:
        return {"tool_wear_multiplier": self.multiplier * (1.0 + self.severity)}


@dataclass
class SpindleBearingDegradation(FailureMode):
    def __post_init__(self) -> None:
        self.name = "SPINDLE_BEARING_DEGRADATION"

    def get_impact(self) -> Dict[str, float]:
        return {
            "vibration_multiplier": 1.0 + 2.0 * self.severity,
            "temp_offset_c": 5.0 * self.severity,
        }


@dataclass
class CoolantSystemFailure(FailureMode):
    def __post_init__(self) -> None:
        self.name = "COOLANT_SYSTEM_FAILURE"

    def get_impact(self) -> Dict[str, float]:
        return {
            "coolant_flow_multiplier": 1.0 - 0.7 * self.severity,
            "temp_offset_c": 3.0 * self.severity,
        }


@dataclass
class ThermalDrift(FailureMode):
    def __post_init__(self) -> None:
        self.name = "THERMAL_DRIFT"

    def get_impact(self) -> Dict[str, float]:
        return {"position_drift_mm": 0.02 * self.severity}


@dataclass
class AxisBacklash(FailureMode):
    def __post_init__(self) -> None:
        self.name = "AXIS_BACKLASH"

    def get_impact(self) -> Dict[str, float]:
        return {"backlash_mm": 0.05 * self.severity}


class FailureManager:
    """Manage active failure modes."""

    def __init__(self) -> None:
        self._active: Dict[str, FailureMode] = {}

    def inject(self, failure: FailureMode) -> None:
        self._active[failure.id] = failure

    def remove(self, failure_id: str) -> None:
        self._active.pop(failure_id, None)

    def active_failures(self) -> List[FailureMode]:
        return list(self._active.values())

    def tick(self, delta_minutes: float) -> None:
        for failure in self._active.values():
            failure.tick(delta_minutes)

    def combined_impact(self) -> Dict[str, float]:
        impact: Dict[str, float] = {}
        for failure in self._active.values():
            for key, value in failure.get_impact().items():
                impact[key] = impact.get(key, 0.0) + value
        return impact
