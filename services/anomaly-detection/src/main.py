"""FastAPI application for anomaly detection."""

from __future__ import annotations

import time
from typing import List

from config import DetectorConfig
from detector import Detector
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from models import Anomaly, DetectionResult, TelemetryBatch
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="Anomaly Detection Service", version="0.1.0")

DETECTION_COUNTER = Counter("anomalies_detected_total", "Total anomalies detected")
PROCESSED_COUNTER = Counter(
    "messages_processed_total", "Total telemetry messages processed"
)
LATENCY_HIST = Histogram("detection_latency_seconds", "Detection latency in seconds")

_detector = Detector(config=DetectorConfig())
_recent_anomalies: List[Anomaly] = []


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
async def ready() -> dict:
    return {"status": "ready"}


@app.post("/detect")
async def detect(batch: TelemetryBatch) -> DetectionResult:
    start = time.perf_counter()
    anomalies: List[Anomaly] = []

    for item in batch.telemetry:
        telemetry = item.model_dump()
        anomalies.extend(_detector.detect_rule_based(telemetry))
        anomalies.extend(
            _detector.detect_zscore(
                "spindle.temperature_c",
                telemetry["spindle"]["temperature_c"],
                item.machine_id,
            )
        )

    duration = time.perf_counter() - start
    LATENCY_HIST.observe(duration)
    PROCESSED_COUNTER.inc(len(batch.telemetry))
    DETECTION_COUNTER.inc(len(anomalies))

    _recent_anomalies.extend(anomalies)
    _recent_anomalies[:] = _recent_anomalies[-100:]

    return DetectionResult(
        anomalies=anomalies,
        model_not_ready=not _detector._iforest_ready,
        processed=len(batch.telemetry),
    )


@app.get("/anomalies")
async def anomalies(limit: int = 50) -> List[Anomaly]:
    return list(_recent_anomalies[-limit:])


@app.get("/metrics")
async def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest(), media_type="text/plain")
