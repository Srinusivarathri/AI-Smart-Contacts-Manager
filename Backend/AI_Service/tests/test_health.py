from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "AI Service"}


def test_root_returns_running():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": "AI Service", "status": "running"}