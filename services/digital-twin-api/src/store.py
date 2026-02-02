"""In-memory data stores for Digital Twin API."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List

from models import AnomalyRecord, Machine, PredictionRecord, Telemetry


@dataclass
class InMemoryStore:
    machines: Dict[str, Machine] = field(default_factory=dict)
    telemetry: Dict[str, Deque[Telemetry]] = field(default_factory=dict)
    predictions: Dict[str, List[PredictionRecord]] = field(default_factory=dict)
    anomalies: Dict[str, List[AnomalyRecord]] = field(default_factory=dict)

    def add_machine(self, machine: Machine) -> None:
        self.machines[machine.id] = machine

    def list_machines(self) -> List[Machine]:
        return list(self.machines.values())

    def get_machine(self, machine_id: str) -> Machine | None:
        return self.machines.get(machine_id)

    def add_telemetry(self, item: Telemetry, max_items: int = 200) -> None:
        q = self.telemetry.setdefault(item.machine_id, deque(maxlen=max_items))
        q.append(item)

    def latest_telemetry(self, machine_id: str) -> Telemetry | None:
        q = self.telemetry.get(machine_id)
        return q[-1] if q else None

    def history(self, machine_id: str) -> List[Telemetry]:
        q = self.telemetry.get(machine_id)
        return list(q) if q else []

    def add_prediction(self, record: PredictionRecord) -> None:
        self.predictions.setdefault(record.machine_id, []).append(record)

    def list_predictions(self, machine_id: str) -> List[PredictionRecord]:
        return self.predictions.get(machine_id, [])

    def add_anomaly(self, record: AnomalyRecord) -> None:
        self.anomalies.setdefault(record.machine_id, []).append(record)

    def list_anomalies(self, machine_id: str) -> List[AnomalyRecord]:
        return self.anomalies.get(machine_id, [])
