#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_structure, safe_write, today


def frontmatter(source: str = "sisi-obsidian-starter") -> str:
    return f"""---
type: note
status: active
source: {source}
date: {today()}
---
"""


def folder_readme(title: str, purpose: str, examples: list[str]) -> str:
    return f"""{frontmatter()}
# {title}

## Purpose

{purpose}

## Put here

{chr(10).join(f"- {item}" for item in examples)}

## Rule

Use clear names. If a note belongs to an active project, put it in `10-Projects/` instead.
"""


def template_note(kind: str) -> str:
    return f"""{frontmatter()}
# {{short-description}} - {{{{date}}}}

Type: {kind}
Status: draft
Source: [ASK ME]

## Summary

[ASK ME]

## Details

[ASK ME]

## Next action

- [ ] [ASK ME]
"""


def content_for(relative: str) -> str:
    if relative == "START HERE - Sisi Obsidian Setup.md":
        return f"""{frontmatter()}
# START HERE - Sisi Obsidian Setup

Open this first:

[[90-Operations/Setup/Start Here]]

Then use:

[[90-Operations/Setup/Claude First Run]]

The installer created a simple vault structure and did not connect external accounts.
"""
    if relative == "00-Inbox/README.md":
        return folder_readme("00-Inbox", "Temporary capture area for unsorted notes.", ["quick notes", "rough ideas", "unprocessed imports"])
    if relative == "10-Projects/README.md":
        return folder_readme("10-Projects", "Active outcomes with a start and finish.", ["client projects", "work deliverables", "learning projects with deadlines"])
    if relative == "20-Areas/README.md":
        return folder_readme("20-Areas", "Ongoing responsibilities without a fixed end date.", ["health", "finance", "career", "team management"])
    if relative == "30-Resources/README.md":
        return folder_readme("30-Resources", "Reference material that may be useful later.", ["research notes", "articles", "how-to notes", "topic summaries"])
    if relative == "40-Meetings/README.md":
        return folder_readme("40-Meetings", "Meeting notes, call notes, and follow-ups.", ["1:1s", "client calls", "team meetings", "interviews"])
    if relative == "99-Archive/README.md":
        return folder_readme("99-Archive", "Old projects and inactive material.", ["finished projects", "obsolete notes", "old exports"])
    if relative.startswith("50-Templates/"):
        return template_note(Path(relative).stem)
    if relative == "10-Projects/_Example Project/README.md":
        return f"""{frontmatter()}
# _Example Project

Use this folder as the shape for real projects.

## Basic structure

- `Tech-Base/TODO.md`
- `Tech-Base/MEMORY.md`
- `Tech-Base/CHANGELOG.md`
- `Tech-Base/MISTAKES.md`

Duplicate this folder only when the project has enough work to deserve its own home.
"""
    if relative.endswith("Tech-Base/TODO.md"):
        return f"""{frontmatter()}
# TODO

- [ ] Replace this example with real project tasks.
"""
    if relative.endswith("Tech-Base/MEMORY.md"):
        return f"""{frontmatter()}
# MEMORY

## Last Completed

- None yet.

## NEXT STEP

- [ASK ME]
"""
    if relative.endswith("Tech-Base/CHANGELOG.md"):
        return f"""{frontmatter()}
# CHANGELOG

- {today()}: Project memory scaffold created.
"""
    if relative.endswith("Tech-Base/MISTAKES.md"):
        return f"""{frontmatter()}
# MISTAKES

Record repeated errors, blockers, and lessons here.
"""
    if relative == "60-Rules/File Naming.md":
        return f"""{frontmatter()}
# File Naming

Use this convention:

```text
project-or-area type short-description - YYYY-MM-DD.md
```

Examples:

- `sisi meeting kickoff - 2026-05-25.md`
- `notion research workspace-map - 2026-05-25.md`
- `personal rule note-naming - 2026-05-25.md`

Rules:

- Use lowercase or simple title case consistently.
- Prefer clear names over clever names.
- Include the date when the note captures an event, meeting, source, or decision.
"""
    if relative == "60-Rules/Obsidian Rules.md":
        return f"""{frontmatter()}
# Obsidian Rules

## Folder Rules

- `00-Inbox`: temporary capture only.
- `10-Projects`: active projects with outcomes.
- `20-Areas`: ongoing responsibilities.
- `30-Resources`: reusable reference material.
- `40-Meetings`: meeting notes and call follow-ups.
- `50-Templates`: reusable note templates.
- `60-Rules`: rules for humans and AI assistants.
- `70-Sources`: imported context from Notion, Mail, Granola, Crisp, Obsidian, or manual exports.
- `90-Operations`: setup logs, reports, and operational traces.
- `99-Archive`: inactive material.

## AI Rule

If Claude, Codex, ChatGPT, Cursor, or another assistant cannot find a fact in this vault or in an approved source, it must write `[ASK ME]` or `UNKNOWN`.
"""
    if relative == "60-Rules/Post-Task Protocol.md":
        return POST_TASK_PROTOCOL
    if relative == "60-Rules/Agent Working Agreement.md":
        return AGENT_WORKING_AGREEMENT_STUB
    if relative == "70-Sources/Context Source Map.md":
        return CONTEXT_SOURCE_MAP
    if relative.startswith("70-Sources/") and relative.endswith("README.md"):
        source_name = Path(relative).parent.name
        return f"""{frontmatter()}
# {source_name}

Put approved {source_name} exports or source notes here.

Rules:

- Import only approved context.
- Preserve source dates and links when possible.
- Do not store secrets in this folder.
- Summaries must link back to source files.
"""
    if relative == "90-Operations/Setup/Implementation Log.md":
        return "# Implementation Log\n\n"
    if relative == "90-Operations/Setup/Setup Answers.md":
        return f"""{frontmatter()}
# Setup Answers

Claude should write interview answers here, one section at a time.
"""
    if relative == "90-Operations/Setup/Start Here.md":
        return START_HERE
    if relative == "90-Operations/Setup/Obsidian Structure Interview.md":
        return OBSIDIAN_INTERVIEW
    if relative == "90-Operations/Setup/Agent Working Agreement Interview.md":
        return AGENT_INTERVIEW
    if relative == "90-Operations/Setup/Claude First Run.md":
        return CLAUDE_FIRST_RUN
    if relative == "90-Operations/Setup/Connect Sources Prompt.md":
        return CONNECT_SOURCES_PROMPT
    if relative == "90-Operations/Setup/First Week Checklist.md":
        return FIRST_WEEK_CHECKLIST
    if relative == "90-Operations/Setup/Connector Registry.md":
        return "# Connector Registry\n\nGenerated by `scripts/install.py`.\n"
    if relative == "90-Operations/Setup/MCP Connection Plan.md":
        return "# MCP Connection Plan\n\nGenerated by `scripts/install.py`.\n"
    return f"{frontmatter()}\n# {Path(relative).stem}\n\n[ASK ME]\n"


START_HERE = f"""{frontmatter()}
# Start Here

## What this vault is

A simple Obsidian workspace for work, learning, projects, meetings, ideas, and personal notes.

## First steps

1. Open `90-Operations/Setup/Claude First Run.md`.
2. Paste it into Claude Code, Claude, Codex, or ChatGPT.
3. Answer one question at a time.
4. Let the assistant update `90-Operations/Setup/Setup Answers.md`.
5. Review `60-Rules/Obsidian Rules.md` before importing sources.

## Safety

External accounts are not connected by this installer. Notion, Mail, Granola, Crisp, and MCP setup require explicit approval.
"""


OBSIDIAN_INTERVIEW = f"""{frontmatter()}
# Obsidian Structure Interview

You are my Obsidian setup assistant.

I am a beginner. Help me create a simple and practical Obsidian vault structure from scratch, so I can use Obsidian for work, learning, projects, meetings, ideas, and personal notes.

Do not give me a long lecture. Run a short interview instead. Ask one question at a time. Do not ask more than one question in a single message.

Your goal is to help me create:
- a simple folder structure;
- clear rules for what goes where;
- a simple file naming convention;
- a few basic note types;
- a short rules file for Obsidian;
- a first-week setup checklist.

Core principles:
- Keep it simple.
- Do not suggest a complex Zettelkasten, PARA, or GTD system unless I ask for it.
- Do not suggest too many plugins.
- Do not create more than 6-10 top-level folders.
- Prefer clear names over clever names.
- The structure should help me find notes later.
- If I use Claude, ChatGPT, Codex, Cursor, or other AI assistants later, file names should be understandable to both humans and AI.

Ask me these questions one by one:

1. What do I want to use Obsidian for?
2. What are my current active areas?
3. What kinds of notes will I create most often?
4. What usually becomes messy for me?
5. How do I usually search for information?
6. Do I want AI assistants to help me with this vault?

Use this default structure unless my answers require something else:

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

Use this simple file naming convention:

```text
project-or-area type short-description - YYYY-MM-DD.md
```

Basic note types:
- idea
- plan
- meeting
- research
- summary
- template
- rule
- source-note
"""


AGENT_INTERVIEW = f"""{frontmatter()}
# Agent Working Agreement Interview

You are helping me create a practical context file for Claude Code and Codex.

Interview me one question at a time. Do not ask more than one question per message.
Your goal is to produce a useful `CLAUDE.md` / `AGENTS.md` file that coding agents can use when working with me.

Collect information about:
1. Who I am: role, background, current situation.
2. What I am building: projects, goals, priorities.
3. My current stack: apps, repos, notes, task systems, automations.
4. How I work: rhythm, constraints, decision style, communication style.
5. What good output looks like: examples, tone, quality bar, preferred formats.
6. My recurring problems: blockers, weak spots, things I want agents to catch.
7. My engineering/product preferences: how to plan, implement, test, review, and ship.
8. Safety rules: what agents should never do without asking.

Rules for the interview:
- Ask concrete questions.
- If my answer is vague, ask one follow-up.
- If you infer something, mark it as an assumption.
- Avoid generic productivity advice.
- Optimize the final file for real work with Claude Code, Codex, and local agents.

When you have enough information, output one clean Markdown file with these sections:

# Agent Working Agreement

## Mission
What the agent is helping me accomplish.

## Current Context
Who I am, what I am building, and what matters now.

## Operating Style
How I prefer agents to work with me.

## Tool Stack
The tools, repos, notes, dashboards, and automations the agent should know about.

## Implementation Preferences
How to plan, code, test, review, and summarize work.

## Communication Rules
How to ask questions, give updates, and write final answers.

## Definition of Done
What must be true before the agent says the task is complete.

## Things To Avoid
Behaviors, assumptions, or actions that create problems for me.

## Open Questions
Important missing context the agent should ask me later.

Keep the final Markdown concise, specific, and actionable. If something is unknown, write `[ASK ME]`.
"""


POST_TASK_PROTOCOL = f"""{frontmatter()}
# Post-Task Protocol

A task is not complete until progress is saved in Obsidian and, when relevant, in GitHub.

## 1. Update Obsidian

For project work, update:

```text
10-Projects/<PROJECT>/Tech-Base/
```

Files:

1. `TODO.md`
   - Mark completed tasks with `[x]`.
   - Add new tasks discovered during work.

2. `MEMORY.md`
   - Update `## NEXT STEP`.
   - Update `## Last Completed`.

3. `CHANGELOG.md`
   - Add one short entry:
   - `- YYYY-MM-DD: what was done`

## 2. Update GitHub Issue

If the work is connected to a GitHub issue, add a progress comment and move board status when relevant.

## 3. Write Session Log

At the end of the session, write:

```text
90-Operations/logs/YYYY-MM-DD -- short-description -- agent.md
```

Include:

# Session Log

## Done
- What was completed

## Current Status
- Where the project stands now

## Next Step
- The next concrete action

## Blockers
- Any errors, risks, or blockers

## 4. Blockers And Mistakes

If there was an error, blocker, repeated failure, or important lesson, record it in:

```text
10-Projects/<PROJECT>/Tech-Base/MISTAKES.md
```

## Rules

- Do not say the task is complete until Obsidian is updated.
- Do not save everything only at the end; update after meaningful steps.
- Prefer updating existing canonical files over creating new scattered notes.
- Keep updates short, factual, and useful for the next agent.
"""


AGENT_WORKING_AGREEMENT_STUB = f"""{frontmatter()}
# Agent Working Agreement

## Mission
[ASK ME]

## Current Context
[ASK ME]

## Operating Style
[ASK ME]

## Tool Stack
[ASK ME]

## Implementation Preferences
[ASK ME]

## Communication Rules
[ASK ME]

## Definition of Done
[ASK ME]

## Things To Avoid
[ASK ME]

## Open Questions
- [ASK ME]
"""


CONTEXT_SOURCE_MAP = f"""{frontmatter()}
# Context Source Map

| Source | Folder | First safe action |
|---|---|---|
| Obsidian | `70-Sources/Obsidian/` | Read local vault notes only. |
| Notion | `70-Sources/Notion/` | Import one approved page/database export. |
| Mail | `70-Sources/Mail/` | Import one approved thread/export. |
| Granola | `70-Sources/Granola/` | Copy one approved transcript export. |
| Crisp | `70-Sources/Crisp/` | Import one approved conversation export. |
| Manual context | `70-Sources/Manual/` | Add dated source notes with links. |

## Rule

Answer context-location questions from this map first. If the answer is not here, ask where the source lives before connecting anything.
"""


CLAUDE_FIRST_RUN = f"""{frontmatter()}
# Claude First Run

Paste this into Claude Code, Claude, Codex, or ChatGPT:

```text
You are my Obsidian setup assistant for the Sisi starter vault.

Start with:
90-Operations/Setup/Obsidian Structure Interview.md

Ask one question at a time. Do not ask more than one question per message.
Write my answers into:
90-Operations/Setup/Setup Answers.md

Then run:
90-Operations/Setup/Agent Working Agreement Interview.md

After the interviews, update:
- 60-Rules/Obsidian Rules.md
- 60-Rules/Agent Working Agreement.md
- 60-Rules/File Naming.md
- 60-Rules/Post-Task Protocol.md

Do not connect Notion, Mail, Granola, Crisp, or any MCP server until I approve the exact source and scope.
If a fact is unknown, write [ASK ME].
```
"""


CONNECT_SOURCES_PROMPT = f"""{frontmatter()}
# Connect Sources Prompt

Paste this into Claude Code or Codex after the first vault interview is done:

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
"""


FIRST_WEEK_CHECKLIST = f"""{frontmatter()}
# First Week Checklist

## Day 1 - Structure

- [ ] Open `START HERE - Sisi Obsidian Setup.md`.
- [ ] Run the Obsidian structure interview.
- [ ] Save answers in `90-Operations/Setup/Setup Answers.md`.
- [ ] Review `60-Rules/Obsidian Rules.md`.

## Day 2 - First Notes

- [ ] Create one project note in `10-Projects/`.
- [ ] Create one area note in `20-Areas/`.
- [ ] Create one meeting note in `40-Meetings/`.
- [ ] Move loose notes out of `00-Inbox`.

## Day 3 - Agent Context

- [ ] Run the Agent Working Agreement interview.
- [ ] Update `60-Rules/Agent Working Agreement.md`.
- [ ] Mark unknowns as `[ASK ME]`.

## Day 4 - Sources

- [ ] Decide which source to import first.
- [ ] Use `90-Operations/Setup/Connect Sources Prompt.md`.
- [ ] Import one approved source object only.

## Day 5 - Search Test

- [ ] Search for one project.
- [ ] Search for one meeting.
- [ ] Search for one source.
- [ ] Rename unclear notes.

## Day 6 - Cleanup

- [ ] Empty or triage `00-Inbox`.
- [ ] Archive inactive material.
- [ ] Update folder rules if something was confusing.

## Day 7 - Review

- [ ] Check `90-Operations/Setup/Implementation Log.md`.
- [ ] Write what works.
- [ ] Write what is still confusing.
- [ ] Decide the next source or project to set up.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Sisi starter Obsidian vault structure.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    structure = load_structure()
    created: list[str] = []
    skipped: list[str] = []

    for directory in structure["directories"]:
        path = vault / directory
        path.mkdir(parents=True, exist_ok=True)
        created.append(directory + "/")

    for relative in structure["files"]:
        path = vault / relative
        if safe_write(path, content_for(relative), force=args.force):
            created.append(relative)
        else:
            skipped.append(relative)

    print(f"Created/verified: {len(created)}")
    print(f"Skipped existing files: {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
