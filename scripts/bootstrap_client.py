#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, safe_write


def run_step(args: list[str]) -> None:
    subprocess.run([sys.executable, *args], cwd=REPO_ROOT, check=True)


def bootstrap_summary(vault: Path, scan_paths: list[str]) -> str:
    return f"""# Bootstrap Summary

## Vault

```text
{vault}
```

## Completed automatically

- Installed / verified simple Obsidian vault structure.
- Wrote starter prompts for the Obsidian setup interview and agent working agreement interview.
- Wrote rules for note naming, source handling, post-task logging, and agent work.
- Generated connector registry and MCP connection plan.
- Generated system doctor report.
- Generated MCP readiness report.
- Ran safe source discovery on approved scan paths.
- Generated a bootstrap context pack.
- Installed Claude Skills and Superpowers into `30-Resources/`.
- Checked vault structure.

## Approved scan paths

{chr(10).join(f"- `{path}`" for path in scan_paths) if scan_paths else "- none provided"}

## Safety

- No files were deleted.
- No files were renamed.
- Existing notes were preserved unless `--force` was used.
- External accounts were not connected.
- Mail, Notion, Granola, Crisp, and external MCP configs were not mutated.

## Next

Open `START HERE - POS FOR BEGINNERS Setup.md`.
Then paste `90-Operations/Setup/Claude First Run.md` into Claude Code, Claude, Codex, or ChatGPT.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Full safe client bootstrap for POS FOR BEGINNERS.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--scan-path", action="append", default=[], help="Approved source folder/file to scan. Can be repeated.")
    parser.add_argument("--max-files", type=int, default=50)
    parser.add_argument("--allow-non-obsidian", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    install_args = ["scripts/install.py", "--vault", str(vault)]
    if args.allow_non_obsidian:
        install_args.append("--allow-non-obsidian")
    run_step(install_args)
    run_step(["scripts/doctor.py", "--vault", str(vault)])
    run_step(["scripts/mcp_readiness.py", "--vault", str(vault)])
    source_args = ["scripts/source_discovery.py", "--vault", str(vault), "--max-files", str(args.max_files)]
    for scan_path in args.scan_path:
        source_args.extend(["--scan-path", scan_path])
    run_step(source_args)
    run_step(["scripts/generate_context_pack.py", "--vault", str(vault)])
    run_step(["scripts/install_skills.py", "--vault", str(vault)])
    run_step(["scripts/check_vault.py", "--vault", str(vault)])

    output = vault / "90-Operations" / "Setup" / "Bootstrap Summary.md"
    safe_write(output, bootstrap_summary(vault, args.scan_path), force=True)
    append_implementation_log(vault, "bootstrap_client", [f"output={output.relative_to(vault)}", "status=complete"])
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
