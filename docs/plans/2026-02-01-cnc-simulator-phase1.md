# CNC Simulator Phase 1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Initialize the repository structure and build the CNC simulator core (config/models/spindle/cnc_machine) with realistic telemetry and tests.

**Architecture:** The simulator core is a Python package that composes a spindle model, axes state, and tool manager to emit telemetry on a fixed async loop. Configuration and Pydantic models define schema; tests validate physics bounds and telemetry schema.

**Tech Stack:** Python 3.11, Pydantic, pytest, numpy.

---

### Task 1: Initialize git and base repo structure

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `TODO_CODEX.md`
- Create: `simulator/src/.gitkeep`
- Create: `simulator/tests/.gitkeep`
- Create: `services/anomaly-detection/src/.gitkeep`
- Create: `services/anomaly-detection/tests/.gitkeep`
- Create: `services/predictive-maintenance/src/.gitkeep`
- Create: `services/predictive-maintenance/tests/.gitkeep`
- Create: `services/alerting-service/src/.gitkeep`
- Create: `services/alerting-service/tests/.gitkeep`
- Create: `services/digital-twin-api/src/.gitkeep`
- Create: `services/digital-twin-api/tests/.gitkeep`
- Create: `services/data-aggregator/src/.gitkeep`
- Create: `services/data-aggregator/tests/.gitkeep`
- Create: `terraform/modules/.gitkeep`
- Create: `terraform/environments/.gitkeep`
- Create: `kubernetes/charts/.gitkeep`
- Create: `kubernetes/manifests/.gitkeep`
- Create: `ansible/playbooks/.gitkeep`
- Create: `ansible/roles/.gitkeep`
- Create: `ci-cd/concourse/.gitkeep`
- Create: `monitoring/kibana-dashboards/.gitkeep`
- Create: `monitoring/grafana-dashboards/.gitkeep`

**Step 1: Initialize git**

Run: `git init`
Expected: Initialized empty Git repository

**Step 2: Write .gitignore**

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.env

# Terraform
*.tfstate
*.tfstate.*
.terraform/
*.tfvars
!*.tfvars.example

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Dependencies
node_modules/

# Build
dist/
build/
*.egg-info/

# Secrets
*.pem
*.key
secrets/

# Worktrees
.worktrees/
```

**Step 3: Create directory structure + .gitkeep**

Run:
```
mkdir -p simulator/src simulator/tests \
  services/{anomaly-detection,predictive-maintenance,alerting-service,digital-twin-api,data-aggregator}/{src,tests} \
  terraform/{modules,environments} \
  kubernetes/{charts,manifests} \
  ansible/{playbooks,roles} \
  ci-cd/concourse \
  monitoring/{kibana-dashboards,grafana-dashboards}

touch simulator/src/.gitkeep simulator/tests/.gitkeep \
  services/anomaly-detection/src/.gitkeep services/anomaly-detection/tests/.gitkeep \
  services/predictive-maintenance/src/.gitkeep services/predictive-maintenance/tests/.gitkeep \
  services/alerting-service/src/.gitkeep services/alerting-service/tests/.gitkeep \
  services/digital-twin-api/src/.gitkeep services/digital-twin-api/tests/.gitkeep \
  services/data-aggregator/src/.gitkeep services/data-aggregator/tests/.gitkeep \
  terraform/modules/.gitkeep terraform/environments/.gitkeep \
  kubernetes/charts/.gitkeep kubernetes/manifests/.gitkeep \
  ansible/playbooks/.gitkeep ansible/roles/.gitkeep \
  ci-cd/concourse/.gitkeep \
  monitoring/kibana-dashboards/.gitkeep monitoring/grafana-dashboards/.gitkeep
```

**Step 4: Create README.md**

```
# CNC Machine Digital Twin - Connected Factory Demo
```

**Step 5: Create TODO_CODEX.md**

Use the provided template from the kickoff prompt.

**Step 6: Initial commit**

Run:
```
git add .
git commit -m "chore: initialize repository structure"
```
Expected: commit created

---

### Task 2: Create simulator configuration + models (TDD)

**Files:**
- Create: `simulator/src/config.py`
- Create: `simulator/src/models.py`
- Create: `simulator/tests/test_models.py`

**Step 1: Write failing tests for models**

```
from simulator.src.models import Telemetry

def test_telemetry_schema_defaults():
    t = Telemetry.example()
    assert t.spindle.rpm >= 0
    assert 0 <= t.tool.wear_percent <= 100
```

**Step 2: Run tests to confirm fail**

Run: `pytest simulator/tests/test_models.py -v`
Expected: FAIL (Telemetry not defined)

**Step 3: Implement models**

Create Pydantic models for spindle, axes, tool, coolant, power, status, telemetry. Include `example()` constructor for tests.

**Step 4: Run tests to confirm pass**

Run: `pytest simulator/tests/test_models.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/models.py simulator/tests/test_models.py

git commit -m "feat(simulator): add telemetry models"
```

---

### Task 3: Implement spindle physics (TDD)

**Files:**
- Create: `simulator/src/spindle.py`
- Create: `simulator/tests/test_spindle.py`

**Step 1: Write failing tests**

```
from simulator.src.spindle import Spindle

def test_power_calculation():
    spindle = Spindle()
    kw = spindle.power_kw(rpm=12000, torque_nm=10)
    assert 10.0 < kw < 15.0
```

**Step 2: Run tests**

Run: `pytest simulator/tests/test_spindle.py::test_power_calculation -v`
Expected: FAIL

**Step 3: Implement spindle model**

Implement methods for thermal expansion, bearing frequencies (BPFO/BPFI/BSF/FTF), power calculation, and vibration as a function of wear. Use realistic defaults.

**Step 4: Run tests**

Run: `pytest simulator/tests/test_spindle.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/spindle.py simulator/tests/test_spindle.py

git commit -m "feat(simulator): add spindle physics"
```

---

### Task 4: Implement CNC machine core loop (TDD)

**Files:**
- Create: `simulator/src/cnc_machine.py`
- Create: `simulator/tests/test_cnc_machine.py`

**Step 1: Write failing tests**

```
from simulator.src.cnc_machine import CNCMachine

def test_generate_telemetry_schema():
    cnc = CNCMachine(machine_id="CNC-001")
    telemetry = cnc.generate_telemetry()
    assert telemetry.machine_id == "CNC-001"
    assert 0 <= telemetry.spindle.rpm <= 24000
```

**Step 2: Run tests**

Run: `pytest simulator/tests/test_cnc_machine.py -v`
Expected: FAIL

**Step 3: Implement CNCMachine**

Implement initialization, start/stop/pause/resume, and generate_telemetry. Use async loop with configurable cycle time (default 0.1s). Compose spindle and axes/tool data.

**Step 4: Run tests**

Run: `pytest simulator/tests/test_cnc_machine.py -v`
Expected: PASS

**Step 5: Commit**

```
git add simulator/src/cnc_machine.py simulator/tests/test_cnc_machine.py

git commit -m "feat(simulator): add CNC machine core"
```

---

### Task 5: Requirements file + basic package setup

**Files:**
- Create: `simulator/requirements.txt`

**Step 1: Write requirements**

Include: `pydantic`, `numpy`, `pytest`, `paho-mqtt` (later), `rich` (optional logging).

**Step 2: Commit**

```
git add simulator/requirements.txt

git commit -m "chore(simulator): add requirements"
```

---

### Task 6: Run full test suite

**Step 1: Run tests**

Run: `pytest simulator/tests -v`
Expected: PASS

**Step 2: Decide next tasks**

Proceed to Task 3 MQTT publisher or Task 4 G-code parser.
