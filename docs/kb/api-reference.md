# API Reference

Base: `http://localhost:8000`. JSON in/out. Auth is the `session` cookie set by login.

| Method | Path | Auth | Success | Errors |
|---|---|---|---|---|
| GET | `/api/health` | none | 200 `{"status":"ok"}` | |
| POST | `/api/auth/login` | none | 200 `{username, role}` + cookie | 401 bad credentials, 422 blank fields |
| POST | `/api/auth/logout` | logged in | 200 `{"status":"logged out"}`; session row deleted | 401 |
| GET | `/api/auth/me` | logged in | 200 `{username, role}` | 401 |
| GET | `/api/configs` | logged in | 200 list, ordered by key then environment. Query: `environment` (exact), `q` (substring of key) | 401 |
| GET | `/api/configs/{id}` | logged in | 200 config | 401, 404 |
| POST | `/api/configs` | admin | 201 config | 401, 403, 409 duplicate (key, env), 422 invalid |
| PUT | `/api/configs/{id}` | admin | 200 config | 401, 403, 404, 409, 422 |
| DELETE | `/api/configs/{id}` | admin | 204 | 401, 403, 404 |

## Config object
```json
{"id": 1, "key": "log.level", "value": "DEBUG", "value_type": "string",
 "environment": "dev", "description": "Application log level",
 "updated_at": "2026-10-02 12:00:00", "updated_by": "system"}
```

## Request body for POST/PUT (`ConfigIn`)
`key` (required, `^[a-z0-9_.-]+$`), `value` (string), `value_type` (`string|int|bool|json`), `environment` (`dev|staging|prod`), `description` (optional).

## Status code rules
- 401 = not logged in / bad session. 403 = logged in but not admin.
- 422 comes from two places: pydantic (detail is a **list**) and our own value check (detail is a **string**). The UI handles both.
- Check order on writes: auth, then body validation, then value/type check, then DB.

Pages: `/` (login), `/static/configs.html` (requires login; redirects to `/` on 401).
