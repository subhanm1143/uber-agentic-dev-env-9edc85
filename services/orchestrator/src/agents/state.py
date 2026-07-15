"""The single canonical state object passed between graph nodes.

Kept JSON-serializable so it can be persisted after every node and replayed.
"""
from __future__ import annotations

from typing import TypedDict


class AgentState(TypedDict, total=False):
    task: str               # the developer's request
    context: str            # retrieved codebase context
    plan: list[str]         # ordered steps from the planner
    patch: str              # unified diff proposed by codegen
    last_stdout: str        # executor output of the last command
    last_exit_code: int     # 0 == success
    iterations: int         # how many refine cycles have run
    max_iterations: int     # hard stop
    succeeded: bool         # set by the executor when tests pass


MAX_ITERATIONS = 3
