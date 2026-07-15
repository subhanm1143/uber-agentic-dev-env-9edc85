"""Run a command inside a throwaway container with no network and a timeout."""
from __future__ import annotations

import subprocess

from .models import ExecResult
from .runner import Runner, check_allowed

_IMAGE = "python:3.12-slim"


class DockerRunner(Runner):
    def __init__(self, image: str = _IMAGE) -> None:
        self._image = image

    def run(self, command: str, workdir: str, timeout: int = 120) -> ExecResult:
        check_allowed(command)
        docker_cmd = [
            "docker", "run", "--rm",
            "--network", "none",          # no network access from agent code
            "--memory", "512m",           # basic resource cap
            "-v", f"{workdir}:/work",
            "-w", "/work",
            self._image,
            "sh", "-c", command,
        ]
        try:
            proc = subprocess.run(
                docker_cmd, capture_output=True, text=True, timeout=timeout
            )
            return ExecResult(
                stdout=proc.stdout, stderr=proc.stderr, exit_code=proc.returncode
            )
        except subprocess.TimeoutExpired as exc:
            return ExecResult(
                stdout=exc.stdout or "", stderr=exc.stderr or "",
                exit_code=124, timed_out=True,
            )
