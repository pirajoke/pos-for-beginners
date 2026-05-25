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
