#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import read_text, safe_write


def build_pack(vault: Path, question: str) -> str:
    files = [
        "60-Rules/Obsidian Rules.md",
        "60-Rules/Agent Working Agreement.md",
        "60-Rules/Post-Task Protocol.md",
        "70-Sources/Context Source Map.md",
        "90-Operations/Setup/Setup Answers.md",
        "90-Operations/Setup/Connector Registry.md",
        "90-Operations/Setup/MCP Connection Plan.md",
        "90-Operations/Setup/MCP Readiness Report.md",
    ]
    sections = []
    for relative in files:
        sections.append(f"## {relative}\n\n{read_text(vault / relative, max_chars=5000)}")
    return f"""# Sisi Vault Context Pack

## Current Question

{question}

## How to use this pack

Use this to answer where information lives, what source to connect next, and what is still unknown. If a fact is not present, write `[ASK ME]`.

{chr(10).join(sections)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a context pack from the Sisi starter vault.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--question", default="Where is the client context located and what source should be connected first?")
    parser.add_argument("--output")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else vault / "90-Operations" / "Setup" / "Bootstrap Context Pack.md"
    safe_write(output, build_pack(vault, args.question), force=True)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
