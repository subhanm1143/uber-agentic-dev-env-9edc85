"""Wire planner → codegen → executor with a bounded refine loop."""
from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from ..llm.providers.base import LLMProvider
from .codegen import make_codegen
from .executor import RunTests, make_executor
from .planner import make_planner
from .state import AgentState


def _route_after_exec(state: AgentState) -> str:
    if state.get("succeeded"):
        return "done"
    if state.get("iterations", 0) >= state.get("max_iterations", 0):
        return "give_up"
    return "retry"


def build_graph(llm: LLMProvider, run_tests: RunTests):
    graph = StateGraph(AgentState)
    graph.add_node("planner", make_planner(llm))
    graph.add_node("codegen", make_codegen(llm))
    graph.add_node("executor", make_executor(run_tests))

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "codegen")
    graph.add_edge("codegen", "executor")
    graph.add_conditional_edges(
        "executor",
        _route_after_exec,
        {"done": END, "give_up": END, "retry": "codegen"},
    )
    return graph.compile()
