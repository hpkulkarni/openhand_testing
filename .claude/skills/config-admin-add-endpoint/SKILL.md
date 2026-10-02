---
name: config-admin-add-endpoint
description: Add or change an API endpoint in the Configuration Admin Tool (config-admin/app). Use for any new route, changed status code, auth rule, or request validation.
---

# Add or change an endpoint

Read first: `docs/kb/api-reference.md`, `docs/kb/conventions.md`, `docs/kb/testing.md`.

## Steps
1. Decide the auth level. Reads: `Depends(auth.current_user)`. Writes: `Depends(auth.require_admin)`. Public only for health/login.
2. Add request models or value rules in `app/schemas.py`; add the route in `app/main.py`.
3. Use parameterised SQL and `db.connect()` in a `with` block.
4. Use the status codes from the API reference (401 not logged in, 403 not admin, 404 missing, 409 duplicate, 422 invalid).
5. Write tests in `tests/` using the `client`, `admin` and `viewer` fixtures. Cover: success, 401 logged out, 403 viewer (if a write), and each error case.
6. Run `cd config-admin && .venv/bin/python -m pytest -q`. All tests must pass.
7. Update `docs/kb/api-reference.md` (and `data-model.md` if the schema changed) in the same change.
8. If the UI uses the endpoint, update `static/app.js` and re-run the smoke test from `docs/kb/runbook.md`.

## Do not
- Build SQL with string formatting from user input.
- Use `innerHTML` with API data.
- Fix items from `docs/kb/known-gaps.md` as a side effect of this change.
