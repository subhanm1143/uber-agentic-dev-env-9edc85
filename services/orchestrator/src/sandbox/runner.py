"""The narrow execution contract agents depend on, plus an allowlist guard."""
from __future__ import annotations

import abc

from .models import ExecResult

# Only these command prefixes may run in the MVP sandbox.
ALLOWLIST = ("pytest", "python -m pytest", "npm test", "npm run", "ls", "cat")


class CommandNotAllowed(Exception):
    pass


def check_allowed(command: str) -> None:
    if not any(command.strip().startswith(prefix) for prefix in ALLOWLIST):
        raise CommandNotAllowed(command)


class Runner(abc.ABC):
    @abc.abstractmethod
    def run(self, command: str, workdir: str, timeout: int = 120) -> ExecResult:
        """Execute a command and return its captured result."""
        raise NotImplementedError
