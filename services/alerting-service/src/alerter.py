"""Alert notification delivery logic."""

from __future__ import annotations

import logging

import httpx

from config import AlertingConfig
from models import AlertRequest

LOG = logging.getLogger(__name__)


class Alerter:
    """Deliver alerts to external channels such as Slack."""

    def __init__(self, config: AlertingConfig) -> None:
        self._config = config

    async def send(self, alert: AlertRequest) -> tuple[str, str]:
        if not self._config.slack_webhook_url:
            LOG.info("Slack webhook not configured; skipping alert delivery")
            return "skipped", "SLACK_WEBHOOK_URL is not configured"

        payload = {
            "text": (
                f"[{alert.severity.upper()}] {alert.machine_id} - {alert.message} "
                f"(source={alert.source}, metric={alert.metric}, value={alert.value})"
            )
        }

        try:
            async with httpx.AsyncClient(timeout=self._config.request_timeout_s) as client:
                response = await client.post(self._config.slack_webhook_url, json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            LOG.exception("Failed to deliver Slack alert")
            return "queued", f"delivery failed: {exc}"

        return "sent", "alert delivered"
