---
name: factory-plan
description: Factory Phase 1 for a Jira ticket. Validates requirements, writes the tech spec, derives P0/P1/P2 test cases, posts each step to Slack care-ai-sw-factory, then opens the planning gate and waits for a human. Use via factory-run or when asked to plan a ticket.
---

# Phase 1: Planning

Follow Phase 1 in `docs/kb/factory-workflow.md`. Inputs: `docs/factory/<TICKET_ID>/00-ticket.md` and `status.json`.

Read first: `docs/kb/architecture.md`, `data-model.md`, `api-reference.md`, `known-gaps.md`, `change-impact-map.md`. Base every claim on the actual code; open the files you cite.

## 1.1 Requirement Validation -> `01-requirements.md`
- Numbered requirements `R1..Rn`, each testable.
- Feasibility against the current code and KB.
- Gaps, ambiguities, open questions (numbered).
- Bug: steps to reproduce, expected vs actual.
- Verdict `ACCEPT` / `CONDITIONAL` / `REJECT`. On `REJECT` skip 1.2 and 1.3 and go to the gate.
- Post the Slack message for 1.1.

## 1.2 Tech Specs -> `02-tech-spec.md`
Current state (with file references), alternatives considered, accepted approach, ordered implementation plan by file, impact per `change-impact-map.md`, risks, assumptions (one per open question from 1.1), ADRs for real decisions. Post the Slack message for 1.2.

## 1.3 Test Cases -> `03-test-cases.md`
`TC-<TICKET_ID>-NN`, priority P0/P1/P2, kind (happy / edge / regression / security), requirement traced, steps, expected result, automation target (file + test name). At least one P0 per requirement. Include regression cases for areas the impact map flags. Create in Zephyr only if a Zephyr tool exists. Post the Slack message for 1.3 with the P0/P1/P2 counts.

## Planning gate
Post the gate message exactly as in the workflow doc, set `planning_gate: pending` in `status.json`, and **stop**. Do not start coding. Tell the user the gate is open and that `proceed` or `feedback: ...` is expected.

Update `status.json` after each step. Post messages through the Slack tool; if none is available, write them to `slack-outbox.md`, show them, and say they were not posted.
