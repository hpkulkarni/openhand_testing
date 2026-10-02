# Known Gaps

Deliberate limitations of this sample app. They are **not** bugs to silently fix inside an unrelated change; raise them as their own task. Reviewers should flag changes that make them worse.

| Gap | Impact | Suggested fix |
|---|---|---|
| Sessions never expire (`created_at` is stored but unused) | A stolen cookie works forever | Reject sessions older than N hours in `auth.current_user` |
| No login rate limiting or lockout | Password guessing is unthrottled | Count failures per username/IP |
| Session cookie lacks the `Secure` flag | Fine on localhost, unsafe over plain HTTP elsewhere | Set `secure=True` when served over HTTPS |
| No CSRF token (relies on `SameSite=Lax` + JSON bodies) | Acceptable locally, weak for production | Add a CSRF token or require a custom header |
| Demo credentials are seeded and documented | Must never reach a real deployment | Make seeding opt-in via an env var |
| No audit history (only `updated_at` / `updated_by`) | Can't see previous values | Add a `config_history` table |
| No migration tool | Schema changes need manual handling | Introduce Alembic or a `schema_version` table |
| Config values stored in plaintext | Not suitable for real secrets | Don't store secrets here; or add encryption |
| Frontend has no automated tests | UI regressions found by hand | Add Playwright smoke tests |
| No pagination on `GET /api/configs` | Fine for tens of rows | Add `limit`/`offset` |
