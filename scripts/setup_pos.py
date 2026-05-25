#!/usr/bin/env python3
"""
POS FOR BEGINNERS — Interactive 8-step setup wizard.

Guides the client through all 8 steps automatically.
Run: python3 scripts/setup_pos.py --vault "/path/to/ObsidianVault"
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, ensure_parent, now_stamp, safe_write, slug, today
from autoconnect import (
    autoconnect, format_status, get_status,
    ZERO_CONFIG_SERVERS, KEY_SERVERS, BUILTIN_SERVERS,
)

# ── UI helpers ───────────────────────────────────────────────────

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"


def banner(step: int, title: str, tag: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"{BOLD}{CYAN}STEP {step:02d}{RESET} — {BOLD}{title}{RESET}  {DIM}[{tag}]{RESET}")
    print(f"{'─' * 60}\n")


def ok(msg: str) -> None:
    print(f"  {GREEN}✓{RESET} {msg}")


def warn(msg: str) -> None:
    print(f"  {YELLOW}!{RESET} {msg}")


def fail(msg: str) -> None:
    print(f"  {RED}✗{RESET} {msg}")


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"  → {prompt}{suffix}: ").strip()
    except EOFError:
        return default
    return answer or default


def ask_yn(prompt: str, default: bool = True) -> bool:
    hint = "Y/n" if default else "y/N"
    try:
        answer = input(f"  → {prompt} [{hint}]: ").strip().lower()
    except EOFError:
        return default
    if not answer:
        return default
    return answer in ("y", "yes", "да", "д")


def run(args: list[str], check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(args, check=check, capture_output=capture, text=True)


def run_script(script: str, extra_args: list[str] | None = None) -> bool:
    cmd = [sys.executable, f"scripts/{script}"] + (extra_args or [])
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"{script} failed: {result.stderr.strip()[:200]}")
        return False
    return True


def has_command(name: str) -> bool:
    return shutil.which(name) is not None


def load_progress(vault: Path) -> dict:
    path = vault / "90-Operations" / "Setup" / "pos-progress.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"completed_steps": [], "started": today(), "last_updated": today()}


def save_progress(vault: Path, progress: dict) -> None:
    progress["last_updated"] = today()
    path = vault / "90-Operations" / "Setup" / "pos-progress.json"
    ensure_parent(path)
    path.write_text(json.dumps(progress, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def step_done(progress: dict, step: int) -> bool:
    return step in progress["completed_steps"]


def mark_done(vault: Path, progress: dict, step: int) -> None:
    if step not in progress["completed_steps"]:
        progress["completed_steps"].append(step)
    save_progress(vault, progress)
    ok(f"Step {step:02d} marked complete.")


# ── STEP 01: Obsidian ───────────────────────────────────────────

def step_01_obsidian(vault: Path, progress: dict, allow_non_obsidian: bool) -> bool:
    banner(1, "Obsidian", "OB")

    if step_done(progress, 1):
        ok("Already completed. Skipping.")
        return True

    print("  Creating vault structure...")
    args = ["--vault", str(vault)]
    if allow_non_obsidian:
        args.append("--allow-non-obsidian")

    if not run_script("install.py", args):
        return False
    ok("Vault structure created.")

    run_script("doctor.py", ["--vault", str(vault)])
    ok("System doctor report generated.")

    run_script("mcp_readiness.py", ["--vault", str(vault)])
    ok("MCP readiness report generated.")

    run_script("source_discovery.py", ["--vault", str(vault)])
    ok("Source discovery completed.")

    run_script("generate_context_pack.py", ["--vault", str(vault)])
    ok("Context pack generated.")

    mark_done(vault, progress, 1)
    print(f"\n  {BOLD}Next:{RESET} Open Obsidian and look at your vault.")
    print(f"  Start with: {CYAN}START HERE - POS FOR BEGINNERS Setup.md{RESET}")
    return True


# ── STEP 02: Claude / Codex ─────────────────────────────────────

def step_02_claude(vault: Path, progress: dict) -> bool:
    banner(2, "Claude / Codex", "AI")

    if step_done(progress, 2):
        ok("Already completed. Skipping.")
        return True

    # Check for Claude Code or Codex
    has_claude = has_command("claude")
    has_codex = has_command("codex")

    if has_claude:
        ok(f"Claude Code found: {shutil.which('claude')}")
    else:
        warn("Claude Code not found.")
        if ask_yn("Install Claude Code now? (npm install -g @anthropic-ai/claude-code)"):
            result = run(["npm", "install", "-g", "@anthropic-ai/claude-code"], check=False)
            if result.returncode == 0:
                ok("Claude Code installed.")
            else:
                warn("Installation failed. You can install it manually later.")

    if has_codex:
        ok(f"Codex found: {shutil.which('codex')}")

    # Generate CLAUDE.md if not exists
    claude_md = vault / "CLAUDE.md"
    if not claude_md.exists():
        print("\n  Let's create your personal CLAUDE.md (agent instructions).\n")

        name = ask("Your name")
        role = ask("Your role (e.g. PM, developer, student, founder)", "builder")
        language = ask("Preferred language for communication", "English")
        projects = ask("Active projects (comma-separated)", "")
        avoid = ask("What should the agent never do?", "Don't overwrite my files without asking")

        claude_content = f"""# Agent Instructions

## Who I Am
- Name: {name}
- Role: {role}
- Language: {language}

## Active Projects
{chr(10).join(f'- {p.strip()}' for p in projects.split(',') if p.strip()) if projects else '- [ASK ME]'}

## Communication
- Respond in {language}.
- Keep answers short and to the point.
- Ask one question at a time.

## Rules
- {avoid}
- If something is unknown, write [ASK ME].
- Follow the Post-Task Protocol after each task.
- Update Obsidian files (TODO, MEMORY, CHANGELOG) after meaningful steps.

## Vault
- Source of truth: this Obsidian vault at `{vault}`
- Rules: `60-Rules/`
- Sources: `70-Sources/`
- Logs: `90-Operations/`
"""
        safe_write(claude_md, claude_content, force=True)
        ok(f"Created {claude_md}")
    else:
        ok("CLAUDE.md already exists.")

    # Copy interview prompts
    agreement = vault / "60-Rules" / "Agent Working Agreement.md"
    if "[ASK ME]" in agreement.read_text(encoding="utf-8"):
        print(f"\n  {YELLOW}Agent Working Agreement still has [ASK ME] placeholders.{RESET}")
        print(f"  Run the full interview by pasting this into Claude Code:")
        print(f"  {CYAN}90-Operations/Setup/Claude First Run.md{RESET}")

    mark_done(vault, progress, 2)
    return True


# ── STEP 03: MCP Servers (auto-connect) ────────────────────────

def step_03_mcp(vault: Path, progress: dict) -> bool:
    banner(3, "MCP Servers", "MCP")

    if step_done(progress, 3):
        ok("Already completed. Skipping.")
        return True

    print("  Auto-configuring MCP servers...\n")

    # Collect optional API keys interactively
    extra_keys: dict[str, str] = {}
    for srv in KEY_SERVERS:
        env_val = os.environ.get(srv["env_key"], "")
        if env_val:
            ok(f"{srv['name']}: key found in environment ({srv['env_key']})")
            extra_keys[srv["env_key"]] = env_val
        else:
            key = ask(f"{srv['name']} API key ({srv['env_key']}, Enter to skip)")
            if key:
                extra_keys[srv["env_key"]] = key

    # Run autoconnect
    summary = autoconnect(
        vault,
        write_global=True,
        create_remote=False,
        extra_keys=extra_keys if extra_keys else None,
    )

    # Report what was configured
    print()
    print(f"  {BOLD}Auto-configured:{RESET}")
    for sid in summary["mcp_configured"]:
        ok(f"{sid}")

    if summary["mcp_needs_key"]:
        print(f"\n  {YELLOW}Skipped (no API key):{RESET}")
        for s in summary["mcp_needs_key"]:
            warn(f"{s['name']} — set {s['env_key']} and re-run")

    print(f"\n  {DIM}Built-in (approve in app):{RESET}")
    for srv in BUILTIN_SERVERS:
        print(f"    {CYAN}i{RESET} {srv['name']}: {srv['note']}")

    print(f"\n  {BOLD}Settings written:{RESET}")
    ok(f"Project: {vault}/.claude/settings.json")
    if summary.get("global_path"):
        ok(f"Global:  ~/.claude/settings.json")
    if summary.get("codex_path"):
        ok(f"Codex:   {summary['codex_path']}")

    print(f"\n  {GREEN}{BOLD}How it works:{RESET}")
    print(f"  1. Open this vault folder in Claude Code or Codex")
    print(f"  2. The app detects MCP servers from .claude/settings.json")
    print(f"  3. You'll see an approval prompt for each server")
    print(f"  4. Click 'Approve' — done, server is connected")
    print(f"  {DIM}No manual config needed. Everything is pre-configured.{RESET}")

    # Update MCP readiness report
    run_script("mcp_readiness.py", ["--vault", str(vault)])

    mark_done(vault, progress, 3)
    return True


# ── STEP 04: Context ────────────────────────────────────────────

def step_04_context(vault: Path, progress: dict) -> bool:
    banner(4, "Context", "CTX")

    if step_done(progress, 4):
        ok("Already completed. Skipping.")
        return True

    print("  Let's set up your project context.\n")

    # Check existing projects
    projects_dir = vault / "10-Projects"
    existing = [d.name for d in projects_dir.iterdir() if d.is_dir() and d.name != "_Example Project"] if projects_dir.exists() else []

    if existing:
        ok(f"Existing projects: {', '.join(existing)}")
    else:
        print("  No projects found yet.\n")

    # Create projects
    while True:
        raw_name = ask("New project name (or press Enter to finish)")
        if not raw_name:
            break

        project_name = slug(raw_name) or "untitled"
        if raw_name != project_name:
            ok(f"Sanitized to: {project_name}")

        project_dir = projects_dir / project_name / "Tech-Base"
        project_dir.mkdir(parents=True, exist_ok=True)

        description = ask(f"  One-line description for '{project_name}'", "[ASK ME]")
        status = ask(f"  Status (active/paused/done)", "active")

        safe_write(project_dir / "TODO.md", f"# TODO — {project_name}\n\n- [ ] Define first tasks\n")
        safe_write(project_dir / "MEMORY.md", f"# MEMORY — {project_name}\n\n## Description\n\n{description}\n\n## Status\n\n{status}\n\n## NEXT STEP\n\n- [ASK ME]\n\n## Last Completed\n\n- Created project structure ({today()})\n")
        safe_write(project_dir / "CHANGELOG.md", f"# CHANGELOG — {project_name}\n\n- {today()}: Project created.\n")
        safe_write(project_dir / "MISTAKES.md", f"# MISTAKES — {project_name}\n\nRecord repeated errors, blockers, and lessons here.\n")
        safe_write(projects_dir / project_name / "README.md", f"# {project_name}\n\n{description}\n\nStatus: {status}\n")

        ok(f"Project '{project_name}' created with Tech-Base structure.")

    # Check areas
    areas_dir = vault / "20-Areas"
    print()
    while True:
        raw_area = ask("Area of responsibility (e.g. health, finance, career — Enter to finish)")
        if not raw_area:
            break
        area_name = slug(raw_area) or "untitled"
        area_file = areas_dir / f"{area_name}.md"
        safe_write(area_file, f"# {area_name}\n\nType: area\nStatus: active\n\n## Notes\n\n- [ASK ME]\n")
        ok(f"Area '{area_name}' created.")

    # Regenerate context pack
    run_script("generate_context_pack.py", ["--vault", str(vault)])
    ok("Context pack regenerated.")

    mark_done(vault, progress, 4)
    return True


# ── STEP 05: Skills ─────────────────────────────────────────────

def step_05_skills(vault: Path, progress: dict) -> bool:
    banner(5, "Skills", "SK")

    if step_done(progress, 5):
        ok("Already completed. Skipping.")
        return True

    print("  Installing skill libraries...\n")

    if run_script("install_skills.py", ["--vault", str(vault)]):
        ok("Claude Skills (Anthropic) installed → 30-Resources/claude-skills/")
        ok("Superpowers (obra) installed → 30-Resources/superpowers/")
    else:
        warn("Skills installation failed. Check your internet connection.")
        warn("You can run manually: python3 scripts/install_skills.py --vault ...")
        return True

    # Show what's available
    skills_dir = vault / "30-Resources" / "claude-skills" / "skills"
    superpowers_dir = vault / "30-Resources" / "superpowers" / "skills"

    if skills_dir.exists():
        skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
        if skills:
            print(f"\n  Available Claude Skills: {', '.join(skills[:10])}")

    if superpowers_dir.exists():
        powers = [d.name for d in superpowers_dir.iterdir() if d.is_dir()]
        if powers:
            print(f"  Available Superpowers: {', '.join(powers[:10])}")

    # Custom skills directory
    custom_skills = Path.home() / ".claude" / "skills"
    if not custom_skills.exists():
        if ask_yn("\n  Create ~/.claude/skills/ for your custom skills?"):
            custom_skills.mkdir(parents=True, exist_ok=True)
            ok(f"Created {custom_skills}")
            # Create an example skill
            example = custom_skills / "example-skill" / "SKILL.md"
            ensure_parent(example)
            safe_write(example, """---
name: example-skill
description: Example skill template — replace with your own
---

This is a template. Create your own skills by:
1. Creating a folder in ~/.claude/skills/
2. Adding a SKILL.md with frontmatter (name, description)
3. Writing instructions for the agent
""")
            ok("Example skill template created.")

    mark_done(vault, progress, 5)
    return True


# ── STEP 06: GitHub Sync (auto-connect) ────────────────────────

def step_06_github(vault: Path, progress: dict) -> bool:
    banner(6, "GitHub Sync", "GH")

    if step_done(progress, 6):
        ok("Already completed. Skipping.")
        return True

    if not has_command("git"):
        fail("git not found. Install git first.")
        return False

    print("  Auto-configuring git and GitHub...\n")

    # Check current state
    status = get_status(vault)
    git_info = status["git"]

    # Auto-setup git + POS upstream (done by autoconnect in step 03, but ensure it's there)
    from autoconnect import setup_git
    create_repo = False

    if has_command("gh") and not git_info.get("vault_remote"):
        create_repo = ask_yn("Create a private GitHub repo for your vault?")

    git_result = setup_git(vault, create_remote=create_repo)

    # Report
    if git_result.get("initialized"):
        ok("Git repository ready.")
    if git_result.get("initial_commit"):
        ok("Initial commit created.")
    if git_result.get("pos_upstream"):
        ok(f"POS FOR BEGINNERS linked as 'pos-upstream' remote")
        print(f"    {DIM}Update vault tools: git fetch pos-upstream && git merge pos-upstream/main{RESET}")
    if git_result.get("vault_remote"):
        ok(f"Vault repo: {git_result['vault_remote']}")
    elif not create_repo:
        print(f"\n  {DIM}No remote repo created. You can add one later:{RESET}")
        print(f"  {DIM}  gh repo create my-vault --private --source {vault} --push{RESET}")

    # Commit current state
    if git_result.get("initialized") and not git_result.get("initial_commit"):
        # Vault existed before — commit new changes from setup
        r = subprocess.run(
            ["git", "-C", str(vault), "status", "--porcelain"],
            capture_output=True, text=True,
        )
        if r.stdout.strip():
            run(["git", "-C", str(vault), "add", "-A"], check=False)
            run(["git", "-C", str(vault), "commit", "-m", f"POS setup update {today()}"], check=False)
            ok("Changes committed.")

            if git_result.get("vault_remote"):
                run(["git", "-C", str(vault), "push", "-u", "origin", "main"], check=False)
                ok("Pushed to remote.")

    mark_done(vault, progress, 6)
    return True


# ── STEP 07: Telegram Bot ───────────────────────────────────────

def step_07_telegram(vault: Path, progress: dict) -> bool:
    banner(7, "Telegram Bot", "TG")

    if step_done(progress, 7):
        ok("Already completed. Skipping.")
        return True

    print("  The Telegram bot connects your system to a chat interface.\n")
    print(f"  {DIM}Architecture: Telegram → Bot API → Script/n8n → Claude API → Obsidian{RESET}\n")

    token = ask("Telegram bot token (from @BotFather, or Enter to skip)")

    if not token:
        warn("Skipping Telegram bot setup.")
        warn("When ready: message @BotFather on Telegram, create a bot, get the token.")
        if ask_yn("Mark this step as done anyway?", default=False):
            mark_done(vault, progress, 7)
        else:
            save_progress(vault, progress)
        return True

    # Save token reference (not the token itself!)
    bot_config = vault / "90-Operations" / "Setup" / "telegram-bot-config.md"
    safe_write(bot_config, f"""# Telegram Bot Config

Bot token is set. Do NOT store the actual token in Obsidian or git.

## Setup Date
{today()}

## Where the token lives
Environment variable: TELEGRAM_BOT_TOKEN
Or in a local config file outside this vault.

## Next Steps
1. Create a simple bot script or n8n workflow.
2. Connect to Claude API for responses.
3. Test: send a message → get a response.
4. Add vault read/write for context.
""", force=True)

    ok("Bot config reference saved (token NOT stored in vault).")
    print(f"\n  {BOLD}To test your bot:{RESET}")
    print(f"  export TELEGRAM_BOT_TOKEN='{token[:10]}...'")
    print(f"  Then build a handler script or use n8n.\n")

    mark_done(vault, progress, 7)
    return True


# ── STEP 08: POS MVP ────────────────────────────────────────────

def step_08_pos_mvp(vault: Path, progress: dict) -> bool:
    banner(8, "POS MVP", "GO")

    if step_done(progress, 8):
        ok("Already completed. Congratulations!")
        return True

    completed = progress["completed_steps"]
    total = 7
    done = len([s for s in range(1, 8) if s in completed])

    print(f"  Progress: {done}/{total} steps completed.\n")

    checklist = [
        (1, "Obsidian vault is your source of truth for notes and context"),
        (2, "AI agent reads your context without re-explaining"),
        (3, "3+ external sources connected (Notion, Gmail, Calendar, etc.)"),
        (4, "Personal and project context documented and up to date"),
        (5, "3+ skills installed and used regularly"),
        (6, "Vault version-controlled with git + GitHub"),
        (7, "Telegram bot (or another interface) for quick access"),
    ]

    all_done = True
    for step, desc in checklist:
        if step in completed:
            print(f"  {GREEN}[✓]{RESET} Step {step:02d}: {desc}")
        else:
            print(f"  {RED}[ ]{RESET} Step {step:02d}: {desc}")
            all_done = False

    if all_done:
        print(f"\n  {GREEN}{BOLD}All steps complete!{RESET}")
        print(f"  Your POS is ready. Use it for real work.\n")

        # Generate final summary
        summary = vault / "90-Operations" / "Setup" / "POS MVP Summary.md"
        safe_write(summary, f"""# POS MVP — Ready

## Completed
- All 8 steps finished on {today()}.
- Started: {progress.get('started', 'unknown')}

## System
- Vault: `{vault}`
- Steps completed: {', '.join(str(s) for s in sorted(completed))}

## What to do now
1. Use the system daily for real work.
2. Fix what's broken, remove what's unused.
3. Add new skills as you discover repeating workflows.
4. Keep CLAUDE.md and project context up to date.
5. Review weekly: what worked, what didn't.
""", force=True)

        mark_done(vault, progress, 8)
        ok("POS MVP summary saved.")
    else:
        print(f"\n  {YELLOW}Complete the remaining steps first.{RESET}")
        print(f"  Re-run: python3 scripts/setup_pos.py --vault \"{vault}\"\n")

    return True


# ── MAIN ─────────────────────────────────────────────────────────

def print_status(progress: dict) -> None:
    steps = [
        (1, "Obsidian", "OB"),
        (2, "Claude/Codex", "AI"),
        (3, "MCP Servers", "MCP"),
        (4, "Context", "CTX"),
        (5, "Skills", "SK"),
        (6, "GitHub Sync", "GH"),
        (7, "Telegram Bot", "TG"),
        (8, "POS MVP", "GO"),
    ]
    print(f"\n{BOLD}POS FOR BEGINNERS — Setup Progress{RESET}\n")
    for num, name, tag in steps:
        done = num in progress["completed_steps"]
        mark = f"{GREEN}✓{RESET}" if done else f"{DIM}○{RESET}"
        print(f"  {mark}  Step {num:02d}  {name} [{tag}]")
    completed = len(progress["completed_steps"])
    print(f"\n  {completed}/8 steps completed.\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="POS FOR BEGINNERS — Interactive 8-step setup wizard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/setup_pos.py --vault ~/ObsidianVault
  python3 scripts/setup_pos.py --vault ~/ObsidianVault --step 3
  python3 scripts/setup_pos.py --vault ~/ObsidianVault --status
        """,
    )
    parser.add_argument("--vault", required=True, help="Path to your Obsidian vault")
    parser.add_argument("--step", type=int, help="Jump to a specific step (1-8)")
    parser.add_argument("--status", action="store_true", help="Show current progress and exit")
    parser.add_argument("--allow-non-obsidian", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()

    # ── iCloud / permission check ────────────────────────
    is_icloud = "iCloud" in str(vault) or "Mobile Documents" in str(vault)
    if is_icloud:
        warn(f"Vault is inside iCloud: {vault}")
        print(f"  {YELLOW}macOS blocks Terminal/Codex from writing to iCloud folders.{RESET}")
        print(f"  {YELLOW}You'll get 'Operation not permitted' unless you fix this.{RESET}")
        print()
        print(f"  {BOLD}Two options:{RESET}")
        print()
        print(f"  {CYAN}Option A:{RESET} Grant Full Disk Access (recommended)")
        print(f"    1. Open System Settings → Privacy & Security → Full Disk Access")
        print(f"    2. Click + and add Terminal (or the app running this script)")
        print(f"    3. Restart Terminal and re-run this command")
        print()
        print(f"  {CYAN}Option B:{RESET} Use a vault outside iCloud")
        alt = ask("Alternative vault path (or Enter to try iCloud anyway)", "")
        if alt:
            vault = Path(alt).expanduser().resolve()
            print(f"  Using: {vault}")

    # Ensure vault dir exists
    try:
        vault.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        fail(f"Cannot create directory: {vault}")
        fail("Permission denied. See iCloud/Full Disk Access instructions above.")
        return 1

    # Quick write test
    test_file = vault / ".pos-write-test"
    try:
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink()
    except (PermissionError, OSError) as e:
        fail(f"Cannot write to vault: {e}")
        if is_icloud:
            fail("iCloud folder is blocked. Grant Full Disk Access or use a different path.")
        else:
            fail("Check folder permissions.")
        return 1

    progress = load_progress(vault)

    if args.status:
        print_status(progress)
        return 0

    print(f"\n{BOLD}{'═' * 60}{RESET}")
    print(f"{BOLD}  POS FOR BEGINNERS — Setup Wizard{RESET}")
    print(f"{BOLD}{'═' * 60}{RESET}")
    print(f"  Vault: {vault}")
    print(f"  Started: {progress.get('started', today())}")

    print_status(progress)

    steps = [
        (1, step_01_obsidian),
        (2, step_02_claude),
        (3, step_03_mcp),
        (4, step_04_context),
        (5, step_05_skills),
        (6, step_06_github),
        (7, step_07_telegram),
        (8, step_08_pos_mvp),
    ]

    # If specific step requested, jump there
    if args.step:
        for num, func in steps:
            if num == args.step:
                if num == 1:
                    func(vault, progress, args.allow_non_obsidian)
                else:
                    func(vault, progress)
                return 0
        fail(f"Unknown step: {args.step}")
        return 1

    # Otherwise, run from first incomplete step
    for num, func in steps:
        if step_done(progress, num):
            continue

        if num == 1:
            if not func(vault, progress, args.allow_non_obsidian):
                return 1
        else:
            if not func(vault, progress):
                return 1

        # After each step, ask to continue
        if num < 8 and not step_done(progress, num + 1):
            print()
            if not ask_yn(f"Continue to Step {num + 1:02d}?"):
                print(f"\n  {DIM}Paused. Re-run to continue from Step {num + 1:02d}.{RESET}")
                print(f"  python3 scripts/setup_pos.py --vault \"{vault}\"\n")
                return 0

    # Final
    append_implementation_log(vault, "setup_pos_complete", [
        f"steps={','.join(str(s) for s in sorted(progress['completed_steps']))}",
        f"started={progress.get('started', 'unknown')}",
        f"finished={today()}",
    ])

    print(f"\n{GREEN}{BOLD}  Setup complete. Your POS is ready.{RESET}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
