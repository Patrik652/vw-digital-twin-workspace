import asyncio
import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_health():
    try:
        import main
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"API import failed: {exc}")

    # Validate the route exists
    assert any(getattr(route, "path", "") == "/health" for route in main.app.routes)

    # Call handler directly to avoid TestClient hangs in this environment
    result = asyncio.run(main.health())
    assert result["status"] == "ok"
