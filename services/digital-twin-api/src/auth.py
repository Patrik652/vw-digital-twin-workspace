"""API key authentication helpers."""

from __future__ import annotations

from config import ApiConfig


def verify_api_key(key: str, config: ApiConfig | None = None) -> bool:
    cfg = config or ApiConfig()
    return key in set(cfg.api_keys)
