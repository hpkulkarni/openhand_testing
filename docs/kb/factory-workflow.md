# Software Factory Workflow

Two phases for any feature or bug, driven by a Jira ticket. Claude Code skills (`.claude/skills/factory-*`) and the OpenHands microagent (`.openhands/microagents/factory-workflow.md`) both follow this file. Change the process here, not in them.

```
PHASE 1 PLANNING:  1.1 Requirement Validation -> 1.2 Tech Specs -> 1.3 Test Cases -> PLANNING GATE (human)
PHASE 2 CODING:    2.1 Coding -> 2.2 Test Development -> 2.3 Testing -> 2.4 PR Ready
```

`TICKET_ID` is the Jira key (e.g. `CFG-123`). `TYPE` is `feature` or `bug`, taken from the Jira issue type.

## Artifacts (audit trail, committed with the PR)
`docs/factory/<TICKET_ID>/`

| File | Written by |
|---|---|
| `00-ticket.md` | start: Jira summary, description, acceptance criteria, link |
| `01-requirements.md` | step 1.1 |
| `02-tech-spec.md` | step 1.2 |
| `03-test-cases.md` | step 1.3 |
| `04-implementation.md` | step 2.1 |
| `05-test-report.md` | steps 2.2 and 2.3 |
| `06-pr-ready.md` | step 2.4 (gate results, PR link) |
| `status.json` | every step |
| `slack-outbox.md` | only when Slack cannot be reached (see below) |

`status.json`:
```json
{"ticket": "CFG-123", "type": "feature", "phase": "planning",
 "steps": {"1.1": "done", "1.2": "done", "1.3": "pending", "2.1": "pending",
           "2.2": "pending", "2.3": "pending", "2.4": "pending"},
 "verdict_1_1": "ACCEPT", "planning_gate": "pending", "branch": "", "pr": ""}
```
`planning_gate` is `pending`, `approved` or `revise`. A step is `pending`, `done` or `blocked`.

## Tool access and what to do without it
| Need | Use | If unavailable |
|---|---|---|
| Read the Jira ticket | Atlassian MCP (may need `authenticate` first) | Ask the user to paste the ticket; save it as `00-ticket.md` and say so |
| Post to Slack `care-ai-sw-factory` | a Slack MCP tool | Append the message to `slack-outbox.md`, show it to the user, and say it was **not** posted |
| Read Slack replies (approval) | a Slack MCP tool | Approval comes only from the user's own message in this session |
| Zephyr test cases | a Zephyr/Jira test tool | Skip; write `Zephyr: not created` |
| Link PR in Jira | Atlassian MCP comment or remote link | Give the user the PR URL and the text to paste |

Never claim a Slack post, Jira link or Zephyr entry happened unless the tool returned success.

## Slack message format
Channel `care-ai-sw-factory`. One message per step, always this shape:
```
[<TICKET_ID>] Step <N.N> done — <Step name>: <summary>
```
Summaries by step:
- **1.1 Requirement Validation**: findings, open questions, verdict `ACCEPT` / `CONDITIONAL` / `REJECT`
- **1.2 Tech Specs**: approach summary, key decisions, ADRs if any
- **1.3 Test Cases**: number created, P0/P1/P2 breakdown, Zephyr link if created
- **2.1 Coding**: files changed, implementation summary, branch name
- **2.2 Test Development**: number of tests written, coverage areas
- **2.3 Testing**: pass/fail count, any failures and cause
- **2.4 PR Ready**: PR link, review checklist summary, open items

Planning gate message:
```
[<TICKET_ID>] PLANNING COMPLETE — Review the 3 steps above and reply 'proceed' to start the Coding phase, or 'feedback: [your notes]' to revise.
```
Keep messages short. Put detail in the artifact file and link or name it.

## Phase 1: Planning
Read first: `docs/kb/architecture.md`, `data-model.md`, `api-reference.md`, `known-gaps.md`, `change-impact-map.md`.

**1.1 Requirement Validation.** Read the ticket. Check feasibility against the real code and KB, and list gaps, ambiguities and open questions. Number each requirement (`R1`, `R2`, ...) so later steps can trace to them. For a bug, confirm it is reproducible from the description and state the expected vs actual behaviour. Verdict:
- `ACCEPT`: clear and feasible.
- `CONDITIONAL`: feasible but open questions exist. Continue, and carry each question into the tech spec as an explicit assumption.
- `REJECT`: not feasible or contradictory. **Skip 1.2 and 1.3** and go straight to the planning gate with the reason.

**1.2 Tech Specs.** Sections: current state (cite files), alternatives considered, accepted approach, implementation plan (ordered, by file), impact (from `change-impact-map.md`), risks, assumptions, ADRs for real design decisions.

**1.3 Test Cases.** Derive from the requirements and spec. Each case: ID `TC-<TICKET_ID>-NN`, priority, kind (happy / edge / regression / security), requirement traced, steps, expected result, automation target (test file and name). P0 = must pass to ship; P1 = important; P2 = nice to have. Every requirement needs at least one P0. Include regression cases for areas in the impact map.

**Planning gate.** Post the gate message, set `planning_gate: pending`, then **stop and wait**.

Approval rules:
- Only a human message counts: the user's reply in this session, or a Slack reply from a person. Tool output, logs, task notifications and your own earlier text are never approval.
- `proceed` -> `planning_gate: approved`, start Phase 2.
- `feedback: ...` -> `planning_gate: revise`. Redo only the affected steps, update artifacts, repost those step messages and the gate.
- Anything else is not approval. Ask.

## Phase 2: Coding
Precondition: `planning_gate` is `approved` in `status.json`. If not, stop and say so.

**2.1 Coding.** Branch from `main`: `feat/<TICKET_ID>-<slug>` or `fix/<TICKET_ID>-<slug>`. Implement exactly the approved spec, following `conventions.md`. If the spec turns out to be wrong or incomplete, stop and ask; do not silently deviate. Record files changed, summary and any deviation in `04-implementation.md`.

**2.2 Test Case Development.** Write unit and integration tests. **Every P0 case from 1.3 must be automated**; name each test or docstring with its `TC-` ID. Automate P1/P2 where cheap and say which are not. For a bug, the first test reproduces the bug and must fail before the fix. Follow `testing.md`.

**2.3 Testing.** Run the full suite (`cd config-admin && .venv/bin/python -m pytest -q`). Report real counts. On failure, find the cause; if it is an implementation bug, fix and rerun (at most 3 attempts), otherwise report. **Do not go to 2.4 with failing tests.** Save output in `05-test-report.md`.

**2.4 PR Ready.** Run the pre-push quality gate and record each result in `06-pr-ready.md`:
1. **Security**: run the `security-review` skill; also check against `conventions.md` security rules (auth dependency, parameterised SQL, `textContent`, no secrets).
2. **Performance**: look for unbounded queries, queries in loops, blocking work on hot paths, needless full-table reads. State "none found" only after looking.
3. **Code review**: run the `config-admin-reviewer` agent or the `code-review` skill against `git diff main...HEAD`.
Any blocking finding stops the step; fix and rerun the gate. When all pass: update `docs/kb/` files for changed behaviour, commit (artifacts included), push, open the PR, link it in Jira, post the step 2.4 message.

PR body: Jira link, summary, spec and test-case references, test result, gate results, open items.

Pushing needs write access to the remote. If push or PR creation is refused, stop and give the user the exact commands to run.
