#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from common import REPO_ROOT, append_implementation_log, safe_write, slug


PATTERNS_PATH = REPO_ROOT / "config" / "source_patterns.json"


def load_patterns() -> dict[str, object]:
    return json.loads(PATTERNS_PATH.read_text(encoding="utf-8"))


def iter_files(path: Path, extensions: set[str], max_files: int) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in extensions else []
    files: list[Path] = []
    for candidate in path.rglob("*"):
        if len(files) >= max_files:
            break
        if candidate.is_file() and candidate.suffix.lower() in extensions:
            files.append(candidate)
    return files


def classify(path: Path, patterns: list[dict[str, object]]) -> tuple[str, str] | None:
    haystack = f"{path.name} {path.parent}".lower()
    for pattern in patterns:
        for keyword in pattern["keywords"]:
            if str(keyword).lower() in haystack:
                return str(pattern["target"]), str(keyword)
    return None


def unique_target(target_dir: Path, source: Path) -> Path:
    base = slug(source.stem)
    suffix = source.suffix.lower()
    target = target_dir / f"{base}{suffix}"
    counter = 2
    while target.exists():
        target = target_dir / f"{base}-{counter}{suffix}"
        counter += 1
    return target


def build_report(imports: list[tuple[Path, Path, str]], matched: int) -> str:
    rows = []
    for source, target, reason in imports:
        rows.append(f"| `{source}` | `{target}` | keyword: `{reason}` |")
    if not rows:
        rows.append("| none | none | no matching files imported |")
    return f"""# Source Discovery Report

This report was generated from explicitly approved scan paths only.

No original files were deleted, renamed, or modified.

## Imported files

| Source | Target | Reason |
|---|---|---|
{chr(10).join(rows)}

## Candidate count

- Matched candidates: {matched}
- Imported copies: {len(imports)}
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely copy approved local source files into the Sisi starter vault.")
    parser.add_argument("--vault", required=True)
    parser.add_argument("--scan-path", action="append", default=[])
    parser.add_argument("--max-files", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    config = load_patterns()
    extensions = {str(ext).lower() for ext in config["extensions"]}
    patterns = list(config["patterns"])

    imports: list[tuple[Path, Path, str]] = []
    matched = 0
    for scan_path in args.scan_path:
        root = Path(scan_path).expanduser().resolve()
        for source in iter_files(root, extensions, args.max_files):
            classification = classify(source, patterns)
            if not classification:
                continue
            matched += 1
            target_rel, reason = classification
            target_dir = vault / target_rel
            target_dir.mkdir(parents=True, exist_ok=True)
            target = unique_target(target_dir, source)
            imports.append((source, target, reason))
            if not args.dry_run:
                shutil.copy2(source, target)

    report = vault / "90-Operations" / "Setup" / "Source Discovery Report.md"
    safe_write(report, build_report(imports, matched), force=True)
    append_implementation_log(
        vault,
        "source_discovery",
        [
            f"scan_paths={', '.join(args.scan_path) if args.scan_path else 'none'}",
            f"matched={matched}",
            f"copied={0 if args.dry_run else len(imports)}",
            f"dry_run={args.dry_run}",
            "original_files_modified=false",
        ],
    )
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
