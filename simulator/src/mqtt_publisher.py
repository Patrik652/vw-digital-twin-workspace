"""MQTT publisher for CNC telemetry."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

try:
    import paho.mqtt.client as mqtt
except Exception:  # pragma: no cover - optional for tests
    mqtt = None


@dataclass
class MQTTPublisher:
    """Publish telemetry to an MQTT broker with buffering and TLS support."""

    machine_id: str
    broker_host: str = "localhost"
    broker_port: int = 1883
    use_tls: bool = False
    cert_path: str | None = None
    key_path: str | None = None
    ca_path: str | None = None
    client_factory: Callable[[], object] | None = None

    client: object | None = field(default=None, init=False)
    _queue: list[str] = field(default_factory=list, init=False)
    _connected: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.client_factory is None:
            if mqtt is None:
                raise RuntimeError("paho-mqtt is required to create a client")
            self.client_factory = mqtt.Client
        self.client = self.client_factory()

        if self.use_tls:
            self.client.tls_set(ca_certs=self.ca_path, certfile=self.cert_path, keyfile=self.key_path)

    @property
    def topic(self) -> str:
        return f"dt/cnc/{self.machine_id}/telemetry"

    def connect(self) -> None:
        self.client.connect(self.broker_host, self.broker_port, keepalive=60)
        if hasattr(self.client, "loop_start"):
            self.client.loop_start()
        self._connected = True
        self._flush_queue()

    def disconnect(self) -> None:
        if hasattr(self.client, "loop_stop"):
            self.client.loop_stop()
        if hasattr(self.client, "disconnect"):
            self.client.disconnect()
        self._connected = False

    def publish(self, payload: dict, qos: int = 0) -> None:
        message = json.dumps(payload)
        if not self._connected:
            self._queue.append(message)
            return
        self.client.publish(self.topic, message, qos=qos)

    def queue_size(self) -> int:
        return len(self._queue)

    def _flush_queue(self) -> None:
        if not self._queue:
            return
        pending = self._queue
        self._queue = []
        for message in pending:
            self.client.publish(self.topic, message, qos=0)
