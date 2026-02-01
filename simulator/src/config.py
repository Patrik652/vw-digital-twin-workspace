"""Configuration for the CNC simulator."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class SimulatorConfig:
    """Configuration values for the CNC simulator core."""

    machine_id: str = "CNC-001"
    cycle_time_s: float = 0.1
    max_spindle_rpm: int = 24000
    min_spindle_rpm: int = 0
    ambient_temp_c: float = 20.0

    @classmethod
    def from_env(cls) -> "SimulatorConfig":
        """Create config from environment variables when provided."""

        return cls(
            machine_id=os.getenv("CNC_MACHINE_ID", cls.machine_id),
            cycle_time_s=float(os.getenv("CNC_CYCLE_TIME_S", cls.cycle_time_s)),
            max_spindle_rpm=int(os.getenv("CNC_MAX_SPINDLE_RPM", cls.max_spindle_rpm)),
            min_spindle_rpm=int(os.getenv("CNC_MIN_SPINDLE_RPM", cls.min_spindle_rpm)),
            ambient_temp_c=float(os.getenv("CNC_AMBIENT_TEMP_C", cls.ambient_temp_c)),
        )
