#!/usr/bin/env python3
"""
autoconnect.py — Auto-configure MCP servers and git for a POS vault.

Writes project-level .claude/settings.json so Claude Code / Codex
prompts the client for approval when they open the vault.
No terminal prompts for zero-config servers.

Usage:
  python3 scripts/autoconnect.py --vault ~/ObsidianVault
  python3 scripts/autoconnect.py --vault ~/ObsidianVault --global   # also write global settings
  python3 scripts/autoconnect.py --vault ~/ObsidianVault --status   # show what's configured
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, ensure_parent, now_stamp, safe_write, today

POS_REPO = "https://github.com/pirajoke/pos-for-beginners.git"

# ── MCP Server Registry ─────────────────────────────────────────

# Zero-config: no API key needed, auto-installed
ZERO_CONFIG_SERVERS = [
    {
        "id": "obsidian",
        "name": "Obsidian",
        "description": "Read/write notes in your vault",
        "config": lambda vault: {
            "command": "npx",
            "args": ["-y", "mcp-obsidian"],
            "env": {"OBSIDIAN_VAULT_PATH": str(vault)},
        },
    },
    {
        "id": "linear",
        "name": "Linear",
        "description": "Task and issue tracking (OAuth in-app)",
        "config": lambda vault: {
            "type": "http",
            "url": "https://mcp.linear.app/mcp",
        },
    },
]

# Key-required: need an API key or token, configured if available
KEY_SERVERS = [
    {
        "id": "notion",
        "name": "Notion",
        "description": "Workspace/page import",
        "env_key": "NOTION_TOKEN",
        "config": lambda vault, key: {
            "command": "npx",
            "args": ["-y", "@notionhq/notion-mcp-server"],
            "env": {"NOTION_TOKEN": key},
        },
    },
    {
        "id": "exa",
        "name": "Exa Search",
        "description": "AI-native web search",
        "env_key": "EXA_API_KEY",
        "config": lambda vault, key: {
            "command": "npx",
            "args": ["-y", "@anthropic-ai/exa-mcp-server"],
            "env": {"EXA_API_KEY": key},
        },
    },
]

# Built-in to Claude.ai / Codex — no MCP config needed, just a note
BUILTIN_SERVERS = [
    {"id": "gmail", "name": "Gmail", "note": "Built-in to Claude.ai — approve in app"},
    {"id": "google-calendar", "name": "Google Calendar", "note": "Built-in to Claude.ai — approve in app"},
    {"id": "github", "name": "GitHub", "note": "Uses gh CLI — install: brew install gh && gh auth login"},
]


# ── Tool detection ───────────────────────────────────────────────

def detect_tools() -> dict:
    """Detect available CLI tools."""
    tools = {}
    for name in ("claude", "codex", "git", "gh", "node", "npx"):
        path = shutil.which(name)
        tools[name] = {"available": path is not None, "path": path}
    return tools


# ── MCP config builder ──────────────────────────────────────────

def build_mcp_servers(vault: Path) -> dict:
    """Build the mcpServers dict from registry + environment."""
    servers = {}

    # Zero-config — always included
    for srv in ZERO_CONFIG_SERVERS:
        servers[srv["id"]] = srv["config"](vault)

    # Key-required — included only if key available in env
    for srv in KEY_SERVERS:
        key = os.environ.get(srv["env_key"], "")
        if key:
            servers[srv["id"]] = srv["config"](vault, key)

    return servers


def build_mcp_servers_with_keys(vault: Path, keys: dict[str, str]) -> dict:
    """Build mcpServers with explicitly provided keys."""
    servers = {}

    for srv in ZERO_CONFIG_SERVERS:
        servers[srv["id"]] = srv["config"](vault)

    for srv in KEY_SERVERS:
        key = keys.get(srv["env_key"], "") or os.environ.get(srv["env_key"], "")
        if key:
            servers[srv["id"]] = srv["config"](vault, key)

    return servers


# ── Project-level settings ───────────────────────────────────────

def write_project_settings(vault: Path, extra_servers: dict | None = None) -> Path:
    """
    Write .claude/settings.json inside the vault (project-level).
    Claude Code reads this when the vault is opened as a project.
    Merges with existing settings if present.
    """
    settings_dir = vault / ".claude"
    settings_path = settings_dir / "settings.json"

    # Load existing
    settings: dict = {}
    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    # Build MCP servers
    mcp = build_mcp_servers(vault)
    if extra_servers:
        mcp.update(extra_servers)

    # Merge — don't overwrite existing server configs
    if "mcpServers" not in settings:
        settings["mcpServers"] = {}
    for sid, config in mcp.items():
        if sid not in settings["mcpServers"]:
            settings["mcpServers"][sid] = config

    # Write
    ensure_parent(settings_path)
    settings_path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    settings_path.chmod(0o600)

    # Ensure .claude is gitignored (contains potential secrets in env)
    gitignore = vault / ".gitignore"
    gitignore_content = ""
    if gitignore.exists():
        gitignore_content = gitignore.read_text(encoding="utf-8")
    if ".claude/settings.json" not in gitignore_content:
        with gitignore.open("a", encoding="utf-8") as f:
            if not gitignore_content.endswith("\n"):
                f.write("\n")
            f.write("# Claude Code project settings (may contain MCP tokens)\n")
            f.write(".claude/settings.json\n")
            f.write(".claude/settings.local.json\n")

    return settings_path


def write_global_settings(vault: Path) -> Path | None:
    """
    Merge MCP servers into global ~/.claude/settings.json.
    Only adds servers not already configured.
    """
    global_path = Path.home() / ".claude" / "settings.json"

    settings: dict = {}
    if global_path.exists():
        try:
            settings = json.loads(global_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            settings = {}

    if "mcpServers" not in settings:
        settings["mcpServers"] = {}

    mcp = build_mcp_servers(vault)
    added = 0
    for sid, config in mcp.items():
        if sid not in settings["mcpServers"]:
            settings["mcpServers"][sid] = config
            added += 1

    if added == 0:
        return None

    ensure_parent(global_path)
    global_path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    global_path.chmod(0o600)
    return global_path


# ── Codex settings ───────────────────────────────────────────────

def write_codex_settings(vault: Path) -> Path | None:
    """Write codex.json if Codex CLI is available."""
    if not shutil.which("codex"):
        return None

    codex_path = vault / "codex.json"
    if codex_path.exists():
        return codex_path

    # Codex uses a similar but different format
    config = {
        "model": "o3",
        "instructions": f"Read CLAUDE.md for project context. Vault path: {vault}",
        "mcpServers": {},
    }

    for srv in ZERO_CONFIG_SERVERS:
        cfg = srv["config"](vault)
        if "command" in cfg:
            config["mcpServers"][srv["id"]] = cfg

    codex_path.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return codex_path


# ── Git setup ────────────────────────────────────────────────────

def setup_git(vault: Path, create_remote: bool = False) -> dict:
    """
    Initialize git in the vault and link POS FOR BEGINNERS as upstream.
    Optionally create a private GitHub repo for the vault.
    """
    result = {
        "initialized": False,
        "pos_upstream": False,
        "vault_remote": None,
        "initial_commit": False,
    }

    if not shutil.which("git"):
        return result

    git_dir = vault / ".git"

    # Init if needed
    if not git_dir.exists():
        subprocess.run(["git", "-C", str(vault), "init"], check=False, capture_output=True)
        result["initialized"] = True

        # Create .gitignore if not exists
        gitignore = vault / ".gitignore"
        if not gitignore.exists():
            safe_write(gitignore, """.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
.DS_Store
*.tmp
node_modules/
.claude/settings.json
.claude/settings.local.json
""")
        # Initial commit
        subprocess.run(["git", "-C", str(vault), "add", "-A"], check=False, capture_output=True)
        subprocess.run(
            ["git", "-C", str(vault), "commit", "-m", "initial vault setup via POS FOR BEGINNERS"],
            check=False, capture_output=True,
        )
        result["initial_commit"] = True
    else:
        result["initialized"] = True

    # Add POS FOR BEGINNERS as upstream remote (for pulling updates)
    remotes = subprocess.run(
        ["git", "-C", str(vault), "remote"], capture_output=True, text=True
    )
    existing_remotes = remotes.stdout.strip().split("\n") if remotes.stdout.strip() else []

    if "pos-upstream" not in existing_remotes:
        r = subprocess.run(
            ["git", "-C", str(vault), "remote", "add", "pos-upstream", POS_REPO],
            check=False, capture_output=True,
        )
        if r.returncode == 0:
            result["pos_upstream"] = True
    else:
        result["pos_upstream"] = True

    # Check for origin remote
    if "origin" in existing_remotes:
        origin = subprocess.run(
            ["git", "-C", str(vault), "remote", "get-url", "origin"],
            capture_output=True, text=True,
        )
        result["vault_remote"] = origin.stdout.strip() if origin.returncode == 0 else None

    # Create private GitHub repo if requested and gh is available
    elif create_remote and shutil.which("gh"):
        vault_name = vault.name or "my-vault"
        repo_name = re.sub(r'[^a-zA-Z0-9._-]', '-', vault_name)
        r = subprocess.run(
            ["gh", "repo", "create", repo_name, "--private", "--source", str(vault), "--push"],
            check=False, capture_output=True, text=True,
        )
        if r.returncode == 0:
            # Get the remote URL
            origin = subprocess.run(
                ["git", "-C", str(vault), "remote", "get-url", "origin"],
                capture_output=True, text=True,
            )
            result["vault_remote"] = origin.stdout.strip() if origin.returncode == 0 else repo_name

    return result


# ── Status report ────────────────────────────────────────────────

def get_status(vault: Path) -> dict:
    """Get current autoconnect status for a vault."""
    status = {
        "tools": detect_tools(),
        "mcp_project": {},
        "mcp_global": {},
        "git": {
            "initialized": (vault / ".git").exists(),
            "pos_upstream": False,
            "vault_remote": None,
        },
    }

    # Project-level MCP
    proj_settings = vault / ".claude" / "settings.json"
    if proj_settings.exists():
        try:
            data = json.loads(proj_settings.read_text(encoding="utf-8"))
            status["mcp_project"] = data.get("mcpServers", {})
        except json.JSONDecodeError:
            pass

    # Global MCP
    global_settings = Path.home() / ".claude" / "settings.json"
    if global_settings.exists():
        try:
            data = json.loads(global_settings.read_text(encoding="utf-8"))
            status["mcp_global"] = data.get("mcpServers", {})
        except json.JSONDecodeError:
            pass

    # Git remotes
    if status["git"]["initialized"]:
        remotes = subprocess.run(
            ["git", "-C", str(vault), "remote", "-v"],
            capture_output=True, text=True,
        )
        if remotes.returncode == 0:
            for line in remotes.stdout.strip().split("\n"):
                if line.startswith("pos-upstream"):
                    status["git"]["pos_upstream"] = True
                if line.startswith("origin"):
                    status["git"]["vault_remote"] = line.split()[1]

    return status


def format_status(vault: Path) -> str:
    """Format status as readable text."""
    s = get_status(vault)
    lines = [f"\n  === Autoconnect Status: {vault} ===\n"]

    # Tools
    lines.append("  Tools:")
    for name, info in s["tools"].items():
        mark = "\033[92m+\033[0m" if info["available"] else "\033[91m-\033[0m"
        lines.append(f"    {mark} {name}")

    # Project MCP
    lines.append(f"\n  Project MCP (.claude/settings.json): {len(s['mcp_project'])} server(s)")
    for sid in s["mcp_project"]:
        lines.append(f"    \033[92m+\033[0m {sid}")

    # Missing servers
    all_ids = {srv["id"] for srv in ZERO_CONFIG_SERVERS + KEY_SERVERS}
    missing = all_ids - set(s["mcp_project"].keys())
    if missing:
        lines.append(f"\n  Not yet configured:")
        for sid in sorted(missing):
            lines.append(f"    \033[2m-\033[0m {sid}")

    # Built-in
    lines.append(f"\n  Built-in (no config needed):")
    for srv in BUILTIN_SERVERS:
        lines.append(f"    \033[96mi\033[0m {srv['name']}: {srv['note']}")

    # Git
    lines.append(f"\n  Git:")
    lines.append(f"    init: {'yes' if s['git']['initialized'] else 'no'}")
    lines.append(f"    pos-upstream: {'linked' if s['git']['pos_upstream'] else 'not linked'}")
    lines.append(f"    origin: {s['git']['vault_remote'] or 'not set'}")

    lines.append("")
    return "\n".join(lines)


# ── Main orchestrator ────────────────────────────────────────────

def autoconnect(
    vault: Path,
    write_global: bool = False,
    create_remote: bool = False,
    extra_keys: dict[str, str] | None = None,
) -> dict:
    """
    Full autoconnect: MCP + git in one call.
    Returns a summary dict.
    """
    summary = {
        "mcp_configured": [],
        "mcp_builtin": [s["name"] for s in BUILTIN_SERVERS],
        "mcp_needs_key": [],
        "settings_path": None,
        "global_path": None,
        "codex_path": None,
        "git": {},
    }

    # 1. Build MCP servers
    if extra_keys:
        servers = build_mcp_servers_with_keys(vault, extra_keys)
    else:
        servers = build_mcp_servers(vault)

    summary["mcp_configured"] = list(servers.keys())

    # Check which key-servers are missing
    for srv in KEY_SERVERS:
        if srv["id"] not in servers:
            summary["mcp_needs_key"].append({
                "id": srv["id"],
                "name": srv["name"],
                "env_key": srv["env_key"],
            })

    # 2. Write project-level settings
    summary["settings_path"] = str(write_project_settings(vault, servers))

    # 3. Optionally write global settings
    if write_global:
        gp = write_global_settings(vault)
        summary["global_path"] = str(gp) if gp else None

    # 4. Write Codex config if available
    cp = write_codex_settings(vault)
    summary["codex_path"] = str(cp) if cp else None

    # 5. Git setup
    summary["git"] = setup_git(vault, create_remote=create_remote)

    # 6. Log
    append_implementation_log(vault, "autoconnect", [
        f"mcp_servers={','.join(summary['mcp_configured'])}",
        f"project_settings={summary['settings_path']}",
        f"git_upstream={'linked' if summary['git'].get('pos_upstream') else 'no'}",
        f"vault_remote={summary['git'].get('vault_remote', 'none')}",
    ])

    return summary


# ── CLI ──────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Auto-configure MCP servers and git for a POS vault.",
    )
    parser.add_argument("--vault", required=True, help="Path to your Obsidian vault")
    parser.add_argument("--global", dest="write_global", action="store_true",
                        help="Also write to global ~/.claude/settings.json")
    parser.add_argument("--create-repo", action="store_true",
                        help="Create a private GitHub repo for the vault")
    parser.add_argument("--status", action="store_true",
                        help="Show current configuration status")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()

    if args.status:
        print(format_status(vault))
        return 0

    summary = autoconnect(
        vault,
        write_global=args.write_global,
        create_remote=args.create_repo,
    )

    # Report
    print(f"\n  \033[1mAutoconnect complete.\033[0m\n")
    print(f"  MCP servers configured: {', '.join(summary['mcp_configured']) or 'none'}")
    if summary["mcp_needs_key"]:
        print(f"  Needs API key: {', '.join(s['name'] for s in summary['mcp_needs_key'])}")
        for s in summary["mcp_needs_key"]:
            print(f"    export {s['env_key']}=... then re-run")
    print(f"  Built-in (approve in app): {', '.join(summary['mcp_builtin'])}")
    print(f"  Settings: {summary['settings_path']}")
    if summary["git"].get("pos_upstream"):
        print(f"  POS upstream: linked")
    if summary["git"].get("vault_remote"):
        print(f"  Vault repo: {summary['git']['vault_remote']}")
    print()
    print(f"  \033[1mNext step:\033[0m Open vault in Claude Code / Codex.")
    print(f"  The app will ask you to approve each MCP connection.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
