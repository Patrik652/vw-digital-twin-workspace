"""Digital Twin API service."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

import httpx
from fastapi import FastAPI, Header, HTTPException, WebSocket

from auth import verify_api_key
from config import ApiConfig
from models import (
    AnomalyRecord,
    AggregateRequest,
    AlertRequest,
    CommandRequest,
    ErrorDetail,
    ErrorResponse,
    Machine,
    MachineStatus,
    PredictionRecord,
    ResponseMetadata,
    SuccessResponse,
    Telemetry,
)
from rate_limit import TokenBucket
from service_client import ServiceClient
from store import InMemoryStore

app = FastAPI(title="Digital Twin API", version="0.1.0")

store = InMemoryStore()
rate_limiters: Dict[str, TokenBucket] = {}
config = ApiConfig()
service_client = ServiceClient(config=config)


def _require_key(x_api_key: str | None) -> str:
    if not x_api_key or not verify_api_key(x_api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


def _rate_limit(key: str) -> None:
    bucket = rate_limiters.setdefault(key, TokenBucket(capacity=100, refill_per_sec=100 / 60))
    if not bucket.allow():
        raise HTTPException(status_code=429, detail="Rate limit exceeded")


def _success(data: Any) -> SuccessResponse:
    return SuccessResponse(data=data, metadata=ResponseMetadata(request_id=str(uuid.uuid4())))


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict:
    return {"status": "ready"}


@app.get("/machines")
async def list_machines(x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    return _success(store.list_machines())


@app.get("/machines/{machine_id}")
async def get_machine(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    machine = store.get_machine(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return _success(machine)


@app.get("/machines/{machine_id}/status")
async def get_status(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    status = MachineStatus()
    return _success(status)


@app.get("/machines/{machine_id}/telemetry")
async def get_telemetry(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    latest = store.latest_telemetry(machine_id)
    return _success(latest)


@app.post("/machines/{machine_id}/telemetry")
async def ingest_telemetry(
    machine_id: str, telemetry: Telemetry, x_api_key: str | None = Header(default=None)
) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    if telemetry.machine_id != machine_id:
        raise HTTPException(status_code=400, detail="Machine ID mismatch")
    if not store.get_machine(machine_id):
        store.add_machine(Machine(id=machine_id, name=machine_id, location="demo"))
    store.add_telemetry(telemetry)
    await _dispatch_telemetry_alerts(telemetry)
    return _success(telemetry)


@app.get("/machines/{machine_id}/history")
async def get_history(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    return _success(store.history(machine_id))


@app.post("/machines/{machine_id}/commands")
async def send_command(
    machine_id: str, command: CommandRequest, x_api_key: str | None = Header(default=None)
) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    return _success({"machine_id": machine_id, "command": command.command, "params": command.params})


@app.get("/predictions/{machine_id}")
async def get_predictions(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    return _success(store.list_predictions(machine_id))


@app.get("/anomalies/{machine_id}")
async def get_anomalies(machine_id: str, x_api_key: str | None = Header(default=None)) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    return _success(store.list_anomalies(machine_id))


@app.post("/machines/{machine_id}/alerts")
async def send_alert(
    machine_id: str, alert: AlertRequest, x_api_key: str | None = Header(default=None)
) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    payload = await service_client.send_alert(
        machine_id=machine_id,
        severity=_normalize_severity(alert.severity),
        message=alert.message,
        metric=alert.metric,
        value=alert.value,
        source=alert.source,
    )
    return _success(payload)


@app.post("/machines/{machine_id}/aggregate")
async def aggregate_machine(
    machine_id: str, req: AggregateRequest, x_api_key: str | None = Header(default=None)
) -> SuccessResponse:
    key = _require_key(x_api_key)
    _rate_limit(key)
    history = store.history(machine_id)
    payload = await service_client.aggregate(
        machine_id=machine_id,
        points=history,
        metric=req.metric,
        windows=_normalize_windows(req),
    )
    return _success(payload)


@app.websocket("/ws/machines/{machine_id}/telemetry")
async def telemetry_ws(websocket: WebSocket, machine_id: str) -> None:
    await websocket.accept()
    latest = store.latest_telemetry(machine_id)
    if latest:
        await websocket.send_json(latest.model_dump(mode="json"))
    await websocket.close()


async def _dispatch_telemetry_alerts(telemetry: Telemetry) -> None:
    spindle = telemetry.data.get("spindle", {})
    temperature = spindle.get("temperature_c")
    if not isinstance(temperature, (int, float)):
        return
    if float(temperature) < config.critical_spindle_temp_c:
        return

    try:
        await service_client.send_alert(
            machine_id=telemetry.machine_id,
            severity="critical",
            message="Spindle temperature crossed critical threshold",
            metric="spindle.temperature_c",
            value=float(temperature),
            source="digital-twin-api",
        )
    except httpx.HTTPError:
        # Alerts are best-effort; ingestion should still succeed.
        pass


def _normalize_severity(severity: str) -> str:
    if severity == "warning":
        return "medium"
    return severity


def _normalize_windows(req: AggregateRequest) -> List[str]:
    if req.window_minutes is None:
        return req.windows
    mapping = {1: "1min", 5: "5min", 60: "1hour"}
    return [mapping[req.window_minutes]]
