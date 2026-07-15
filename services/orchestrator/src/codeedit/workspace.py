"""Filesystem helpers: hashing, backups, and atomic writes."""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_if_exists(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def backup(path: Path, backup_dir: Path) -> str:
    """Copy the current file into the run's artifacts dir; return the backup path."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / path.name
    dest.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
    return str(dest)


def atomic_write(path: Path, content: str) -> None:
    """Write to a temp file in the same dir, then rename — never a half-written file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
        os.replace(tmp, path)   # atomic on POSIX
    except Exception:
        os.unlink(tmp)
        raise
