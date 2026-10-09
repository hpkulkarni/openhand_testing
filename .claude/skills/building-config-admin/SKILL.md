---
name: building-config-admin
description: Administer building configuration records (buildings, floors, rooms, devices, settings). Use when asked to add, update, validate, or review building configuration data.
---

# Building Configuration Admin

Helps manage building configuration data safely and consistently.

## Hierarchy

Building > Floor > Room/Zone > Device. Every record needs a unique ID and a parent (except Building).

## Workflow

1. **Locate** the config source (JSON/YAML/DB export). Ask the user if it is not obvious.
2. **Read before editing**: show the current values of the record(s) to be changed.
3. **Apply the change** with the smallest possible edit; never reformat unrelated entries.
4. **Validate** (see checklist) and report any problems.
5. **Summarize** as a before/after diff and wait for confirmation before anything destructive.

## Validation checklist

- IDs are unique and follow the existing naming convention.
- Every floor references an existing building; every room an existing floor; every device an existing room.
- Required fields are present and correctly typed (name, id, timezone, status).
- No device is assigned to two rooms.
- Values are within allowed ranges (e.g. setpoints, schedules, capacities).

## Rules

- Never delete a building, floor, or room that still has children without explicit confirmation.
- Never change an existing ID; create a new record and migrate instead.
- Keep a backup or rely on git history before bulk edits.
- Do not commit secrets (API keys, credentials) found in config files.

## Output format

For each change: `<record id>: <field> <old> -> <new>`, followed by validation results (pass/fail per checklist item).
