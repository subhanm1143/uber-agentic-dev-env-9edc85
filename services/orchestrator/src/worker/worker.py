"""Pull run ids off the queue and execute them, one lock per run."""
from __future__ import annotations

from uuid import UUID

from ..agents.run_controller import execute_run
from ..db.repositories import run_repo
from ..llm.providers.openai import OpenAIProvider
from ..models import RunStatus
from ..queue.redis_queue import acquire_lock, dequeue, heartbeat, release_lock
from ..sandbox.docker_runner import DockerRunner


def _run_tests_for(repo_path: str):
    runner = DockerRunner()

    def run_tests(command: str):
        result = runner.run(command, workdir=repo_path)
        return result.stdout + result.stderr, result.exit_code

    return run_tests


def process_one(run_id_str: str) -> None:
    # The lock makes processing idempotent: a duplicate delivery is dropped.
    if not acquire_lock(run_id_str):
        return
    try:
        run = run_repo.get(UUID(run_id_str))
        if run is None or run.status in (RunStatus.SUCCEEDED, RunStatus.FAILED):
            return  # already terminal — safe to skip on a redelivery
        heartbeat(run_id_str)
        # In a real system task/project lookups would supply these:
        execute_run(
            run_id=run.id,
            task="<loaded from task_repo>",
            repo_path="<loaded from project_repo>",
            llm=OpenAIProvider(),
            run_tests=_run_tests_for("<repo_path>"),
        )
    finally:
        release_lock(run_id_str)


def main() -> None:
    print("worker started; waiting for runs...")
    while True:
        run_id = dequeue()
        if run_id is not None:
            process_one(run_id)


if __name__ == "__main__":
    main()
