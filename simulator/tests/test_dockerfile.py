from pathlib import Path


def test_simulator_dockerfile_exists():
    dockerfile = Path(__file__).resolve().parents[1] / "Dockerfile"
    assert dockerfile.exists()
