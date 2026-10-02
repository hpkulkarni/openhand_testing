# Architecture

Small server-rendered-free app: a FastAPI JSON API plus static HTML/JS pages. SQLite via the standard library `sqlite3` (no ORM). No build step.

```
config-admin/
  app/
    main.py      FastAPI app, all routes, lifespan (calls init_db)
    auth.py      password hashing, sessions, dependencies current_user / require_admin
    db.py        connect(), SCHEMA, init_db(), db_path()
    seed.py      demo users + sample configs (inserted only into empty tables)
    schemas.py   pydantic models (LoginIn, ConfigIn) + validate_value()
  static/
    login.html   sign-in page (served at "/")
    configs.html list/search/filter + create/edit/delete dialog
    app.js       configs page logic (fetch API, render table)
    style.css    light/dark theme, responsive table
  tests/         pytest; conftest.py gives `client`, `admin`, `viewer` fixtures
  requirements.txt, pytest.ini
```

## Request flow
1. Browser loads `/` (login.html), posts to `POST /api/auth/login`.
2. Server verifies PBKDF2 hash, inserts a row in `sessions`, sets an `httponly` cookie `session`.
3. Browser goes to `/static/configs.html`; `app.js` calls `/api/auth/me` then `/api/configs`.
4. Protected routes use `Depends(auth.current_user)` (any logged-in user) or `Depends(auth.require_admin)` (writes).
5. 401 from any call makes `app.js` redirect to `/`.

## Roles
- `admin`: read and write configs.
- `viewer`: read only. The UI hides write buttons, but the **server** enforces it (403).

## Key design choices
- DB path is resolved per call from `CONFIG_ADMIN_DB`, so tests use a temp file without touching real data.
- Sessions are opaque random tokens stored server-side (so logout really invalidates them).
- The frontend renders values with `textContent`, never `innerHTML`, because config values are untrusted input.
