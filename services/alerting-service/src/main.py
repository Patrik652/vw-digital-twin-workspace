"""FastAPI application for alerting service."""

from __future__ import annotations

from fastapi import FastAPI

from alerter import Alerter
from config import AlertingConfig
from models import AlertRequest, AlertResponse

app = FastAPI(title="Alerting Service", version="0.1.0")

_config = AlertingConfig()
_alerter = Alerter(config=_config)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict:
    return {"status": "ready"}


@app.post("/alerts", response_model=AlertResponse)
async def create_alert(alert: AlertRequest) -> AlertResponse:
    status, detail = await _alerter.send(alert)
    return AlertResponse(status=status, detail=detail)
