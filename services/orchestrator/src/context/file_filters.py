"""Decide which files are worth indexing."""
from __future__ import annotations

from pathlib import Path

_SKIP_DIRS = {".git", "node_modules", "__pycache__", "dist", "build", ".venv"}
_CODE_SUFFIXES = {".py", ".ts", ".tsx", ".js", ".sql", ".md", ".json", ".yaml", ".yml"}
_MAX_BYTES = 200_000  # skip generated/huge files


def should_index(path: Path) -> bool:
    if any(part in _SKIP_DIRS for part in path.parts):
        return False
    if path.suffix not in _CODE_SUFFIXES:
        return False
    try:
        return path.stat().st_size <= _MAX_BYTES
    except OSError:
        return False
