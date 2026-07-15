"""Drive a run with full instrumentation: events, metrics, and logs."""
from __future__ import annotations

import time
from datetime import datetime
from uuid import UUID

from ..codeedit.patch_apply import apply_edits
from ..context.retriever import retrieve
from ..db.repositories import run_repo
from ..llm.providers.base import LLMProvider
from ..models import RunStatus
from ..observability.events import RunEvent, record_event
from ..observability.logger import log
from ..observability.metrics import incr, observe_duration
from .executor import RunTests
from .graph import build_graph
from .state import MAX_ITERATIONS, AgentState


def execute_run(
    run_id: UUID,
    task: str,
    repo_path: str,
    llm: LLMProvider,
    run_tests: RunTests,
) -> AgentState:
    started = time.monotonic()
    incr("runs_started")
    log(str(run_id), "run_started", task=task)
    record_event(RunEvent(run_id=run_id, node_name="run", status="started",
                          started_at=datetime.utcnow()))

    run_repo.set_status(run_id, RunStatus.RUNNING)
    chunks = retrieve(repo_path, task)
    context = "\n\n".join(f"# {c['path']}\n{c['text']}" for c in chunks)

    graph = build_graph(llm, run_tests)
    final = graph.invoke({
        "task": task, "context": context,
        "iterations": 0, "max_iterations": MAX_ITERATIONS,
    })

    if final.get("edits"):
        apply_edits(repo_path, str(run_id), final["edits"])

    succeeded = bool(final.get("succeeded"))
    status = RunStatus.SUCCEEDED if succeeded else RunStatus.FAILED
    run_repo.set_status(run_id, status)

    observe_duration("run_seconds", time.monotonic() - started)
    incr("runs_succeeded" if succeeded else "runs_failed")
    log(str(run_id), "run_finished", status=status.value,
        iterations=final.get("iterations", 0))
    record_event(RunEvent(run_id=run_id, node_name="run", status=status.value.lower(),
                          started_at=datetime.utcnow(), ended_at=datetime.utcnow()))
    return final
