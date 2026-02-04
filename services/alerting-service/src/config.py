"""Configuration for alerting service."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AlertingConfig:
    """Runtime configuration loaded from environment variables."""

    slack_webhook_url: str | None = os.getenv("SLACK_WEBHOOK_URL")
    app_name: str = os.getenv("ALERTING_APP_NAME", "alerting-service")
    request_timeout_s: float = float(os.getenv("ALERTING_HTTP_TIMEOUT_S", "5"))
