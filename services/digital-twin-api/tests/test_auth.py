import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_invalid_key():
    try:
        from auth import verify_api_key
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"Auth import failed: {exc}")

    assert not verify_api_key("bad")
