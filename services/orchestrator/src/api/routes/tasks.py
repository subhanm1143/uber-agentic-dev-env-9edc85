from uuid import UUID

from fastapi import APIRouter

from ...db.repositories import project_repo, task_repo
from ...models import Task
from ..errors import NotFound
from ..schemas import CreateTaskRequest, TaskResponse

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(project_id: str, body: CreateTaskRequest) -> TaskResponse:
    pid = UUID(project_id)
    if project_repo.get(pid) is None:
        raise NotFound("project not found")
    task = task_repo.create(Task(project_id=pid, description=body.description))
    return TaskResponse(id=task.id, project_id=task.project_id, description=task.description)
