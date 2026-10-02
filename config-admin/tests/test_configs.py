NEW = {"key": "feature.beta", "value": "true", "value_type": "bool",
       "environment": "dev", "description": "beta flag"}


def test_configs_require_login(client):
    assert client.get("/api/configs").status_code == 401


def test_seed_data_present(viewer):
    rows = viewer.get("/api/configs").json()
    assert len(rows) == 10
    assert {r["environment"] for r in rows} == {"dev", "staging", "prod"}


def test_filter_by_environment(viewer):
    rows = viewer.get("/api/configs", params={"environment": "prod"}).json()
    assert rows and all(r["environment"] == "prod" for r in rows)


def test_search_by_key(viewer):
    rows = viewer.get("/api/configs", params={"q": "smtp"}).json()
    assert rows and all("smtp" in r["key"] for r in rows)


def test_get_missing_config_404(viewer):
    assert viewer.get("/api/configs/9999").status_code == 404


def test_admin_can_create(admin):
    res = admin.post("/api/configs", json=NEW)
    assert res.status_code == 201
    body = res.json()
    assert body["key"] == "feature.beta" and body["updated_by"] == "admin"


def test_duplicate_key_in_same_environment_conflicts(admin):
    admin.post("/api/configs", json=NEW)
    assert admin.post("/api/configs", json=NEW).status_code == 409


def test_same_key_allowed_in_other_environment(admin):
    admin.post("/api/configs", json=NEW)
    assert admin.post("/api/configs", json={**NEW, "environment": "prod"}).status_code == 201


def test_admin_can_update(admin):
    created = admin.post("/api/configs", json=NEW).json()
    res = admin.put(f"/api/configs/{created['id']}", json={**NEW, "value": "false"})
    assert res.status_code == 200 and res.json()["value"] == "false"


def test_update_missing_config_404(admin):
    assert admin.put("/api/configs/9999", json=NEW).status_code == 404


def test_admin_can_delete(admin):
    created = admin.post("/api/configs", json=NEW).json()
    assert admin.delete(f"/api/configs/{created['id']}").status_code == 204
    assert admin.get(f"/api/configs/{created['id']}").status_code == 404


def test_delete_missing_config_404(admin):
    assert admin.delete("/api/configs/9999").status_code == 404


def test_viewer_cannot_write(viewer):
    assert viewer.post("/api/configs", json=NEW).status_code == 403
    assert viewer.put("/api/configs/1", json=NEW).status_code == 403
    assert viewer.delete("/api/configs/1").status_code == 403


def test_type_validation(admin):
    assert admin.post("/api/configs", json={**NEW, "value_type": "int", "value": "abc"}).status_code == 422
    assert admin.post("/api/configs", json={**NEW, "value_type": "bool", "value": "yes"}).status_code == 422
    assert admin.post("/api/configs", json={**NEW, "value_type": "json", "value": "{bad"}).status_code == 422


def test_key_format_and_environment_validation(admin):
    assert admin.post("/api/configs", json={**NEW, "key": "Bad Key!"}).status_code == 422
    assert admin.post("/api/configs", json={**NEW, "environment": "qa"}).status_code == 422
