---
name: config-admin-review-change
description: Review a code change (diff, branch or PR) in this repo against the knowledgebase and produce a risk-rated verdict. Use when asked to review, assess impact, or gate a change to config-admin.
---

# Review a change

Read first: `docs/kb/change-impact-map.md`, `docs/kb/conventions.md`, `docs/kb/known-gaps.md`.

## Steps
1. Get the change: `git diff main...HEAD` (or the PR diff). List changed files.
2. For each changed file, look it up in the impact map and note the risk level and the other things it says to check.
3. Run the checklist at the bottom of the impact map (auth dependency, parameterised SQL, tests, KB updated, known gaps, new dependencies).
4. Run the tests: `cd config-admin && .venv/bin/python -m pytest -q`.
5. Read the changed code itself. Do not judge from the diff summary alone.

## Output
```
Risk: LOW | MEDIUM | HIGH
Verdict: Block | Request changes | Approve with notes | Approve
Changed areas: <files grouped by impact-map row>
Findings:
  - [severity] file:line - what is wrong and why it matters
Missing: <tests / KB updates / checks not done>
Tests: <pass/fail counts>
```
Only report problems you verified in the code. If something could not be checked, say so.
