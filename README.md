# CNC Machine Digital Twin - Connected Factory Demo

A CNC machine digital twin demo built for a Volkswagen Group Services application. It includes a physics-inspired simulator, anomaly detection, predictive maintenance, and a digital twin API.

## Architecture

- **Simulator** produces telemetry and publishes over MQTT.
- **Anomaly Detection** flags outliers via rules, Z-score, and Isolation Forest.
- **Predictive Maintenance** estimates tool RUL and spindle health.
- **Digital Twin API** serves REST + WebSocket access to latest state.

## Quick Start

### Local Python (dev)

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r simulator/requirements.txt
pip install -r services/anomaly-detection/requirements.txt
pip install -r services/predictive-maintenance/requirements.txt
pip install -r services/digital-twin-api/requirements.txt
pytest
```

### Docker Compose

```bash
docker compose up --build
```

This starts the MQTT broker, simulator, and three API services on ports 8000-8002.

## Simulator

Run the simulator loop locally:

```bash
python - << 'PY'
import asyncio
from simulator.src.cnc_machine import CNCMachine

asyncio.run(CNCMachine().run())
PY
```

Environment variables:
- `MQTT_BROKER` (default `localhost`)
- `MQTT_PORT` (default `1883`)
- `MQTT_USE_TLS` (`true|false`)

## Services


## Demo Steps

1. Start the stack:

```bash
docker compose up --build
```

2. Check health endpoints:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
```

3. (Optional) Connect to the WebSocket:

```bash
# Example using wscat
wscat -c ws://localhost:8000/ws/machines/CNC-001/telemetry
```

- **Anomaly Detection**: `http://localhost:8001/health`
- **Predictive Maintenance**: `http://localhost:8002/health`
- **Digital Twin API**: `http://localhost:8000/health`
- **Digital Twin WebSocket**: `ws://localhost:8000/ws/machines/{machine_id}/telemetry`

## Testing

```bash
pytest
```

## Repository Layout

- `simulator/` CNC machine simulator
- `services/` microservices (anomaly detection, predictive maintenance, digital twin API)
- `terraform/` IaC modules and environments
- `kubernetes/` Helm charts and manifests
- `monitoring/` dashboards and configs
