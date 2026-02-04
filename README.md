# CNC Machine Digital Twin - Connected Factory Demo

A CNC machine digital twin demo built for a Volkswagen Group Services application. It includes a physics-inspired simulator, anomaly detection, predictive maintenance, and a digital twin API.

## Demo Video

<video src="https://github.com/Patrik652/vw-digital-twin-workspace/raw/main/demo/vw-digital-twin-full-demo.mp4" controls width="100%"></video>

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
pip install -r services/alerting-service/requirements.txt
pip install -r services/data-aggregator/requirements.txt
pytest
```

### Docker Compose

```bash
docker compose up --build
```

This starts the MQTT broker, simulator, and five API services on ports 8000-8004.

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

- **Digital Twin API**: `http://localhost:8000`
- **Anomaly Detection**: `http://localhost:8001`
- **Predictive Maintenance**: `http://localhost:8002`
- **Alerting Service**: `http://localhost:8003`
- **Data Aggregator**: `http://localhost:8004`

### Digital Twin API integration settings

Configure `digital-twin-api` forwarding via environment variables:

- `ALERTING_SERVICE_URL` default: `http://alerting-service:8000`
- `DATA_AGGREGATOR_URL` default: `http://data-aggregator:8000`
- `CRITICAL_SPINDLE_TEMP_C` default: `90`
- `SERVICE_TIMEOUT_S` default: `3`

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
curl http://localhost:8003/health
curl http://localhost:8004/health
```

3. Ingest telemetry through Digital Twin API (auto-alert when spindle temperature is critical):

```bash
curl -X POST http://localhost:8000/machines/CNC-001/telemetry \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-key" \
  -d '{"timestamp":"2026-02-04T06:40:00Z","machine_id":"CNC-001","data":{"spindle":{"temperature_c":95.0}}}'
```

4. Request aggregated rollup through Digital Twin API (forwarded to data-aggregator):

```bash
curl -X POST http://localhost:8000/machines/CNC-001/aggregate \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-key" \
  -d '{"metric":"spindle.temperature_c","windows":["1min","5min"]}'
```

5. Send explicit alert through Digital Twin API (forwarded to alerting-service):

```bash
curl -X POST http://localhost:8000/machines/CNC-001/alerts \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-key" \
  -d '{"severity":"high","message":"Manual test alert","metric":"spindle.temperature_c","value":95.0}'
```

Backward compatibility:
- `severity: "warning"` is accepted and internally mapped to `medium`.
- `window_minutes` is accepted only as `1`, `5`, or `60` and mapped to `["1min"]`, `["5min"]`, or `["1hour"]`.

Validation example (unsupported `window_minutes` returns `422`):

```bash
curl -X POST http://localhost:8000/machines/CNC-001/aggregate \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-key" \
  -d '{"window_minutes":7}'
```

6. (Optional) Connect to the WebSocket:

```bash
# Example using wscat
wscat -c ws://localhost:8000/ws/machines/CNC-001/telemetry
```

- **Anomaly Detection**: `http://localhost:8001/health`
- **Predictive Maintenance**: `http://localhost:8002/health`
- **Digital Twin API**: `http://localhost:8000/health`
- **Alerting Service**: `http://localhost:8003/health`
- **Data Aggregator**: `http://localhost:8004/health`
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
