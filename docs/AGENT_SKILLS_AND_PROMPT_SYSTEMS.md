# Agent Skills And Prompt Systems

This repo installs and documents a small starter library of reusable agent workflows. The goal is to keep the client out of one huge prompt and give them a clear menu of skills to use when relevant.

## Installed By `scripts/install_skills.py`

### Superpowers

Source: https://github.com/obra/superpowers

A composable skills framework and coding-agent methodology. Use it to learn how to split agent abilities into reusable workflows, avoid repeating the same instructions, and build a personal library of agent behaviors.

Installed into:

```text
30-Resources/superpowers/
```

### Claude Skills

Source: https://github.com/anthropics/skills

Official Agent Skills examples and specification. Good examples include document workflows, structured research, code workflows, and repeatable operational tasks.

Installed into:

```text
30-Resources/claude-skills/
```

### RIS Claude Code Skills

Source: https://github.com/serejaris/ris-claude-code

This provides the curated skills currently used in this POS starter:

- `skills/ceo-council/SKILL.md`
- `skills/product-data-audit/`
- `skills/gh-issues/`

Installed into:

```text
30-Resources/ris-claude-code/
```

## Recommended Skills

### CEO Council

Use when:

- the decision is high leverage;
- you need multiple independent executive perspectives;
- product, growth, or business strategy is unclear.

Source: https://github.com/serejaris/ris-claude-code/blob/main/skills/ceo-council/SKILL.md

### Product Data Audit

Use when:

- you need to understand a product before changing it;
- analytics, customer signals, and workflows are scattered;
- you want leverage points before building automations or agents.

Source: https://github.com/serejaris/ris-claude-code/tree/main/skills/product-data-audit

### GitHub Issues Management

Use when:

- creating tasks from chat;
- storing context for future sessions;
- tracking implementation status;
- connecting agent work to a durable task system.

Source: https://github.com/serejaris/ris-claude-code/tree/main/skills/gh-issues

## Search And Research

### Exa

Source: https://exa.ai

Use for:

- research agents;
- market scans;
- competitor research;
- technical reference discovery;
- enriching workflows with live web data.

Requires:

```text
EXA_API_KEY
```

### Claude Code Docs

Source: https://code.claude.com/docs

Use for:

- project memory;
- `CLAUDE.md`;
- terminal workflows;
- tool permissions;
- local agent work.

### Model Context Protocol

Source: https://modelcontextprotocol.io/docs/getting-started/intro

Use for:

- connecting AI apps to external tools and data sources;
- designing safe source connection flows;
- understanding MCP servers and clients.

## Rule

Install reference libraries into the vault. Activate or copy specific skills into Claude Code only after the client chooses which workflows they actually need.
