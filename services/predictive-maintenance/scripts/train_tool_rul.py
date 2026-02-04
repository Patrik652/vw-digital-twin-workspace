"""Train a simple linear regression model for tool RUL (demo stub)."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "tool_rul_sample.csv"


def main() -> None:
    rows = []
    with DATA_PATH.open() as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            rows.append(row)

    X = np.array(
        [
            [
                float(r["wear_percent"]),
                float(r["runtime_minutes"]),
                float(r["cutting_speed_m_min"]),
            ]
            for r in rows
        ]
    )
    y = np.array([float(r["minutes_remaining"]) for r in rows])

    model = LinearRegression().fit(X, y)
    print("coefficients:", model.coef_)
    print("intercept:", model.intercept_)


if __name__ == "__main__":
    main()
