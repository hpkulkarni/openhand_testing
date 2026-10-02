from tests.conftest import login


def test_health_is_public(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_login_success_returns_role_and_sets_cookie(client):
    res = login(client)
    assert res.status_code == 200
    assert res.json() == {"username": "admin", "role": "admin"}
    assert "session" in res.cookies


def test_login_wrong_password_rejected(client):
    assert login(client, "admin", "nope").status_code == 401


def test_login_unknown_user_rejected(client):
    assert login(client, "ghost", "x").status_code == 401


def test_login_blank_fields_rejected(client):
    assert client.post("/api/auth/login", json={"username": "", "password": ""}).status_code == 422


def test_me_requires_login(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_returns_current_user(viewer):
    assert viewer.get("/api/auth/me").json() == {"username": "viewer", "role": "viewer"}


def test_logout_invalidates_session(admin):
    assert admin.post("/api/auth/logout").status_code == 200
    assert admin.get("/api/auth/me").status_code == 401


def test_forged_session_cookie_rejected(client):
    client.cookies.set("session", "not-a-real-token")
    assert client.get("/api/auth/me").status_code == 401
