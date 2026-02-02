#!/usr/bin/env bash
set -euo pipefail
pytest simulator/tests -v
pytest services/anomaly-detection/tests -v
pytest services/predictive-maintenance/tests -v
pytest services/digital-twin-api/tests -v
