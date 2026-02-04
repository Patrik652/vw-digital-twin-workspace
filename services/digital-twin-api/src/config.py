"""Configuration for Digital Twin API."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiConfig:
    """API configuration values."""

    api_keys: list[str] = tuple(filter(None, os.getenv("API_KEYS", "dev-key").split(",")))  # type: ignore[assignment]
    rate_limit_per_min: int = int(os.getenv("RATE_LIMIT_PER_MIN", "100"))
    alerting_service_url: str = os.getenv(
        "ALERTING_SERVICE_URL", "http://alerting-service:8000"
    )
    data_aggregator_url: str = os.getenv(
        "DATA_AGGREGATOR_URL", "http://data-aggregator:8000"
    )
    service_timeout_s: float = float(os.getenv("SERVICE_TIMEOUT_S", "3"))
    critical_spindle_temp_c: float = float(os.getenv("CRITICAL_SPINDLE_TEMP_C", "90"))
