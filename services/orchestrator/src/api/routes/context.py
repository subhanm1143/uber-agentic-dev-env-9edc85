from uuid import UUID

from fastapi import APIRouter

from ...context.retriever import retrieve
from ...db.repositories import project_repo
from ..errors import NotFound

router = APIRouter(prefix="/projects/{project_id}/context", tags=["context"])


@router.get("")
def debug_context(project_id: str, q: str, top_k: int = 5) -> dict:
    """Debug endpoint: inspect exactly what context an agent would see."""
    project = project_repo.get(UUID(project_id))
    if project is None:
        raise NotFound("project not found")
    return {"query": q, "chunks": retrieve(project.repo_path, q, top_k)}
