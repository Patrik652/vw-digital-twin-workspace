# Simulator MQTT + G-code + Failure Modes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add MQTT publishing, G-code parsing, and failure mode injection to the CNC simulator.

**Architecture:** The simulator publishes telemetry through an MQTT client with buffering and TLS support. A standalone G-code parser translates FANUC-style lines into structured commands. Failure modes are modeled as injectable behaviors that adjust telemetry over time.

**Tech Stack:** Python 3.11, paho-mqtt, Pydantic, pytest.

---

### Task 1: MQTT publisher core (TDD)

**Files:**
- Create: `simulator/src/mqtt_publisher.py`
- Modify: `simulator/src/config.py`
- Test: `simulator/tests/test_mqtt_publisher.py`

**Step 1: Write failing tests**

```python
from mqtt_publisher import MQTTPublisher

class FakeClient:
    ...

def test_buffered_publish_flushes_on_connect():
    publisher = MQTTPublisher(machine_id="CNC-001", client_factory=FakeClient)
    publisher.publish({"value": 1})
    assert publisher.queue_size() == 1
    publisher.connect()
    assert publisher.queue_size() == 0
```

**Step 2: Run tests to verify they fail**

Run: `pytest simulator/tests/test_mqtt_publisher.py -v`
Expected: FAIL (ModuleNotFoundError)

**Step 3: Implement minimal MQTT publisher**

Implement MQTTPublisher with buffer, connect/disconnect, TLS config, topic formatting.

**Step 4: Run tests to verify they pass**

Run: `pytest simulator/tests/test_mqtt_publisher.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/mqtt_publisher.py simulator/src/config.py simulator/tests/test_mqtt_publisher.py

git commit -m "feat(simulator): add MQTT publisher"
```

---

### Task 2: G-code parser (TDD)

**Files:**
- Create: `simulator/src/gcode_parser.py`
- Create: `simulator/tests/test_gcode_parser.py`
- Create: `simulator/gcode_samples/` (directory)

**Step 1: Write failing tests**

```python
from gcode_parser import GCodeParser

def test_parses_motion_block():
    parser = GCodeParser()
    cmd = parser.parse_line("N0010 G01 X10.0 Y5.0 F1200")
    assert cmd.block_number == 10
    assert 1 in cmd.g_codes
    assert cmd.x == 10.0
```

**Step 2: Run tests to verify they fail**

Run: `pytest simulator/tests/test_gcode_parser.py -v`
Expected: FAIL

**Step 3: Implement parser**

Support G/M codes, axes, feed, spindle, tool, comments. Provide simple sample programs.

**Step 4: Run tests to verify they pass**

Run: `pytest simulator/tests/test_gcode_parser.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/gcode_parser.py simulator/tests/test_gcode_parser.py simulator/gcode_samples

git commit -m "feat(simulator): add G-code parser"
```

---

### Task 3: Failure mode injection (TDD)

**Files:**
- Create: `simulator/src/failure_modes.py`
- Create: `simulator/tests/test_failure_modes.py`

**Step 1: Write failing tests**

```python
from failure_modes import FailureManager, ToolWearAccelerated

def test_failure_injection_tracks_active():
    manager = FailureManager()
    failure = ToolWearAccelerated(multiplier=3.0)
    manager.inject(failure)
    assert len(manager.active_failures()) == 1
```

**Step 2: Run tests to verify they fail**

Run: `pytest simulator/tests/test_failure_modes.py -v`
Expected: FAIL

**Step 3: Implement failure modes**

Create base class + 5 modes with gradual progression and impacts.

**Step 4: Run tests to verify they pass**

Run: `pytest simulator/tests/test_failure_modes.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/failure_modes.py simulator/tests/test_failure_modes.py

git commit -m "feat(simulator): add failure mode injection"
```

---

### Task 4: Run full simulator tests

**Step 1: Run tests**

Run: `pytest simulator/tests -v`
Expected: PASS
