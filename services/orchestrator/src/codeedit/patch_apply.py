"""Apply FileEdits atomically, backing up first and detecting conflicts."""
from __future__ import annotations

from pathlib import Path

from .patch_models import ApplyResult, FileEdit
from .workspace import atomic_write, backup, read_if_exists, sha256


def apply_edits(
    repo_path: str, run_id: str, edits: list[FileEdit]
) -> ApplyResult:
    root = Path(repo_path)
    backup_dir = root / ".artifacts" / run_id / "backups"
    applied: list[str] = []
    conflicts: list[str] = []
    backups: list[str] = []

    for edit in edits:
        target = root / edit.path
        current = read_if_exists(target)

        # Conflict: the file changed since the edit was generated.
        if edit.expected_sha is not None and current is not None:
            if sha256(current) != edit.expected_sha:
                conflicts.append(edit.path)
                continue

        if current is not None:
            backups.append(backup(target, backup_dir))

        atomic_write(target, edit.new_content)
        applied.append(edit.path)

    return ApplyResult(applied=applied, conflicts=conflicts, backups=backups)
