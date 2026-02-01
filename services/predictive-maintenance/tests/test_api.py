import sys
from pathlib import Path
import asyncio

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_health():
    try:
        import main
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"API import failed: {exc}")

    assert any(getattr(route, "path", "") == "/health" for route in main.app.routes)
    result = asyncio.run(main.health())
    assert result["status"] == "ok"
