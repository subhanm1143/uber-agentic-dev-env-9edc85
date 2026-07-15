from fastapi import APIRouter
from pydantic import BaseModel

from ...sandbox.docker_runner import DockerRunner
from ...sandbox.runner import CommandNotAllowed
from ..errors import ApiError

router = APIRouter(prefix="/sandbox", tags=["sandbox"])
_runner = DockerRunner()


class ExecRequest(BaseModel):
    command: str
    workdir: str
    timeout: int = 120


@router.post("/exec")
def exec_command(body: ExecRequest) -> dict:
    try:
        result = _runner.run(body.command, body.workdir, body.timeout)
    except CommandNotAllowed as exc:
        raise ApiError(400, f"command not allowed: {exc}") from exc
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.exit_code,
        "timed_out": result.timed_out,
    }
