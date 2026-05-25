#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from common import load_structure, read_text


REQUIRED_CONNECTORS = ["Obsidian", "Notion", "Mail", "Granola", "Crisp"]
REQUIRED_RULE_TEXT = [
    "Do not create more than 6-10 top-level folders",
    "one question at a time",
    "Do not connect Notion, Mail, Granola, Crisp",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a POS FOR BEGINNERS Obsidian vault.")
    parser.add_argument("--vault", required=True)
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    structure = load_structure()
    errors: list[str] = []

    if len(structure["top_level_folders"]) > structure["max_top_level_folders"]:
        errors.append("too many top-level folders in config")

    for directory in structure["directories"]:
        if not (vault / directory).is_dir():
            errors.append(f"missing directory: {directory}")

    for relative in structure["files"]:
        if not (vault / relative).is_file():
            errors.append(f"missing file: {relative}")

    registry = vault / "90-Operations" / "Setup" / "Connector Registry.md"
    registry_text = read_text(registry)
    for connector in REQUIRED_CONNECTORS:
        if connector not in registry_text:
            errors.append(f"Connector Registry missing {connector}")

    interview = vault / "90-Operations" / "Setup" / "Obsidian Structure Interview.md"
    interview_text = read_text(interview)
    for required in REQUIRED_RULE_TEXT[:2]:
        if required not in interview_text:
            errors.append(f"Obsidian interview missing required phrase: {required}")

    first_run = vault / "90-Operations" / "Setup" / "Claude First Run.md"
    first_run_text = read_text(first_run)
    if REQUIRED_RULE_TEXT[2] not in first_run_text:
        errors.append("Claude First Run missing connector safety gate")

    if errors:
        print("Vault check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Vault check passed: {vault}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
