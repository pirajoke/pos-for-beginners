# POS FOR BEGINNERS

A small git starter kit that creates a practical Obsidian vault structure, then guides a beginner through setup questions and safe context-source connection.

This is similar in spirit to the POS Daniel handoff, but it is not Barro-specific. It is a reusable client vault starter — POS FOR BEGINNERS.

## What This Repo Does

- Creates a simple Obsidian structure with 10 top-level folders.
- Adds starter rules for folders, note naming, and post-task logging.
- Adds two one-question-at-a-time interviews:
  - Obsidian structure interview.
  - Claude/Codex agent working agreement interview.
- Adds safe source folders for Notion, Mail, Granola, Crisp, Obsidian, and manual context.
- Generates readiness reports for local tools and MCP connector environment variables.
- Copies approved source exports into the correct source folder when a scan path is provided.
- Installs Claude Skills and Superpowers — composable skill libraries for AI agents.
- Does not connect external accounts automatically.

## Quick Start

**Option A — Double-click (macOS):**
1. Clone: `git clone https://github.com/pirajoke/pos-for-beginners.git`
2. Double-click `install.command`
3. Drag your Obsidian vault folder into Terminal
4. Follow the wizard — it walks you through all 8 steps

**Option B — Command line:**
```bash
git clone https://github.com/pirajoke/pos-for-beginners.git
cd pos-for-beginners
python3 scripts/setup_pos.py --vault "/path/to/ObsidianVault"
```

**Check progress:**
```bash
python3 scripts/setup_pos.py --vault "/path/to/ObsidianVault" --status
```

**Jump to a specific step:**
```bash
python3 scripts/setup_pos.py --vault "/path/to/ObsidianVault" --step 3
```

The wizard automatically: creates vault structure, installs Claude/Codex, configures MCP servers, sets up context, installs skills, initializes GitHub, and guides Telegram bot setup.

## Installed Folder Structure

```text
ObsidianVault/
|-- 00-Inbox/
|-- 10-Projects/
|-- 20-Areas/
|-- 30-Resources/
|-- 40-Meetings/
|-- 50-Templates/
|-- 60-Rules/
|-- 70-Sources/
|-- 90-Operations/
`-- 99-Archive/
```

## Skills & Superpowers

The bootstrap automatically clones two skill libraries into `30-Resources/`:

- **Claude Skills** (`claude-skills/`) — official Anthropic skill examples: document workflows, research, code workflows.
- **Superpowers** (`superpowers/`) — composable reusable skills for coding agents by obra.

To update them independently:

```bash
python3 scripts/install_skills.py --vault "/path/to/ObsidianVault"
```

## Source Connection Rule

Use `90-Operations/Setup/Connect Sources Prompt.md`.

Connect one source at a time. Start with manual export or read-only scope. Never scrape broad mailboxes/workspaces, auto-send email, mutate Notion, or store secrets in the vault.

## Validation

```bash
python3 -m unittest discover -s tests
python3 scripts/check_vault.py --vault "/path/to/ObsidianVault"
python3 scripts/doctor.py --vault "/path/to/ObsidianVault"
python3 scripts/mcp_readiness.py --vault "/path/to/ObsidianVault"
```

## 8-Step Roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md) for the full path:

```
Step 01  Obsidian      → vault + structure + rules
Step 02  Claude/Codex  → agent + working agreement
Step 03  MCP servers   → connect platforms one by one
Step 04  Context       → personal + project context
Step 05  Skills        → repeatable agent capabilities
Step 06  GitHub sync   → backup + issues + agent memory
Step 07  Telegram bot  → quick access interface
Step 08  POS MVP       → everything works on real work
```

## Repo Safety

This repo contains structure, scripts, prompts, and templates only. Do not commit client secrets or raw private source material.
