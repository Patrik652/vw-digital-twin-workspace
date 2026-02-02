"""Configuration for Digital Twin API."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ApiConfig:
    """API configuration values."""

    api_keys: list[str] = tuple(filter(None, os.getenv("API_KEYS", "dev-key").split(",")))  # type: ignore[assignment]
    rate_limit_per_min: int = int(os.getenv("RATE_LIMIT_PER_MIN", "100"))
