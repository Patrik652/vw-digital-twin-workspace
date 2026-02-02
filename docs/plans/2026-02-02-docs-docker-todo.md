# Docs + Docker + TODO Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add simulator Docker artifacts, a useful README, and update TODO status to reflect completed work.

**Architecture:** Keep Docker assets minimal and consistent with existing Python services. README documents how to run simulator and services locally. TODO reflects current task completion without changing code behavior.

**Tech Stack:** Docker, docker-compose, Markdown, Python.

---

### Task 1: Simulator Dockerfile

**Files:**
- Create: `simulator/Dockerfile`

**Step 1: Write the failing test**

Create: `simulator/tests/test_dockerfile.py`

```python
from pathlib import Path


def test_simulator_dockerfile_exists():
    dockerfile = Path(__file__).resolve().parents[1] / "Dockerfile"
    assert dockerfile.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest simulator/tests/test_dockerfile.py::test_simulator_dockerfile_exists -v`
Expected: FAIL (file missing)

**Step 3: Write minimal implementation**

Create `simulator/Dockerfile`:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY gcode_samples ./gcode_samples

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "simulator.src.main"]
```

Note: If `simulator/src/main.py` does not exist, set CMD to `python -m simulator.src.cnc_machine` or add a minimal `main.py` that starts the simulator loop.

**Step 4: Run test to verify it passes**

Run: `pytest simulator/tests/test_dockerfile.py::test_simulator_dockerfile_exists -v`
Expected: PASS

**Step 5: Commit**

```bash
git add simulator/Dockerfile simulator/tests/test_dockerfile.py
git commit -m "feat(simulator): add Dockerfile"
```

---

### Task 2: Docker Compose for Local Demo

**Files:**
- Create: `docker-compose.yaml`

**Step 1: Write the failing test**

Create: `tests/test_docker_compose.py`

```python
from pathlib import Path


def test_docker_compose_exists():
    compose = Path(__file__).resolve().parents[1] / "docker-compose.yaml"
    assert compose.exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_docker_compose.py::test_docker_compose_exists -v`
Expected: FAIL (file missing)

**Step 3: Write minimal implementation**

Create `docker-compose.yaml` with services for simulator + three APIs (anomaly, predictive, digital twin), wiring env vars and ports.

Example minimal content:

```yaml
version: "3.9"
services:
  simulator:
    build: ./simulator
    environment:
      MQTT_BROKER_HOST: broker
    depends_on:
      - broker
  anomaly-detection:
    build: ./services/anomaly-detection
    ports: ["8001:8000"]
  predictive-maintenance:
    build: ./services/predictive-maintenance
    ports: ["8002:8000"]
  digital-twin-api:
    build: ./services/digital-twin-api
    ports: ["8000:8000"]
  broker:
    image: eclipse-mosquitto:2
    ports: ["1883:1883"]
```

Adjust to match actual service module paths and configs.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_docker_compose.py::test_docker_compose_exists -v`
Expected: PASS

**Step 5: Commit**

```bash
git add docker-compose.yaml tests/test_docker_compose.py
git commit -m "feat: add docker-compose for local demo"
```

---

### Task 3: README Documentation

**Files:**
- Modify: `README.md`

**Step 1: Write the failing test**

Create: `tests/test_readme.py`

```python
from pathlib import Path


def test_readme_has_sections():
    text = Path(__file__).resolve().parents[1] / "README.md"
    content = text.read_text()
    assert "## Quick Start" in content
    assert "## Services" in content
    assert "## Simulator" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_readme.py::test_readme_has_sections -v`
Expected: FAIL (README minimal)

**Step 3: Write minimal implementation**

Update `README.md` to include:
- Overview
- Quick Start (venv + pytest)
- Simulator usage
- Services endpoints
- Docker compose usage
- Testing section

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_readme.py::test_readme_has_sections -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md tests/test_readme.py
git commit -m "docs: expand README"
```

---

### Task 4: TODO Status Update

**Files:**
- Modify: `TODO_CODEX.md`

**Step 1: Write the failing test**

Create: `tests/test_todo_codex.py`

```python
from pathlib import Path


def test_todo_has_completed_tasks():
    text = Path(__file__).resolve().parents[1] / "TODO_CODEX.md"
    content = text.read_text()
    assert "[x] Task 2" in content or "[X] Task 2" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_todo_codex.py::test_todo_has_completed_tasks -v`
Expected: FAIL (tasks not checked)

**Step 3: Write minimal implementation**

Mark completed tasks in `TODO_CODEX.md` (Tasks 2–6, 12–14) based on delivered code. Leave anything missing unchecked.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_todo_codex.py::test_todo_has_completed_tasks -v`
Expected: PASS

**Step 5: Commit**

```bash
git add TODO_CODEX.md tests/test_todo_codex.py
git commit -m "chore: update TODO_CODEX status"
```

---

### Task 5: Full Test Run

**Files:**
- None

**Step 1: Run full test suite**

Run: `pytest`
Expected: PASS (17+ tests)

**Step 2: Commit if needed**

Only if any last-minute fixes.

