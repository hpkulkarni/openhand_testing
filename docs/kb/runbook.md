# Runbook

All commands run from `config-admin/`.

## First-time setup
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run
```bash
.venv/bin/uvicorn app.main:app --reload --port 8000
```
Open http://localhost:8000. Sign in with `admin` / `admin123` (edit) or `viewer` / `viewer123` (read-only).
The database is created on first start at `config-admin/data/config_admin.db` and seeded.

## Reset to demo data
Stop the server, delete `data/config_admin.db`, start again.

## Use a different database
`CONFIG_ADMIN_DB=/path/to/file.db .venv/bin/uvicorn app.main:app`

## Test
```bash
.venv/bin/python -m pytest -q
```

## Manual smoke test (after any frontend change)
1. Sign in as `viewer`: table shows 10 rows, no "New config" button, no Edit/Delete.
2. Sign out, sign in as `admin`: buttons appear.
3. New config `test.flag`, type `bool`, value `maybe`: expect an error "value must be 'true' or 'false'".
4. Change the value to `true`: row appears. Edit it, then delete it.
5. Filter by `prod` and search `smtp`: list narrows.
6. Open `/static/configs.html` in a private window: redirects to `/`.

## Troubleshooting
| Symptom | Cause / fix |
|---|---|
| `ModuleNotFoundError: app` when running pytest | Run from `config-admin/`; `pytest.ini` sets `pythonpath = .` |
| Login always fails after editing seed | Old DB has old users. Delete `data/config_admin.db` |
| Port in use | Use `--port 8001` |
| Everything redirects to `/` | Session cookie missing/invalid; sign in again |
