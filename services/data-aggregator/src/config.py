"""Configuration for data-aggregator service."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AggregatorConfig:
    """Runtime configuration for rollup windows."""

    default_windows: tuple[str, ...] = tuple(os.getenv("AGGREGATION_WINDOWS", "1min,5min,1hour").split(","))
