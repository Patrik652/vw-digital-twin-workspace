from pathlib import Path


def test_digital_twin_api_has_websocket_backend_dependency():
    req = (
        Path(__file__).resolve().parents[1]
        / "services"
        / "digital-twin-api"
        / "requirements.txt"
    )
    content = req.read_text().lower()
    assert "websockets" in content or "uvicorn[standard]" in content
