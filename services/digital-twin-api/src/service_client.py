"""Client for downstream alerting and aggregation services."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
from config import ApiConfig
from models import Telemetry


class ServiceClient:
    """HTTP wrapper for alerting-service and data-aggregator."""

    def __init__(self, config: ApiConfig) -> None:
        self._config = config

    async def send_alert(
        self,
        *,
        machine_id: str,
        severity: str,
        message: str,
        metric: str | None = None,
        value: float | None = None,
        source: str = "digital-twin-api",
    ) -> dict[str, Any]:
        payload = {
            "machine_id": machine_id,
            "severity": severity,
            "source": source,
            "message": message,
            "metric": metric,
            "value": value,
        }
        async with httpx.AsyncClient(timeout=self._config.service_timeout_s) as client:
            response = await client.post(
                f"{self._config.alerting_service_url}/alerts", json=payload
            )
            response.raise_for_status()
            return response.json()

    async def aggregate(
        self,
        *,
        machine_id: str,
        points: list[Telemetry],
        metric: str,
        windows: list[str],
    ) -> dict[str, Any]:
        telemetry_points = []
        for point in points:
            value = self._extract_metric(point.data, metric)
            if value is None:
                continue
            telemetry_points.append(
                {
                    "machine_id": machine_id,
                    "metric": metric,
                    "timestamp": point.timestamp.isoformat(),
                    "value": value,
                }
            )

        payload = {"points": telemetry_points, "windows": windows}
        async with httpx.AsyncClient(timeout=self._config.service_timeout_s) as client:
            response = await client.post(
                f"{self._config.data_aggregator_url}/aggregate", json=payload
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _extract_metric(data: dict[str, Any], metric: str) -> float | None:
        current: Any = data
        for part in metric.split("."):
            if not isinstance(current, dict) or part not in current:
                return None
            current = current[part]
        if isinstance(current, (int, float)):
            return float(current)
        return None
