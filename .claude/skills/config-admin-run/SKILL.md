---
name: config-admin-run
description: Set up, start, reset and smoke-test the Configuration Admin Tool in config-admin/. Use when asked to run the app, log in, reset demo data, or verify a change works in the browser.
---

# Run the Configuration Admin Tool

Read `docs/kb/runbook.md` first; it is the source of truth for commands and the smoke test.

1. `cd config-admin`
2. First time only: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
3. Start: `.venv/bin/uvicorn app.main:app --port 8000` (add `--reload` for development)
4. Check `curl -s localhost:8000/api/health` returns `{"status":"ok"}`
5. Demo logins: `admin` / `admin123` (can edit), `viewer` / `viewer123` (read-only)

Reset demo data: stop the server, delete `config-admin/data/config_admin.db`, start again.

After a frontend change, walk through the manual smoke test in the runbook. Stop any server you started before finishing.
