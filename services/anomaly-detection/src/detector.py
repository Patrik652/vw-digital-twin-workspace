"""Anomaly detection logic."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List

import numpy as np
from config import DetectorConfig
from models import Anomaly
from sklearn.ensemble import IsolationForest


@dataclass
class Detector:
    """Combine statistical, ML, and rule-based anomaly detectors."""

    config: DetectorConfig = field(default_factory=DetectorConfig)
    _history: Dict[str, Deque[float]] = field(default_factory=dict, init=False)
    _iforest: IsolationForest = field(
        default_factory=lambda: IsolationForest(
            n_estimators=100, contamination=0.02, random_state=42
        )
    )
    _iforest_ready: bool = field(default=False, init=False)

    def _push(self, metric: str, value: float) -> None:
        window = self._history.setdefault(metric, deque(maxlen=self.config.window_size))
        window.append(value)

    def detect_rule_based(self, telemetry: dict) -> List[Anomaly]:
        anomalies: List[Anomaly] = []
        machine_id = telemetry.get("machine_id", "unknown")
        spindle = telemetry.get("spindle", {})
        tool = telemetry.get("tool", {})
        coolant = telemetry.get("coolant", {})

        if spindle.get("temperature_c", 0) > self.config.rule_temp_high_c:
            anomalies.append(
                Anomaly(
                    machine_id=machine_id,
                    metric="spindle.temperature_c",
                    value=spindle.get("temperature_c", 0),
                    severity="high",
                    detector="rule",
                    reason="Spindle temperature high",
                )
            )

        if tool.get("wear_percent", 0) > self.config.rule_tool_wear_high:
            anomalies.append(
                Anomaly(
                    machine_id=machine_id,
                    metric="tool.wear_percent",
                    value=tool.get("wear_percent", 0),
                    severity="medium",
                    detector="rule",
                    reason="Tool wear high",
                )
            )

        if spindle.get("vibration_mm_s", 0) > self.config.rule_vibration_high:
            anomalies.append(
                Anomaly(
                    machine_id=machine_id,
                    metric="spindle.vibration_mm_s",
                    value=spindle.get("vibration_mm_s", 0),
                    severity="high",
                    detector="rule",
                    reason="Vibration high",
                )
            )

        if (
            spindle.get("rpm", 0) > self.config.rule_min_rpm_running
            and coolant.get("flow_rate_lpm", 0) < self.config.rule_coolant_low
        ):
            anomalies.append(
                Anomaly(
                    machine_id=machine_id,
                    metric="coolant.flow_rate_lpm",
                    value=coolant.get("flow_rate_lpm", 0),
                    severity="high",
                    detector="rule",
                    reason="Coolant flow low while spindle running",
                )
            )

        return anomalies

    def detect_zscore(
        self, metric: str, value: float, machine_id: str
    ) -> List[Anomaly]:
        anomalies: List[Anomaly] = []
        self._push(metric, value)
        window = self._history[metric]
        if len(window) < max(5, self.config.window_size // 2):
            return anomalies
        mean = float(np.mean(window))
        std = float(np.std(window))
        if std <= 1e-6:
            return anomalies
        z = abs((value - mean) / std)
        if z > self.config.zscore_threshold:
            anomalies.append(
                Anomaly(
                    machine_id=machine_id,
                    metric=metric,
                    value=value,
                    severity="medium",
                    detector="zscore",
                    reason=f"Z-score {z:.2f} exceeds threshold",
                )
            )
        return anomalies

    def train_iforest(self, features: np.ndarray) -> None:
        if len(features) < 10:
            return
        self._iforest.fit(features)
        self._iforest_ready = True

    def detect_iforest(
        self, features: np.ndarray, machine_id: str, metric_label: str = "multivariate"
    ) -> List[Anomaly]:
        if not self._iforest_ready:
            return []
        preds = self._iforest.predict(features)
        anomalies: List[Anomaly] = []
        for idx, pred in enumerate(preds):
            if pred == -1:
                anomalies.append(
                    Anomaly(
                        machine_id=machine_id,
                        metric=metric_label,
                        value=float(idx),
                        severity="low",
                        detector="isolation_forest",
                        reason="Isolation Forest flagged outlier",
                    )
                )
        return anomalies
