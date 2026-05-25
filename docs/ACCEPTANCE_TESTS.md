# Acceptance Tests

The starter is accepted when these are true.

## Install

- A clean vault can be bootstrapped with `scripts/bootstrap_client.py`.
- The vault has no more than 10 top-level folders.
- Existing notes are not overwritten by default.
- `START HERE - POS FOR BEGINNERS Setup.md` exists at the vault root.

## Client Guidance

- The first setup prompt asks one question at a time.
- The client can find:
  - folder rules;
  - file naming convention;
  - note templates;
  - first-week checklist;
  - agent working agreement interview;
  - source connection prompt.

## Source/MCP Safety

- Connector Registry includes Obsidian, Notion, Mail, Granola, and Crisp.
- MCP Readiness Report checks env vars but does not connect accounts.
- Source Discovery copies only from approved scan paths.
- No script sends email, mutates Notion, mutates Crisp, or writes external MCP config.

## Agent Handoff

- A client can paste `90-Operations/Setup/Claude First Run.md` into Claude/Codex and answer questions one at a time.
- Unknowns remain `[ASK ME]`.
- Setup actions are logged to `90-Operations/Setup/Implementation Log.md`.
