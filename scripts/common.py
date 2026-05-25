from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "config" / "vault_structure.json"


def load_structure() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def safe_write(path: Path, content: str, force: bool = False) -> bool:
    ensure_parent(path)
    if path.exists() and not force:
        return False
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return True


def read_text(path: Path, max_chars: int | None = None) -> str:
    if not path.exists():
        return f"UNKNOWN: missing file {path}"
    text = path.read_text(encoding="utf-8", errors="replace")
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars] + "\n\n[truncated]"
    return text


def append_implementation_log(vault: Path, title: str, lines: list[str]) -> None:
    log_path = vault / "90-Operations" / "Setup" / "Implementation Log.md"
    ensure_parent(log_path)
    if not log_path.exists():
        log_path.write_text("# Implementation Log\n\n", encoding="utf-8")
    entry = [f"## {now_stamp()} - {title}", ""]
    entry.extend(f"- {line}" for line in lines)
    entry.append("")
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(entry) + "\n")


def slug(value: str) -> str:
    clean = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in clean:
        clean = clean.replace("--", "-")
    return clean.strip("-") or "untitled"
