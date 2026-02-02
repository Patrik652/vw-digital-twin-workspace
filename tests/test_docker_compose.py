from pathlib import Path


def test_docker_compose_exists():
    compose = Path(__file__).resolve().parents[1] / "docker-compose.yaml"
    assert compose.exists()
