from pathlib import Path


def test_readme_has_demo_section():
    text = Path(__file__).resolve().parents[1] / "README.md"
    content = text.read_text()
    assert "## Demo Steps" in content
    assert "docker compose up" in content
    assert "curl" in content
