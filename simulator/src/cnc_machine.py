"""Core CNC machine simulator class."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timezone
import random
import time

from config import SimulatorConfig
from models import (
    AxesTelemetry,
    AxisState,
    CoolantTelemetry,
    PowerTelemetry,
    SpindleTelemetry,
    StatusTelemetry,
    Telemetry,
    ToolTelemetry,
)
from spindle import Spindle


@dataclass
class CNCMachine:
    """Simulate a CNC machine state and produce telemetry snapshots."""

    machine_id: str | None = None
    config: SimulatorConfig | None = None
    spindle: Spindle = field(default_factory=Spindle)

    _running: bool = field(default=False, init=False)
    _paused: bool = field(default=False, init=False)
    _last_cycle_ts: float | None = field(default=None, init=False)
    _tool_wear_percent: float = field(default=0.0, init=False)
    _tool_runtime_minutes: float = field(default=0.0, init=False)

    def __post_init__(self) -> None:
        if self.config is None:
            self.config = SimulatorConfig.from_env()
        if self.machine_id is None:
            self.machine_id = self.config.machine_id

    def start(self) -> None:
        """Start the simulator loop."""

        self._running = True
        self._paused = False
        self._last_cycle_ts = time.monotonic()

    def stop(self) -> None:
        """Stop the simulator loop."""

        self._running = False
        self._paused = False

    def pause(self) -> None:
        """Pause the simulator loop."""

        self._paused = True

    def resume(self) -> None:
        """Resume the simulator loop."""

        if self._running:
            self._paused = False

    async def run(self) -> None:
        """Run the simulator loop asynchronously."""

        self.start()
        while self._running:
            if not self._paused:
                self.generate_telemetry()
            await asyncio.sleep(self.config.cycle_time_s)

    def _advance_state(self, delta_s: float) -> None:
        if delta_s <= 0:
            return
        self._tool_runtime_minutes += delta_s / 60.0
        wear_rate_per_min = 0.05  # conservative demo rate
        self._tool_wear_percent = min(100.0, self._tool_wear_percent + wear_rate_per_min * (delta_s / 60.0))

    def _elapsed_since_last_cycle(self) -> float:
        now = time.monotonic()
        if self._last_cycle_ts is None:
            self._last_cycle_ts = now
            return 0.0
        delta = now - self._last_cycle_ts
        self._last_cycle_ts = now
        return delta

    def generate_telemetry(self) -> Telemetry:
        """Generate a single telemetry snapshot."""

        delta_s = self._elapsed_since_last_cycle() if self._running else 0.0
        self._advance_state(delta_s)

        rpm = 0.0 if not self._running or self._paused else random.uniform(3000, 18000)
        load_percent = 0.0 if rpm == 0 else random.uniform(20.0, 80.0)
        torque_nm = 6.0 + 0.0005 * rpm
        spindle_kw = self.spindle.power_kw(rpm=rpm, torque_nm=torque_nm)

        feed = 0.0 if rpm == 0 else random.uniform(500.0, 8000.0)
        servo_kw = 0.5 + 0.0002 * feed
        total_kw = spindle_kw + servo_kw

        axes = AxesTelemetry(
            x=AxisState(position_mm=random.uniform(0, 250), velocity_mm_min=feed),
            y=AxisState(position_mm=random.uniform(0, 250), velocity_mm_min=feed),
            z=AxisState(position_mm=random.uniform(-100, 0), velocity_mm_min=feed / 2.0),
        )

        spindle = SpindleTelemetry(
            rpm=rpm,
            load_percent=load_percent,
            temperature_c=random.uniform(25.0, 60.0),
            vibration_mm_s=self.spindle.vibration_mm_s(wear_percent=self._tool_wear_percent),
        )

        tool = ToolTelemetry(
            id="T01",
            type="end_mill",
            diameter_mm=10.0,
            wear_percent=self._tool_wear_percent,
            runtime_minutes=self._tool_runtime_minutes,
        )

        coolant = CoolantTelemetry(
            flow_rate_lpm=12.0 if rpm > 0 else 0.0,
            temperature_c=random.uniform(20.0, 30.0),
            pressure_bar=4.0 if rpm > 0 else 0.0,
        )

        power = PowerTelemetry(total_kw=total_kw, spindle_kw=spindle_kw, servo_kw=servo_kw)

        status = StatusTelemetry(
            mode="AUTO",
            program="O1234",
            block="N0100",
            cycle_time_s=int(self.config.cycle_time_s * 1000),
        )

        return Telemetry(
            timestamp=datetime.now(timezone.utc),
            machine_id=self.machine_id,
            spindle=spindle,
            axes=axes,
            tool=tool,
            coolant=coolant,
            power=power,
            status=status,
        )
