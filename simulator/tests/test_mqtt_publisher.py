import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


class FakeClient:
    def __init__(self):
        self.connected = False
        self.published = []
        self.tls_enabled = False

    def connect(self, host, port, keepalive=60):
        self.connected = True

    def loop_start(self):
        return None

    def loop_stop(self):
        return None

    def disconnect(self):
        self.connected = False

    def publish(self, topic, payload, qos=0):
        if not self.connected:
            raise RuntimeError("not connected")
        self.published.append((topic, payload, qos))

    def tls_set(self, ca_certs=None, certfile=None, keyfile=None):
        self.tls_enabled = True


def test_buffered_publish_flushes_on_connect():
    try:
        from mqtt_publisher import MQTTPublisher
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"MQTTPublisher import failed: {exc}")

    publisher = MQTTPublisher(
        machine_id="CNC-001",
        broker_host="localhost",
        broker_port=1883,
        client_factory=FakeClient,
    )
    publisher.publish({"value": 1})
    assert publisher.queue_size() == 1
    publisher.connect()
    assert publisher.queue_size() == 0
    assert publisher.client.published
