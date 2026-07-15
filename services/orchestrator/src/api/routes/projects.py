from fastapi import APIRouter

from ...db.repositories import project_repo
from ...models import Project
from ..errors import NotFound
from ..schemas import CreateProjectRequest, ProjectResponse

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(body: CreateProjectRequest) -> ProjectResponse:
    project = project_repo.create(Project(name=body.name, repo_path=body.repo_path))
    return ProjectResponse(
        id=project.id, name=project.name,
        repo_path=project.repo_path, created_at=project.created_at,
    )


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: str) -> ProjectResponse:
    from uuid import UUID
    project = project_repo.get(UUID(project_id))
    if project is None:
        raise NotFound("project not found")
    return ProjectResponse(
        id=project.id, name=project.name,
        repo_path=project.repo_path, created_at=project.created_at,
    )
