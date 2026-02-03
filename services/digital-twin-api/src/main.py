"""Digital Twin API service."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import Depends, FastAPI, Header, HTTPException, WebSocket

from auth import verify_api_key
from models import (
    AnomalyRecord,
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
from store import InMemoryStore

app = FastAPI(title="Digital Twin API", version="0.1.0")

store = InMemoryStore()
rate_limiters: Dict[str, TokenBucket] = {}


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


@app.websocket("/ws/machines/{machine_id}/telemetry")
async def telemetry_ws(websocket: WebSocket, machine_id: str) -> None:
    await websocket.accept()
    latest = store.latest_telemetry(machine_id)
    if latest:
        await websocket.send_json(latest.model_dump())
    await websocket.close()
