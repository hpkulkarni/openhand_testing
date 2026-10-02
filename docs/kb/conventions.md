# Conventions

## Python (backend)
- Python 3.12+ syntax (`str | None`). Standard library first; add a dependency only if truly needed, and put it in `requirements.txt`.
- Routes live in `app/main.py`. Keep business rules in `schemas.py`/`auth.py`, not inline in routes, when they grow.
- Always use **parameterised SQL** (`?` placeholders). Never build SQL with f-strings from user input. (The `LIKE` in `list_configs` passes the pattern as a parameter; the `sql +=` lines append only fixed text.)
- Open connections with `db.connect()` in a `with` block so writes commit.
- Writes require `Depends(auth.require_admin)`; reads require `Depends(auth.current_user)`. A new route without a dependency is a bug unless it is deliberately public (only `/api/health`, `/api/auth/login`).
- Map errors to the status codes in [api-reference.md](api-reference.md); raise `HTTPException` with a plain-string `detail`.

## Frontend
- Plain HTML/JS, no framework, no build step, no CDN scripts.
- Insert server data with `textContent`/DOM APIs. Never `innerHTML` with API data.
- UI role checks are cosmetic. The server is the authority.

## Security rules (do not weaken)
- Passwords only via `auth.hash_password` / `verify_password` (constant-time compare).
- Session cookie stays `httponly`, `samesite=lax`.
- Never log passwords, tokens or full cookie values.
- Never commit real secrets, `.env`, or `*.db` files (see `.gitignore`).

## Git / PRs
- One feature per branch (`feat/...`, `fix/...`). Small PRs. Describe what changed and how it was tested.
- Update the matching `docs/kb/` file in the same PR as the behaviour change.
