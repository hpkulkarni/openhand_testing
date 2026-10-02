# Testing

Framework: pytest + FastAPI `TestClient` (needs `httpx`, already in requirements). Run from `config-admin/`:

```bash
.venv/bin/python -m pytest -q
```
Baseline at creation: **24 passed**. Don't merge a change that lowers this without saying why.

## Fixtures (`tests/conftest.py`)
- `client`: fresh app on a temp SQLite file (`CONFIG_ADMIN_DB` monkeypatched), lifespan runs so the schema and seed data exist.
- `admin` / `viewer`: `client` already logged in as that user.
- `login(client, username, password)` helper.

## What each kind of change needs
| Change | Minimum tests |
|---|---|
| New endpoint | happy path, 401 when logged out, 403 for viewer if it writes, 404/409/422 where they apply |
| Changed validation | one passing and one failing case per rule |
| Auth change | wrong password, unknown user, forged cookie, logout invalidates |
| Seed change | update `test_seed_data_present` count |
| Schema change | a test that reads and writes the new column |
| Frontend-only change | no automated tests yet; smoke-test by hand (see [runbook.md](runbook.md)) |

## Rules
- Tests must not touch `config-admin/data/`. Always use the `client` fixture.
- One behaviour per test, named for the behaviour (`test_viewer_cannot_write`).
- A bug fix starts with a failing test that reproduces it.
- Known warning: Starlette's `httpx` deprecation notice in TestClient. Harmless.
