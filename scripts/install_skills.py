#!/usr/bin/env python3
"""Clone and install agent skill/resource libraries into the client vault."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, ensure_parent

RESOURCES_PATH = REPO_ROOT / "config" / "agent_resources.json"


def load_resources() -> dict[str, object]:
    return json.loads(RESOURCES_PATH.read_text(encoding="utf-8"))


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


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"  - {item}" for item in items)


def write_skills_readme(vault: Path, results: dict[str, str], resources: dict[str, object]) -> None:
    """Write a summary note into the vault about installed skills."""
    repo_sections = []
    for repo in resources["clone_repositories"]:
        target = repo["target"]
        highlights = repo.get("highlight_paths", [])
        repo_sections.append(
            f"""### {repo["name"]}

- Location: `30-Resources/{target}/`
- Source: {repo["url"].removesuffix(".git")}
- Status: `{results.get(repo["id"], "unknown")}`
- Contains: {repo["description"]}
- Use when:
{bullet_list(repo["use_when"])}
{f"- Highlight paths: {', '.join(f'`{path}`' for path in highlights)}" if highlights else ""}
"""
        )

    recommended_sections = []
    for skill in resources["recommended_skills"]:
        recommended_sections.append(
            f"""### {skill["name"]}

- Installed source: `30-Resources/{skill["source_repo"]}/{skill["path"]}`
- Web: {skill["url"]}
- Use when:
{bullet_list(skill["use_when"])}
"""
        )

    reference_sections = []
    for resource in resources["reference_resources"]:
        env_vars = resource.get("env_vars", [])
        reference_sections.append(
            f"""### {resource["name"]}

- Link: {resource["url"]}
- Purpose: {resource["description"]}
- Use when:
{bullet_list(resource["use_when"])}
{f"- Env vars: {', '.join(f'`{name}`' for name in env_vars)}" if env_vars else ""}
"""
        )

    content = f"""# Agent Skills And Prompt Systems

## What Are These?

Skills and prompt systems are composable instruction packages. Instead of one huge prompt, the agent loads the right workflow when the task requires it.

## Installed Repositories

{chr(10).join(repo_sections)}

## Recommended Starting Skills

{chr(10).join(recommended_sections)}

## Search And Research

{chr(10).join(reference_sections)}

## How To Use

1. Browse `30-Resources/` to see what is installed.
2. For Claude Code plugin skills, install them in the actual Claude Code plugin/skills location when you are ready.
3. For project work, tell the agent which skill/workflow to use.
4. Example: "Use Product Data Audit before changing this product workflow."
5. Example: "Use GitHub Issues Management to turn this chat into durable tasks."

## Safety

- Do not paste secrets into these skill folders.
- Do not clone private client data into `30-Resources/`.
- Treat these as reference libraries until the client chooses which skills to activate.
- Keep source-specific credentials in environment variables or approved app settings, never in Obsidian.

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

    resource_config = load_resources()
    results: dict[str, str] = {}
    for repo in resource_config["clone_repositories"]:
        dest = resources / repo["target"]
        status = clone_or_pull(repo["url"], dest)
        results[repo["id"]] = status
        print(f"  {repo['target']}: {status}")

    write_skills_readme(vault, results, resource_config)

    append_implementation_log(
        vault,
        "install_skills",
        [f"{k}={v}" for k, v in results.items()]
        + [
            "guide=30-Resources/Skills & Superpowers Guide.md",
            "references=Exa, Claude Code Docs, MCP Docs",
            "recommended_skills=CEO Council, Product Data Audit, GitHub Issues Management",
        ],
    )

    print(f"Skills installed into: {resources}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
