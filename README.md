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
- Does not connect external accounts automatically.

## Client Quick Start

macOS:

1. Clone or download this repo:
   `git clone https://github.com/pirajoke/pos-for-beginners.git`
2. Open the repo folder.
3. Double-click `install.command`.
4. Drag the target Obsidian vault folder into Terminal.
5. Optional: drag a folder with approved source exports.
6. Open `START HERE - POS FOR BEGINNERS Setup.md` in Obsidian.
7. Paste `90-Operations/Setup/Claude First Run.md` into Claude Code, Claude, Codex, or ChatGPT.

Command line:

```bash
git clone https://github.com/pirajoke/pos-for-beginners.git
cd pos-for-beginners
python3 scripts/bootstrap_client.py --vault "/path/to/ObsidianVault"
```

For a non-Obsidian test folder:

```bash
python3 scripts/bootstrap_client.py --vault /tmp/pos-demo-vault --allow-non-obsidian
```

Optional approved source import:

```bash
python3 scripts/bootstrap_client.py \
  --vault "/path/to/ObsidianVault" \
  --scan-path "/path/to/approved/source/exports"
```

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

## Repo Safety

This repo contains structure, scripts, prompts, and templates only. Do not commit client secrets or raw private source material.
