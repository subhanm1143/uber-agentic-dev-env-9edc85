"""Lightweight event sourcing: append one row per agent node to Postgres."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from ..db.connection import connection


@dataclass(slots=True)
class RunEvent:
    run_id: UUID
    node_name: str
    status: str                 # 'started' | 'succeeded' | 'failed'
    started_at: datetime
    ended_at: datetime | None = None
    error_summary: str | None = None
    token_usage: int = 0


def record_event(event: RunEvent) -> UUID:
    event_id = uuid4()
    with connection() as conn:
        conn.execute(
            """INSERT INTO run_events
                 (id, run_id, node_name, status, started_at, ended_at,
                  error_summary, token_usage)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (event_id, event.run_id, event.node_name, event.status,
             event.started_at, event.ended_at, event.error_summary, event.token_usage),
        )
    return event_id


def events_for(run_id: UUID, since_id: UUID | None = None) -> list[dict]:
    with connection() as conn:
        rows = conn.execute(
            """SELECT id, node_name, status, started_at, ended_at, error_summary
               FROM run_events WHERE run_id = %s ORDER BY started_at""",
            (run_id,),
        ).fetchall()
    return [
        {"id": str(r[0]), "node": r[1], "status": r[2],
         "started_at": r[3].isoformat(), "error": r[5]}
        for r in rows
    ]
