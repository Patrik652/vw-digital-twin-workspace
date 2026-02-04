import pytest


def test_parse_g00():
    try:
        from gcode_parser import GCodeParser
    except Exception as exc:  # pragma: no cover - import safety
        pytest.fail(f"GCodeParser import failed: {exc}")

    parser = GCodeParser()
    cmd = parser.parse_line("N0010 G00 X12.5 Y3.0 Z2.0")

    assert cmd.block_number == 10
    assert 0 in cmd.g_codes
    assert cmd.x == 12.5
    assert cmd.y == 3.0
    assert cmd.z == 2.0


def test_parse_g01():
    from gcode_parser import GCodeParser

    parser = GCodeParser()
    cmd = parser.parse_line("N0020 G01 X10.0 Y5.0 F1200")

    assert cmd.block_number == 20
    assert 1 in cmd.g_codes
    assert cmd.x == 10.0
    assert cmd.y == 5.0
    assert cmd.f == 1200


def test_parse_m_codes():
    from gcode_parser import GCodeParser

    parser = GCodeParser()
    cmd = parser.parse_line("N0030 M03 S8000 T1")

    assert cmd.block_number == 30
    assert 3 in cmd.m_codes
    assert cmd.s == 8000
    assert cmd.t == 1
