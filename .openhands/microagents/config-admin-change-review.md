---
name: config-admin-change-review
type: knowledge
version: 1.0.0
agent: CodeActAgent
triggers:
  - review this change
  - review the pr
  - review pull request
  - impact analysis
  - code review
---

# Reviewing a change in this repo

1. Read `docs/kb/change-impact-map.md`, `docs/kb/conventions.md` and `docs/kb/known-gaps.md`.
2. Get the diff (`git diff main...HEAD`) and list the changed files.
3. Look up each file in the impact map; note its risk level and the other things to check.
4. Run the checklist at the bottom of the impact map, then run `cd config-admin && .venv/bin/python -m pytest -q`.
5. Read the changed code itself. Only report problems you confirmed, with `file:line`.

Report in this form:
```
Risk: LOW | MEDIUM | HIGH
Verdict: Block | Request changes | Approve with notes | Approve
Changed areas:
Findings:
Missing:
Tests:
```
Blocking: write route without `require_admin`, SQL built from user input, committed secrets, failing tests.
