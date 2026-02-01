import sys
from pathlib import Path

import pytest

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC_DIR))


def test_parses_motion_block():
    try:
        from gcode_parser import GCodeParser
    except Exception as exc:  # pragma: no cover - intentional for red phase
        pytest.fail(f"GCodeParser import failed: {exc}")

    parser = GCodeParser()
    cmd = parser.parse_line("N0010 G01 X10.0 Y5.0 F1200")
    assert cmd.block_number == 10
    assert 1 in cmd.g_codes
    assert cmd.x == 10.0
    assert cmd.y == 5.0
    assert cmd.f == 1200
