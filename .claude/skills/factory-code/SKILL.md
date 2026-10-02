---
name: factory-code
description: Factory Phase 2 for a Jira ticket. Implements the approved tech spec, automates P0 test cases, runs the suite, runs the pre-push quality gate (security, performance, code review), raises the PR and links it in Jira, posting each step to Slack. Only runs after the planning gate is approved.
---

# Phase 2: Coding

Follow Phase 2 in `docs/kb/factory-workflow.md`.

## Precondition
Read `docs/factory/<TICKET_ID>/status.json`. If `planning_gate` is not `approved`, stop and tell the user the gate is not approved. Do not code.

Read first: `02-tech-spec.md`, `03-test-cases.md`, `docs/kb/conventions.md`, `docs/kb/testing.md`.

## 2.1 Coding -> `04-implementation.md`
- Branch from `main`: `feat/<TICKET_ID>-<slug>` or `fix/<TICKET_ID>-<slug>`.
- Implement the approved spec. For endpoints, follow the `config-admin-add-endpoint` skill.
- If the spec is wrong or incomplete, stop and ask. Record any deviation.
- Post the Slack message for 2.1 (files changed, summary, branch).

## 2.2 Test Case Development -> `05-test-report.md`
- Automate every P0 from `03-test-cases.md`, naming each test with its `TC-` ID. Automate P1/P2 where cheap and list what is not automated.
- Bug: write the reproducing test first and confirm it fails before the fix.
- Post the Slack message for 2.2 (count, coverage areas).

## 2.3 Testing
- `cd config-admin && .venv/bin/python -m pytest -q`. Report real counts and output.
- Failure caused by the implementation: fix and rerun, at most 3 attempts. Otherwise mark the step `blocked` and report.
- Never continue to 2.4 with failing tests.
- Post the Slack message for 2.3 (pass/fail, causes).

## 2.4 PR Ready -> `06-pr-ready.md`
1. Security: `security-review` skill plus the security rules in `conventions.md`.
2. Performance: unbounded queries, queries in loops, blocking work on hot paths, needless full reads. Write "none found" only after looking.
3. Code review: `config-admin-reviewer` agent or `code-review` skill on `git diff main...HEAD`.
Blocking finding -> fix, rerun tests and the gate. All pass -> update the matching `docs/kb/` files, commit with the factory folder, push, open the PR (body: Jira link, summary, spec and test references, test result, gate results, open items), link it in Jira, post the Slack message for 2.4.

If push or PR creation is refused, stop and give the user the exact commands. Set `pr` in `status.json` only once a PR exists.
