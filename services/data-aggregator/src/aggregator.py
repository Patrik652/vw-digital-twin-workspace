"""Time-window aggregation logic for telemetry metrics."""

from __future__ import annotations

from collections import defaultdict
from datetime import datetime

from models import AggregateBucket, MetricPoint, Window

_WINDOW_TO_SECONDS = {
    "1min": 60,
    "5min": 300,
    "1hour": 3600,
}


class DataAggregator:
    """Build fixed-window rollups from metric points."""

    def aggregate(
        self, points: list[MetricPoint], windows: list[Window]
    ) -> list[AggregateBucket]:
        grouped: dict[tuple[str, str, Window, datetime], list[float]] = defaultdict(
            list
        )

        for point in points:
            for window in windows:
                bucket_start = self._bucket_start(point.timestamp, window)
                grouped[(point.machine_id, point.metric, window, bucket_start)].append(
                    point.value
                )

        buckets: list[AggregateBucket] = []
        for (machine_id, metric, window, bucket_start), values in grouped.items():
            buckets.append(
                AggregateBucket(
                    machine_id=machine_id,
                    metric=metric,
                    window=window,
                    bucket_start=bucket_start,
                    count=len(values),
                    min_value=min(values),
                    max_value=max(values),
                    avg_value=sum(values) / len(values),
                )
            )

        buckets.sort(key=lambda b: (b.machine_id, b.metric, b.window, b.bucket_start))
        return buckets

    @staticmethod
    def _bucket_start(timestamp: datetime, window: Window) -> datetime:
        bucket_seconds = _WINDOW_TO_SECONDS[window]
        ts_seconds = int(timestamp.timestamp())
        floored = ts_seconds - (ts_seconds % bucket_seconds)
        return datetime.fromtimestamp(floored, tz=timestamp.tzinfo)
