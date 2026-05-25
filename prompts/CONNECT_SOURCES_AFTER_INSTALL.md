# Connect Sources After Install

Use this only after the first Obsidian interview has been saved.

## Operator Prompt

```text
You are helping me connect context sources to my Obsidian vault safely.

Read first:
- 70-Sources/Context Source Map.md
- 90-Operations/Setup/Connector Registry.md
- 90-Operations/Setup/MCP Connection Plan.md
- 60-Rules/Obsidian Rules.md

Ask one question at a time.
First ask: Which source should we connect or import first: Obsidian, Notion, Mail, Granola, Crisp, or Manual?

Rules:
- Do not connect more than one source at a time.
- Use manual export first when possible.
- Use read-only scope first.
- Store secrets outside the vault.
- Do not scrape broad mailboxes or workspaces.
- Do not send email.
- Do not mutate Notion, Mail, Crisp, or calendar data.
- First successful import should create one source note in the correct `70-Sources/` folder.
- Record the action in `90-Operations/Setup/Implementation Log.md`.
```

## First Safe Imports

- Notion: one approved page/database export.
- Mail: one approved thread export.
- Granola: one approved transcript.
- Crisp: one approved conversation export.
- Manual: one dated context note.
