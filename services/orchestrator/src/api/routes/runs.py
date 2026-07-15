from uuid import UUID

from fastapi import APIRouter

from ...db.repositories import run_repo
from ...models import Run
from ...queue.redis_queue import enqueue
from ..errors import NotFound
from ..schemas import RunResponse

router = APIRouter(tags=["runs"])


@router.post("/tasks/{task_id}/runs", response_model=RunResponse, status_code=202)
def start_run(task_id: str) -> RunResponse:
    # Persist as QUEUED, push the id onto the queue, return immediately.
    run = run_repo.create(Run(task_id=UUID(task_id)))
    enqueue(str(run.id))
    return RunResponse(
        id=run.id, task_id=run.task_id,
        status=run.status.value, iterations=run.iterations,
    )


@router.get("/runs/{run_id}", response_model=RunResponse)
def get_run(run_id: str) -> RunResponse:
    run = run_repo.get(UUID(run_id))
    if run is None:
        raise NotFound("run not found")
    return RunResponse(
        id=run.id, task_id=run.task_id,
        status=run.status.value, iterations=run.iterations,
    )
