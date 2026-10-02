# OpenHands Testing Framework

This repository is a sandbox for an AI-assisted software factory. It contains a small sample application, the knowledge the AI tools need to work on it, and the agent and skill definitions for both Claude Code and OpenHands.

## Contents

| Path | What it is |
|---|---|
| `config-admin/` | **Configuration Admin Tool**: login page plus a configuration list with create, edit, delete, search and environment filter. FastAPI, SQLite, plain HTML/JS. |
| `docs/kb/` | **Knowledgebase** shared by all agents: architecture, data model, API, conventions, testing, runbook, change-impact map, known gaps. Start at `docs/kb/README.md`. |
| `.claude/skills/` | Claude Code skills: run the app, add an endpoint, review a change, update the KB. |
| `.claude/agents/` | Claude Code agents: developer, reviewer, tester. |
| `.openhands/microagents/` | OpenHands microagents: repo guide, knowledge trigger, change-review trigger. |
| `fibonacci.py` | Unrelated sample from an earlier OpenHands test. |

## Run the Configuration Admin Tool

```bash
cd config-admin
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --port 8000
```

Open http://localhost:8000 and sign in with:

- `admin` / `admin123`: can create, edit and delete configurations
- `viewer` / `viewer123`: read-only

These are demo credentials for local testing only. The database is created and seeded with 10 sample configurations on first start.

## Test

```bash
cd config-admin
.venv/bin/python -m pytest -q
```

## Contributing

Work on a feature branch and open a pull request. Update the matching file in `docs/kb/` whenever behaviour changes. See `docs/kb/conventions.md`.
