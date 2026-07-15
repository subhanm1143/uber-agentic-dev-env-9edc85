"""A structured edit format. Full-file replace is the simplest safe MVP edit."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FileEdit:
    path: str                    # repo-relative path
    new_content: str             # the full new file contents
    expected_sha: str | None = None  # sha of the content we based the edit on


@dataclass(slots=True)
class ApplyResult:
    applied: list[str]
    conflicts: list[str]
    backups: list[str]
