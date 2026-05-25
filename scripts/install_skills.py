#!/usr/bin/env python3
"""Clone and install Claude Code skills and superpowers into the client vault."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, ensure_parent

SKILLS_DIR_NAME = "claude-skills"
SUPERPOWERS_DIR_NAME = "superpowers"

REPOS = {
    "skills": {
        "url": "https://github.com/anthropics/skills.git",
        "target": SKILLS_DIR_NAME,
        "description": "Official Claude Skills library by Anthropic",
    },
    "superpowers": {
        "url": "https://github.com/obra/superpowers.git",
        "target": SUPERPOWERS_DIR_NAME,
        "description": "Composable skills for coding agents by obra",
    },
}


def clone_or_pull(url: str, dest: Path) -> str:
    """Clone repo if missing, pull if already exists. Returns status string."""
    if dest.exists() and (dest / ".git").exists():
        subprocess.run(
            ["git", "-C", str(dest), "pull", "--ff-only"],
            check=False,
            capture_output=True,
        )
        return "updated"
    elif dest.exists():
        shutil.rmtree(dest)

    ensure_parent(dest)
    result = subprocess.run(
        ["git", "clone", "--depth", "1", url, str(dest)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Warning: failed to clone {url}: {result.stderr.strip()}", file=sys.stderr)
        return "failed"
    return "cloned"


def write_skills_readme(vault: Path, results: dict[str, str]) -> None:
    """Write a summary note into the vault about installed skills."""
    content = """# Installed Skills & Superpowers

## What Are These?

Skills and superpowers are composable instruction packages that teach AI agents
how to perform specific types of work. Instead of one huge prompt, the agent
loads the right skill when the task requires it.

## Installed Repositories

### Claude Skills (Anthropic Official)
- Location: `30-Resources/claude-skills/`
- Source: https://github.com/anthropics/skills
- Contains: document workflows, structured research, code workflows, repeatable tasks

### Superpowers (obra)
- Location: `30-Resources/superpowers/`
- Source: https://github.com/obra/superpowers
- Contains: reusable composable skills for coding agents

## How To Use

1. Browse the skills folders to see what's available.
2. When starting a task, tell your AI agent to load a relevant skill.
3. Example: "Load the code-review skill before reviewing this PR."

## Updating

Run from the pos-for-beginners repo:

```bash
python3 scripts/install_skills.py --vault "/path/to/ObsidianVault"
```

This will pull the latest versions.
"""
    path = vault / "30-Resources" / "Skills & Superpowers Guide.md"
    ensure_parent(path)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install Claude skills and superpowers into the vault.")
    parser.add_argument("--vault", required=True)
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    resources = vault / "30-Resources"
    resources.mkdir(parents=True, exist_ok=True)

    results: dict[str, str] = {}
    for key, repo in REPOS.items():
        dest = resources / repo["target"]
        status = clone_or_pull(repo["url"], dest)
        results[key] = status
        print(f"  {repo['target']}: {status}")

    write_skills_readme(vault, results)

    append_implementation_log(
        vault,
        "install_skills",
        [f"{k}={v}" for k, v in results.items()] + ["guide=30-Resources/Skills & Superpowers Guide.md"],
    )

    print(f"Skills installed into: {resources}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
