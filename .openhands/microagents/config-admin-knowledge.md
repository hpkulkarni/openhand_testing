---
name: config-admin-knowledge
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - config-admin
  - configuration admin
  - config admin
  - admin tool
  - login page
---

# Configuration Admin Tool knowledge

Full documentation is in `docs/kb/`. Open the file that matches the task:

- Layout and request flow: `docs/kb/architecture.md`
- Tables, validation and seed data: `docs/kb/data-model.md`
- Endpoints, auth and status codes: `docs/kb/api-reference.md`
- Code and security rules: `docs/kb/conventions.md`
- Writing and running tests: `docs/kb/testing.md`
- Running and resetting the app: `docs/kb/runbook.md`
- What a change affects: `docs/kb/change-impact-map.md`
- Limitations not to fix by accident: `docs/kb/known-gaps.md`

Roles: `admin` can read and write configs, `viewer` is read-only, and the server enforces it (403). Environments: `dev`, `staging`, `prod`. Value types: `string`, `int`, `bool`, `json`.

Quick check that everything works: `cd config-admin && .venv/bin/python -m pytest -q`.
