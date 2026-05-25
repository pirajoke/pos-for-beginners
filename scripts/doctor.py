#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, read_text, safe_write


CONNECTORS_PATH = REPO_ROOT / "config" / "connectors.json"


def connector_rows() -> list[str]:
    connectors = json.loads(CONNECTORS_PATH.read_text(encoding="utf-8"))["connectors"]
    rows = []
    for connector in connectors:
        env_vars = connector.get("env_vars", [])
        env_status = [f"{name}={'set' if os.environ.get(name) else 'missing'}" for name in env_vars]
        rows.append(
            "| {name} | {role} | {target} | {status} | {env_status} |".format(
                name=connector["name"],
                role=connector["role"],
                target=connector["target"],
                status=connector["default_status"],
                env_status=", ".join(env_status) if env_status else "none",
            )
        )
    return rows


def build_report(vault: Path) -> str:
    tools = ["python3", "git", "node", "npx", "claude", "codex"]
    tool_lines = "\n".join(f"- {tool}: {shutil.which(tool) or 'missing'}" for tool in tools)
    source_map = read_text(vault / "70-Sources" / "Context Source Map.md", max_chars=4000)
    return f"""# System Doctor Report

## Vault

```text
{vault}
```

## Local tools

{tool_lines}

## Connector status

| Connector | Role | Vault target | Default status | Env status |
|---|---|---|---|---|
{chr(10).join(connector_rows())}

## Context source map

{source_map}

## Result

This report checks local readiness and environment variables only. It does not connect accounts, scrape mail, read Notion, send messages, or mutate external systems.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a local readiness report for a Sisi starter vault.")
    parser.add_argument("--vault", required=True)
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    output = vault / "90-Operations" / "Setup" / "System Doctor Report.md"
    safe_write(output, build_report(vault), force=True)
    append_implementation_log(vault, "doctor", [f"output={output.relative_to(vault)}", "external_mutation=false"])
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
