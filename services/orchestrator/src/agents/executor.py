"""Executor agent: run the project's tests and record the outcome.

The actual sandbox call is injected so this node stays testable; in the wired
graph it is the Docker runner built in a later step.
"""
from __future__ import annotations

from typing import Callable, Tuple

from .state import AgentState

# run_tests(command) -> (stdout, exit_code)
RunTests = Callable[[str], Tuple[str, int]]


def make_executor(run_tests: RunTests, test_command: str = "pytest -q"):
    def executor(state: AgentState) -> AgentState:
        stdout, exit_code = run_tests(test_command)
        return {
            **state,
            "last_stdout": stdout,
            "last_exit_code": exit_code,
            "succeeded": exit_code == 0,
            "iterations": state.get("iterations", 0) + 1,
        }

    return executor
