from pathlib import Path


def test_readme_has_sections():
    text = Path(__file__).resolve().parents[1] / "README.md"
    content = text.read_text()
    assert "## Quick Start" in content
    assert "## Services" in content
    assert "## Simulator" in content
