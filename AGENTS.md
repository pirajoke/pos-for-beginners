# Agent Instructions

## Mission

Maintain a narrow POS FOR BEGINNERS starter kit that can be cloned by a client and used to create a simple, practical Obsidian vault structure.

The repo should help a beginner:

- create a usable vault structure;
- answer setup questions one at a time;
- generate an agent working agreement;
- understand where Notion, Mail, Granola, Crisp, and manual context should go;
- connect MCP/source systems safely later.

## Hard Scope

Do not turn this into:

- a complex Zettelkasten system;
- a full PARA/GTD methodology product;
- a dashboard-first product;
- a broad personal AI OS;
- an autonomous connector bot;
- a mailbox scraper;
- a secret manager.

The first product is: install the vault structure, ask the client the right setup questions, and preserve source context safely in Obsidian.

## Source Of Truth

The client Obsidian vault is the source of truth after install.

Every script that changes the client vault must append an entry to:

```text
90-Operations/Setup/Implementation Log.md
```

Setup answers must be saved to:

```text
90-Operations/Setup/Setup Answers.md
```

## Safety

- Do not connect external accounts without explicit approval.
- Do not store secrets in git or Obsidian.
- Do not scrape broad mailboxes, Notion workspaces, or Crisp histories.
- Do not auto-send email or messages.
- Use manual export or read-only scope first.
- Import one approved source object before any bulk import.

## Development Rules

- Keep scripts dependency-free.
- Prefer markdown and JSON over databases.
- Never overwrite existing client notes unless `--force` is explicitly used.
- Update tests when structure or script behavior changes.
- Run:

```bash
python3 -m unittest discover -s tests
```

before considering repo changes complete.
