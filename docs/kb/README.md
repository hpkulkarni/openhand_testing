# Config Admin Knowledgebase

Single source of truth for the Configuration Admin Tool. Claude Code agents/skills (`.claude/`) and OpenHands microagents (`.openhands/microagents/`) both read from here, so update these files when behaviour changes and the tools stay in sync.

| File | Read it when |
|---|---|
| [architecture.md](architecture.md) | You need the layout, request flow or where code lives |
| [data-model.md](data-model.md) | You touch tables, columns, seed data or validation rules |
| [api-reference.md](api-reference.md) | You add or change an endpoint, status code or auth rule |
| [conventions.md](conventions.md) | You write any code (style, security rules, do/don't) |
| [testing.md](testing.md) | You write or run tests, or decide what a change needs |
| [runbook.md](runbook.md) | You run, reset or debug the app locally |
| [change-impact-map.md](change-impact-map.md) | You need to know what else a change affects (used by the review flow) |
| [factory-workflow.md](factory-workflow.md) | You run or change the Jira-driven planning and coding process |
| [known-gaps.md](known-gaps.md) | You review security/quality or are tempted to "fix" something listed there |

Scope: everything under `config-admin/`. Repo root also holds an unrelated `fibonacci.py` sample; ignore it.
