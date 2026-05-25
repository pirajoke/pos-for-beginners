#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import platform
import shutil
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, load_structure, safe_write
from setup_vault import content_for


CONNECTORS_PATH = REPO_ROOT / "config" / "connectors.json"


def load_connectors() -> list[dict[str, object]]:
    return json.loads(CONNECTORS_PATH.read_text(encoding="utf-8"))["connectors"]


def connector_registry(vault: Path) -> str:
    rows = []
    for connector in load_connectors():
        env_vars = ", ".join(connector.get("env_vars", [])) if connector.get("env_vars") else "none"
        rows.append(
            "| {name} | {role} | {status} | {target} | {approval} | {secrets} | {env} |".format(
                name=connector["name"],
                role=connector["role"],
                status=connector["default_status"],
                target=connector["target"],
                approval="yes" if connector["approval_required"] else "no",
                secrets="yes" if connector["secret_required"] else "no",
                env=env_vars,
            )
        )
    return f"""# Connector Registry

This note tracks which systems can be connected, where their context should land, and what the client must approve.

## Registry

| System | Role | Current status | Vault target | Approval required | Secret required | Env vars |
|---|---|---|---|---|---|---|
{chr(10).join(rows)}

## Rule

Connectors may retrieve approved context and save source notes into Obsidian. They must not auto-send messages, mutate external systems, scrape broad workspaces, or store secrets in the vault.

## Install target

```text
{vault}
```
"""


def mcp_plan() -> str:
    sections = []
    for connector in load_connectors():
        env_vars = connector.get("env_vars", [])
        sections.append(
            f"""## {connector["name"]}

- Purpose: {connector["role"]}.
- First safe action: {connector["first_action"]}
- Required approval: {'yes' if connector["approval_required"] else 'no'}.
- Required secrets/env vars: {', '.join(env_vars) if env_vars else 'none'}.
- Context target: `{connector["target"]}`.
- Status: `{connector["default_status"]}`.
"""
        )
    return "# MCP Connection Plan\n\n" + "\n".join(sections) + """
## Safety Gates

1. Ask which source to connect first.
2. Confirm scope in plain language.
3. Prefer manual export before API/MCP.
4. Use read-only credentials first.
5. Import one approved object and write one source note.
6. Stop for review before bulk import.
"""


def install_report(vault: Path, created: list[str], skipped: list[str], allow_non_obsidian: bool) -> str:
    return f"""# Install Report

## Result

POS FOR BEGINNERS vault installed or verified.

## Vault

```text
{vault}
```

## Machine

- OS: {platform.platform()}
- Python: {platform.python_version()}
- Repo: `{REPO_ROOT}`
- Obsidian marker required: {'no' if allow_non_obsidian else 'yes'}

## Created or verified

{len(created)} paths

## Skipped existing files

{len(skipped)} files

Skipped files were preserved. The installer does not overwrite notes by default.

## Next action

Open `START HERE - POS FOR BEGINNERS Setup.md`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="One-command installer for the POS FOR BEGINNERS vault.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--allow-non-obsidian", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    if not args.allow_non_obsidian and not (vault / ".obsidian").exists():
        print(f"Refusing to install into non-Obsidian folder without --allow-non-obsidian: {vault}")
        return 2

    structure = load_structure()
    created: list[str] = []
    skipped: list[str] = []

    for directory in structure["directories"]:
        (vault / directory).mkdir(parents=True, exist_ok=True)
        created.append(directory + "/")

    for relative in structure["files"]:
        path = vault / relative
        content = content_for(relative)
        if relative == "90-Operations/Setup/Connector Registry.md":
            content = connector_registry(vault)
        elif relative == "90-Operations/Setup/MCP Connection Plan.md":
            content = mcp_plan()
        if safe_write(path, content, force=args.force):
            created.append(relative)
        else:
            skipped.append(relative)

    report_path = vault / "90-Operations" / "Setup" / "Install Report.md"
    safe_write(report_path, install_report(vault, created, skipped, args.allow_non_obsidian), force=True)
    append_implementation_log(
        vault,
        "install",
        [
            f"vault={vault}",
            f"repo={REPO_ROOT}",
            f"created_or_verified={len(created)}",
            f"skipped_existing={len(skipped)}",
            f"python3={shutil.which('python3') or 'missing'}",
            "external_connectors=not_connected_without_approval",
        ],
    )
    print(f"Installed POS FOR BEGINNERS into: {vault}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
