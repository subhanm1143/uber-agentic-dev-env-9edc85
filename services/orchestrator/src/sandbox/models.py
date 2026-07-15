"""The result of running a command in the sandbox."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ExecResult:
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False
