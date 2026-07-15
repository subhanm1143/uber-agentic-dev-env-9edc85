from uuid import UUID

from fastapi import APIRouter

from ...observability.events import events_for
from ...observability.metrics import snapshot

router = APIRouter(tags=["observability"])


@router.get("/runs/{run_id}/events")
def run_events(run_id: str) -> dict:
    return {"events": events_for(UUID(run_id))}


@router.get("/metrics")
def metrics() -> dict:
    return snapshot()
