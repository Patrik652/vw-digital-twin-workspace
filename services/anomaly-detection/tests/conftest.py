import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
MODULES = ("config", "models", "main", "auth", "detector", "predictor", "cnc_machine")


def _remove_src_path() -> None:
    src_path = str(SRC_DIR)
    while src_path in sys.path:
        sys.path.remove(src_path)


@pytest.fixture(autouse=True)
def _isolate_imports():
    _remove_src_path()
    sys.path.append(str(SRC_DIR))
    for name in MODULES:
        sys.modules.pop(name, None)
    yield
    _remove_src_path()
