---
name: config-admin-update-kb
description: Keep docs/kb/ in sync with code changes. Use after changing config-admin behaviour, routes, schema, seed data, or tests, or when asked to refresh the knowledgebase.
---

# Update the knowledgebase

The KB in `docs/kb/` is shared by Claude Code and OpenHands. Stale docs mislead both.

## Steps
1. List what changed: `git diff --name-only main...HEAD`.
2. Map files to docs using `docs/kb/change-impact-map.md`:
   - routes / status codes -> `api-reference.md`
   - `db.py` / `seed.py` / `schemas.py` -> `data-model.md`
   - file layout / flow -> `architecture.md`
   - test counts / fixtures -> `testing.md`
   - run steps -> `runbook.md`
3. Edit only the statements that are now wrong. Verify each against the code; do not copy from memory.
4. If you fixed something listed in `known-gaps.md`, remove that row. If you found a new limitation, add one.
5. Check links in `docs/kb/README.md` still resolve.

Keep the docs short and factual. No speculation.
