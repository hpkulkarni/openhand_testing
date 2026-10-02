---
name: config-admin-repo
type: repo
version: 1.0.0
agent: CodeActAgent
---

# Repository guide

This repo contains the **Configuration Admin Tool** in `config-admin/` (FastAPI + SQLite + plain HTML/JS). `fibonacci.py` at the root is an unrelated sample.

The knowledgebase is in `docs/kb/`. **Read `docs/kb/README.md` first**, then the file that matches your task. Do not guess about the schema, routes or conventions; they are documented there.

## Commands (run inside `config-admin/`)
- Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Tests: `.venv/bin/python -m pytest -q` (24 tests passed when this was written)
- Run: `.venv/bin/uvicorn app.main:app --port 8000`, demo login `admin` / `admin123`

## Rules
- Work on a feature branch and open a PR. Do not push to `main`.
- Every protected route needs `Depends(auth.current_user)` or `Depends(auth.require_admin)`.
- Use parameterised SQL. Use `textContent`, not `innerHTML`, for API data in the frontend.
- Add or update tests for every behaviour change and run them before finishing.
- Update the matching `docs/kb/` file in the same change.
- Never commit secrets, `.env` or `*.db` files.
- When calling MCP tools (such as `create_pr`), pass only the parameters that tool defines. Do not add `security_risk` to MCP tool calls, and pass list arguments as real lists.
