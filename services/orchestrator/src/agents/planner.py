"""Planner agent: turn a task + context into an ordered list of steps."""
from __future__ import annotations

from ..llm.providers.base import LLMProvider
from .state import AgentState

_SYSTEM = (
    "You are a senior engineer. Given a task and repository context, produce a "
    "short ordered plan (3-6 steps) to implement it. Return one step per line."
)


def make_planner(llm: LLMProvider):
    def planner(state: AgentState) -> AgentState:
        user = f"TASK:\n{state['task']}\n\nCONTEXT:\n{state.get('context', '')}"
        resp = llm.complete(_SYSTEM, user, max_tokens=512)
        steps = [line.strip("-* ").strip() for line in resp.text.splitlines() if line.strip()]
        return {**state, "plan": steps}

    return planner
