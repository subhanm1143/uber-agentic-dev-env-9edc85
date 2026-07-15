"""CodeGen agent: emit structured FileEdits (full-file replace) for the next step."""
from __future__ import annotations

import json

from ..codeedit.patch_models import FileEdit
from ..codeedit.workspace import sha256
from ..llm.providers.base import LLMProvider
from .state import AgentState

_SYSTEM = (
    "You are a coding agent. Given a plan and repository context, return a JSON "
    'array of edits: [{"path": str, "new_content": str}] implementing the next '
    "unfinished step. Return ONLY the JSON array."
)


def make_codegen(llm: LLMProvider):
    def codegen(state: AgentState) -> AgentState:
        plan_text = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(state.get("plan", [])))
        feedback = ""
        if state.get("last_exit_code", 0) != 0:
            feedback = f"\n\nPREVIOUS RUN FAILED:\n{state.get('last_stdout', '')}"
        user = f"PLAN:\n{plan_text}\n\nCONTEXT:\n{state.get('context', '')}{feedback}"
        resp = llm.complete(_SYSTEM, user, max_tokens=2048)

        raw_edits = json.loads(resp.text)
        edits = [
            FileEdit(
                path=e["path"],
                new_content=e["new_content"],
                expected_sha=sha256(e["new_content"]),
            )
            for e in raw_edits
        ]
        return {**state, "edits": edits}

    return codegen
