#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, safe_write


CONNECTORS_PATH = REPO_ROOT / "config" / "connectors.json"


def load_connectors() -> list[dict[str, object]]:
    return json.loads(CONNECTORS_PATH.read_text(encoding="utf-8"))["connectors"]


def command_status() -> str:
    commands = ["claude", "codex", "node", "npx", "python3"]
    return "\n".join(f"- {cmd}: {shutil.which(cmd) or 'missing'}" for cmd in commands)


def build_report() -> str:
    rows = []
    for connector in load_connectors():
        env_vars = connector.get("env_vars", [])
        missing = [env_var for env_var in env_vars if not os.environ.get(env_var)]
        readiness = "ready-no-secret-needed" if not env_vars else ("env-ready" if not missing else "missing-env")
        rows.append(
            "| {name} | {role} | {readiness} | {missing} | {target} |".format(
                name=connector["name"],
                role=connector["role"],
                readiness=readiness,
                missing=", ".join(missing) if missing else "none",
                target=connector["target"],
            )
        )
    return f"""# MCP Readiness Report

This report checks local readiness only. It does not connect accounts or write external MCP config.

## Local commands

{command_status()}

## Connector readiness

| Connector | Role | Readiness | Missing env vars | Vault target |
|---|---|---|---|---|
{chr(10).join(rows)}

## Safe connection policy

1. Connect one source at a time.
2. Use manual export or read-only scope first.
3. Store secrets outside the vault and outside git.
4. First test reads one approved object and writes a source note into Obsidian.
5. Never auto-send email, mutate Notion, mutate Crisp, or bulk-import without review.

## Operator instruction

Use `90-Operations/Setup/Connect Sources Prompt.md` as the operator prompt. If MCP tools are available, prefer them for read-only source import. If not, use manual export into `70-Sources/`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MCP readiness and safe setup report.")
    parser.add_argument("--vault", required=True)
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    output = vault / "90-Operations" / "Setup" / "MCP Readiness Report.md"
    safe_write(output, build_report(), force=True)
    append_implementation_log(vault, "mcp_readiness", [f"output={output.relative_to(vault)}", "external_config_mutated=false"])
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
