# POS FOR BEGINNERS — 8-Step Roadmap

A step-by-step guide from zero to a working personal operating system.

Each step builds on the previous one. Do not skip ahead. Complete one step before moving to the next.

---

## STEP 01 — Obsidian (OB)

**Goal:** Create a vault, build structure, keep notes and context in one place.

**What happens:**
- Install Obsidian on your machine.
- Run `bootstrap_client.py` to create the vault structure (10 folders, templates, rules).
- Complete the Obsidian Structure Interview (6 questions, one at a time).
- Create your first notes: one project, one area, one meeting note.

**Deliverables:**
- Working vault with `00-Inbox/` through `99-Archive/`.
- `60-Rules/Obsidian Rules.md` customized to your answers.
- `60-Rules/File Naming.md` with your naming convention.
- `90-Operations/Setup/Setup Answers.md` filled in.

**How to start:**
```bash
git clone https://github.com/pirajoke/pos-for-beginners.git
cd pos-for-beginners
python3 scripts/bootstrap_client.py --vault "/path/to/ObsidianVault"
```

**Done when:** You can create, find, and rename notes without confusion.

---

## STEP 02 — Claude / Codex (AI)

**Goal:** Use the agent as the system engine that can read, write, and build.

**What happens:**
- Install Claude Code CLI (`npm install -g @anthropic-ai/claude-code`) or use Codex.
- Complete the Agent Working Agreement Interview (8 topics, one at a time).
- Generate your personal `CLAUDE.md` and `AGENTS.md` files.
- Agent learns: who you are, how you work, what to avoid, what "done" means.

**Deliverables:**
- `60-Rules/Agent Working Agreement.md` — your working contract with AI.
- `CLAUDE.md` in your project root — agent instructions.
- Agent can read your vault, follow your rules, and write structured notes.

**How to start:**
Paste `90-Operations/Setup/Claude First Run.md` into Claude Code, Claude, Codex, or ChatGPT.

**Done when:** The agent produces output that matches your style and follows your rules without re-explaining.

---

## STEP 03 — MCP Servers (MCP)

**Goal:** Connect platforms: notes, code, tasks, search, calendar, Telegram.

**What happens:**
- Review `90-Operations/Setup/MCP Connection Plan.md` — which systems can connect.
- Review `90-Operations/Setup/MCP Readiness Report.md` — which env vars are set.
- Connect one source at a time, manual export first, then read-only API.
- Configure MCP servers in Claude Code settings (`~/.claude/settings.json`).

**Available connectors (connect in this order):**

| # | Server | What it does | First safe action | Config |
|---|--------|-------------|-------------------|--------|
| 1 | **Obsidian** | Read/write vault notes | Verify vault structure | `npx mcp-obsidian` |
| 2 | **Notion** | Import pages/databases | Read one approved page | `npx @notionhq/notion-mcp-server` |
| 3 | **Gmail** | Import email threads | Read one approved thread | Claude.ai built-in or MCP |
| 4 | **Google Calendar** | Read events and schedules | Read today's events | Claude.ai built-in or MCP |
| 5 | **Linear** | Tasks, issues, projects | List team issues | `npx @linear/mcp-server` |
| 6 | **GitHub** | Repos, issues, PRs | List repos | `gh` CLI (no MCP needed) |
| 7 | **Telegram** | Messages, bot interaction | Read one chat export | Custom bot or manual export |
| 8 | **Exa** | Web search, research | One search query | `npx @anthropic-ai/exa-mcp-server` |
| 9 | **Granola** | Meeting transcripts | Copy one transcript | Manual export to `70-Sources/Granola/` |
| 10 | **Crisp** | Support chat history | Export one conversation | Manual export or API |

**Safety rules:**
- One connector at a time.
- Manual export before API.
- Read-only scope first.
- Secrets stay outside the vault and outside git.
- Never scrape broad mailboxes/workspaces.
- Never auto-send messages.
- First import = one object + one source note in `70-Sources/`.

**How to start:**
```bash
# Check readiness
python3 scripts/mcp_readiness.py --vault "/path/to/ObsidianVault"

# Then use the guided prompt
# Paste 90-Operations/Setup/Connect Sources Prompt.md into Claude Code
```

**Example MCP config (`~/.claude/settings.json`):**
```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "/path/to/ObsidianVault"
      }
    },
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "ntn_..."
      }
    }
  }
}
```

**Done when:** At least 2-3 sources are connected and the agent can read from them.

---

## STEP 04 — Context (CTX)

**Goal:** Personal context, project context, contacts, notes, and files.

**What happens:**
- Write your personal context: who you are, what you do, what matters now.
- Write project context for each active project (Tech-Base structure).
- Import contacts, key people, stakeholders into `20-Areas/` or `30-Resources/`.
- Map all your notes and files into the vault or link to them.

**Deliverables:**
- `CLAUDE.md` with personal identity, values, goals, projects.
- `10-Projects/<PROJECT>/Tech-Base/` for each active project (TODO, MEMORY, CHANGELOG, MISTAKES).
- `70-Sources/` populated with imported context from connected sources.
- `20-Areas/` with ongoing responsibilities documented.

**Key context files:**
```
CLAUDE.md                              — who you are + how agents should work
10-Projects/<NAME>/Tech-Base/TODO.md   — current tasks
10-Projects/<NAME>/Tech-Base/MEMORY.md — what happened, what's next
70-Sources/Context Source Map.md       — where context lives
60-Rules/Agent Working Agreement.md    — the contract
```

**Done when:** A new agent session can read your context files and understand your situation without you re-explaining.

---

## STEP 05 — Skills (SK)

**Goal:** Repeatable capabilities: summaries, project management, reviews, audits, and strategy workflows.

**What happens:**
- Browse installed skill libraries in `30-Resources/claude-skills/` and `30-Resources/superpowers/`.
- Browse installed RIS Claude Code skills in `30-Resources/ris-claude-code/`.
- Pick 3-5 skills that match your workflow.
- Install custom skills into `~/.claude/skills/` or your project's skills folder.
- Create your own skills for repeating workflows.

**Installed libraries:**
- `claude-skills/` — Anthropic official: document workflows, structured research, code workflows.
- `superpowers/` — obra: composable reusable skills for coding agents.
- `ris-claude-code/` — CEO Council, Product Data Audit, GitHub Issues workflow.
- `Skills & Superpowers Guide.md` — local index with Exa, Claude Code docs, and MCP docs links.

**Skill examples to start with:**
| Skill | What it does | When to use |
|-------|-------------|-------------|
| Commit | Structured git commits | After each code change |
| Review | Code review workflow | Before merging PRs |
| Research | Web research with sources | Market analysis, competitor scan |
| Plan | Implementation planning | Before starting a feature |
| Summary | Structured summaries | After meetings, after reading |
| CEO Council | Multiple executive perspectives | High-leverage business/product decisions |
| Product Data Audit | Map data sources and decision loops | Before automating or changing a product |
| GitHub Issues | Durable task and session context | When using GitHub as an execution system |
| Exa | AI-native live web research | Market scans and source discovery |

**How to create a custom skill:**
```markdown
# ~/.claude/skills/my-skill/SKILL.md
---
name: weekly-summary
description: Generate a weekly summary of work done
---

Read git logs, Obsidian changelogs, and Linear issues for the past 7 days.
Output a structured summary with: done, blocked, next week, metrics.
```

**Done when:** You have 3+ skills/resources that save you time on repeating tasks and know when to use CEO Council, Product Data Audit, and GitHub Issues.

---

## STEP 06 — GitHub Sync (GH)

**Goal:** Backup, version history, issues, and agent memory for execution.

**What happens:**
- Create a private GitHub repo for your vault (or use git locally).
- Set up commit + push after meaningful changes.
- Use GitHub Issues as a task/memory system for agents.
- Connect GitHub Projects board for visual tracking.

**Setup:**
```bash
cd /path/to/ObsidianVault
git init
git remote add origin https://github.com/<you>/my-vault.git
git add -A && git commit -m "initial vault" && git push -u origin main
```

**Agent memory via GitHub Issues:**
```bash
# Create a task for the agent
gh issue create --title "Research competitors" --body "..." --repo <you>/agent-memory

# Agent reads its tasks
gh issue list --repo <you>/agent-memory --state open

# Agent reports progress
gh issue comment 1 --body "Done: found 5 competitors" --repo <you>/agent-memory
```

**Auto-save rule (add to CLAUDE.md):**
```markdown
After each completed step:
1. Update Obsidian files (TODO, MEMORY, CHANGELOG).
2. git add + commit + push.
3. Comment on the relevant GitHub issue.
```

**Done when:** Your vault has version history and agents can read/write GitHub issues.

---

## STEP 07 — Telegram Bot (TG)

**Goal:** A simple interface where people ask, answer, and receive output.

**What happens:**
- Create a Telegram bot via @BotFather.
- Connect the bot to your agent (Claude Code, custom script, or n8n).
- Bot can: receive questions, trigger agent tasks, return results.
- Optional: bot writes meeting notes, forwards context to vault.

**Minimal stack:**
```
Telegram → Bot API → Your script/n8n → Claude API → Response
                                      ↓
                              Obsidian vault (save context)
```

**Use cases:**
- Quick capture: send a message → note appears in `00-Inbox/`.
- Ask the agent: "What's my schedule today?" → reads calendar + vault.
- Forward a meeting transcript → saved to `70-Sources/Granola/`.
- Status check: "What's the status of project X?" → reads Tech-Base/MEMORY.md.

**Done when:** You can send a message to Telegram and get a useful response from the agent.

---

## STEP 08 — POS MVP (GO)

**Goal:** A small working system around your own tools and real work.

**What happens:**
- All 7 previous steps are working together.
- You use the system daily for real work, not just setup.
- The agent knows your context, follows your rules, uses your tools.
- You iterate: fix what's broken, remove what's unused, add what's missing.

**Definition of a working POS:**
- [ ] Obsidian vault is your single source of truth for notes and context.
- [ ] AI agent reads your context and produces useful output without re-explaining.
- [ ] 3+ external sources are connected (Notion, Gmail, Calendar, Linear, etc.).
- [ ] Personal and project context is documented and up to date.
- [ ] 3+ skills are installed and used regularly.
- [ ] Vault is version-controlled with git + GitHub.
- [ ] Telegram bot (or another interface) provides quick access.
- [ ] Post-task protocol runs automatically: notes, commits, issue updates.

**Metrics to track:**
- How many times per day you open Obsidian.
- How many agent sessions use context without re-explaining.
- How many tasks are completed through the system vs. outside it.

**Done when:** The system works for real work, not just as a demo.

---

## Summary

```
STEP 01  Obsidian     → vault + structure + rules
STEP 02  Claude/Codex → agent + working agreement + CLAUDE.md
STEP 03  MCP servers  → connect platforms one by one
STEP 04  Context      → personal + project + sources
STEP 05  Skills       → repeatable agent capabilities
STEP 06  GitHub sync  → backup + issues + agent memory
STEP 07  Telegram bot → simple interface for quick access
STEP 08  POS MVP      → everything works together on real work
```

Each step takes 1-3 days for a beginner. Total: 2-4 weeks to a working POS.
