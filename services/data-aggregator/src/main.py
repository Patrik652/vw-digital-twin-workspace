"""FastAPI application for data-aggregator service."""

from __future__ import annotations

from aggregator import DataAggregator
from config import AggregatorConfig
from fastapi import FastAPI
from models import AggregateRequest, AggregateResponse

app = FastAPI(title="Data Aggregator Service", version="0.1.0")

_config = AggregatorConfig()
_aggregator = DataAggregator()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict:
    return {"status": "ready", "windows": list(_config.default_windows)}


@app.post("/aggregate", response_model=AggregateResponse)
async def aggregate(request: AggregateRequest) -> AggregateResponse:
    windows = request.windows or list(_config.default_windows)
    buckets = _aggregator.aggregate(request.points, windows)
    return AggregateResponse(buckets=buckets)
