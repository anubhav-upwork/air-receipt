from app import __version__
from fastapi.testclient import TestClient


def test_version():
    assert __version__ == '0.4.0'


def test_health(app_client: TestClient) -> None:
    rv = app_client.get("/health")
    assert rv.status_code == 200
