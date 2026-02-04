import sys
from pathlib import Path

import pytest

FILE_PATH = Path(__file__).resolve()
ROOT_DIR = None
for parent in FILE_PATH.parents:
    if (parent / "services").is_dir() and (parent / "simulator").is_dir():
        ROOT_DIR = parent
        break
if ROOT_DIR is None:
    ROOT_DIR = FILE_PATH.parents[2]
SRC_DIR = FILE_PATH.parents[1] / "src"
MODULES = ("config", "models", "main", "auth", "detector", "predictor", "cnc_machine")


def _remove_src_path() -> None:
    src_paths = [ROOT_DIR / "simulator" / "src"] + list(
        (ROOT_DIR / "services").glob("*/src")
    )
    for candidate in src_paths:
        cand_str = str(candidate)
        while cand_str in sys.path:
            sys.path.remove(cand_str)


@pytest.fixture(autouse=True)
def _isolate_imports():
    _remove_src_path()
    sys.path.insert(0, str(SRC_DIR))
    for name in MODULES:
        sys.modules.pop(name, None)
    yield
    _remove_src_path()
