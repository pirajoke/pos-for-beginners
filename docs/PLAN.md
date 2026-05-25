# Execution Plan

Aligned with the 8-step roadmap in `docs/ROADMAP.md`.

## Phase 1 — Obsidian + Claude (Steps 01-02) ✅

Definition of done:

- `scripts/install.py` creates the exact starter vault structure.
- Existing notes are preserved by default.
- Setup actions are logged.
- Obsidian structure interview asks one question at a time.
- Agent working agreement interview asks one question at a time.
- Unknowns are marked `[ASK ME]`.

Validation:

```bash
python3 scripts/bootstrap_client.py --vault /tmp/pos-demo-vault --allow-non-obsidian
python3 scripts/check_vault.py --vault /tmp/pos-demo-vault
python3 -m unittest discover -s tests
```

## Phase 2 — MCP + Context (Steps 03-04) ✅

Definition of done:

- Connector registry covers 10 platforms (Obsidian, Notion, Gmail, Calendar, Linear, GitHub, Exa, Telegram, Granola, Crisp).
- MCP readiness report checks env vars without connecting accounts.
- Example MCP config provided (`config/mcp_servers.example.json`).
- Approved-path source discovery can copy local exports into source folders.
- Source map covers all source types.
- Connect Sources prompt guides safe one-at-a-time connection.

## Phase 3 — Skills (Step 05) ✅

Definition of done:

- `scripts/install_skills.py` clones Claude Skills and Superpowers into `30-Resources/`.
- Skills guide note generated in vault.
- Integrated into bootstrap pipeline.

## Phase 4 — GitHub Sync (Step 06)

Definition of done:

- Documentation for vault git setup.
- Agent memory via GitHub Issues documented.
- Auto-save protocol references git commit + push.

## Phase 5 — Telegram Bot (Step 07)

Definition of done:

- Bot setup guide documented.
- Basic bot template or reference provided.
- Integration path to vault documented.

## Phase 6 — POS MVP Checklist (Step 08)

Definition of done:

- MVP readiness checklist in the vault.
- All 8 steps documented and tested.
- Client can follow the roadmap without Maxim present.

## Phase 7 — Handoff

Definition of done:

- Client instructions are clear enough to follow independently.
- GitHub handoff is documented.
- README covers the full journey.
