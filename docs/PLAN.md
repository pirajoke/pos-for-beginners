# Execution Plan

## Phase 0 - Repo Scaffold

Definition of done:

- Repo has README, AGENTS, CLAUDE, docs, prompts, config, scripts, and tests.
- Git history exists.
- Scripts are dependency-free.

Validation:

```bash
python3 -m unittest discover -s tests
```

## Phase 1 - Vault Bootstrap

Definition of done:

- `scripts/install.py` creates the exact starter vault structure.
- Existing notes are preserved by default.
- Setup actions are logged.
- Connector registry and MCP plan are installed.

Validation:

```bash
python3 scripts/bootstrap_client.py --vault /tmp/pos-demo-vault --allow-non-obsidian
python3 scripts/check_vault.py --vault /tmp/pos-demo-vault
```

## Phase 2 - Guided Interviews

Definition of done:

- Obsidian structure interview asks one question at a time.
- Agent working agreement interview asks one question at a time.
- Unknowns are marked `[ASK ME]`.

## Phase 3 - Source Connection

Definition of done:

- Source map covers Obsidian, Notion, Mail, Granola, Crisp, and Manual.
- MCP readiness report checks env vars without connecting accounts.
- Approved-path source discovery can copy local exports into source folders.

## Phase 4 - Handoff

Definition of done:

- Client instructions are clear enough to follow without Maxim present.
- GitHub handoff is documented after the target repo is created.
