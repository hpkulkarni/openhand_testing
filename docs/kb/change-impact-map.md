# Change Impact Map

Use this to answer "if this file changes, what else must be checked?" It is the basis for automated change review.

| If this changes | Also check / update | Risk |
|---|---|---|
| `app/auth.py` | `tests/test_auth.py`, every route's dependency, [conventions.md](conventions.md) security rules | HIGH (security) |
| `app/main.py` route added/changed | [api-reference.md](api-reference.md), `tests/test_configs.py` or `test_auth.py`, auth dependency present | MEDIUM |
| `app/schemas.py` | API docs, validation tests, `static/app.js` error handling (422 shape) | MEDIUM |
| `app/db.py` `SCHEMA` | [data-model.md](data-model.md), `seed.py`, existing-DB migration note, tests | HIGH (data) |
| `app/seed.py` | `test_seed_data_present` count, data-model.md seed list, README demo credentials | LOW |
| `static/login.html` / `app.js` | runbook smoke test, that `textContent` is still used, redirect-on-401 | MEDIUM |
| `static/style.css` | visual check light + dark + narrow width | LOW |
| `requirements.txt` | runbook setup, dependency review (new package = justify it) | MEDIUM |
| `tests/` only | nothing else; confirm the suite still passes | LOW |
| `docs/kb/` only | nothing else; confirm statements still match the code | LOW |
| `docs/kb/factory-workflow.md` | `.claude/skills/factory-*`, `.openhands/microagents/factory-workflow.md` (they must match it) | MEDIUM |
| `.claude/`, `.openhands/` | KB links still valid; descriptions still match behaviour | LOW |

## Review checklist for any change
1. Does every new/changed route have the right auth dependency?
2. Is SQL parameterised?
3. Are new behaviours covered by tests, and does the suite pass?
4. Was the matching `docs/kb/` file updated?
5. Does anything in [known-gaps.md](known-gaps.md) get worse?
6. Any new dependency, secret, or file that should be in `.gitignore`?

## Suggested verdicts
- **Block**: missing auth on a write route, SQL built from user input, secrets committed, tests failing.
- **Request changes**: missing tests for new behaviour, KB not updated, `innerHTML` with API data.
- **Approve with notes**: style nits, small follow-ups.
