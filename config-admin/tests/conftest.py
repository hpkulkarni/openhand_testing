import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("CONFIG_ADMIN_DB", str(tmp_path / "test.db"))
    from app.main import app

    with TestClient(app) as c:  # context manager runs lifespan -> init_db + seed
        yield c


def login(client, username="admin", password="admin123"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


@pytest.fixture()
def admin(client):
    assert login(client).status_code == 200
    return client


@pytest.fixture()
def viewer(client):
    assert login(client, "viewer", "viewer123").status_code == 200
    return client
