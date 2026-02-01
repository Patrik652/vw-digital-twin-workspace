"""Kinesis-style consumer stub (kept as kafka_consumer for compatibility)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List


@dataclass
class KinesisStubConsumer:
    """Stubbed consumer that yields telemetry batches from a provider."""

    batch_provider: Callable[[], Iterable[dict]]

    def poll(self) -> List[dict]:
        return list(self.batch_provider())
