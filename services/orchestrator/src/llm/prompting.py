"""Prompt assembly + a hard size guard run before any network call."""
from __future__ import annotations

from .errors import PromptTooLarge

_MAX_CHARS = 48_000  # ~12k tokens; a cheap guard against runaway prompts


def guard_size(system: str, user: str) -> None:
    total = len(system) + len(user)
    if total > _MAX_CHARS:
        raise PromptTooLarge(f"prompt is {total} chars, limit is {_MAX_CHARS}")


def build_context_block(chunks: list[dict]) -> str:
    """Render retrieved chunks into a labeled block for the user prompt."""
    parts = []
    for c in chunks:
        parts.append(f"# {c['path']}:{c['start_line']}\n{c['text']}")
    return "\n\n".join(parts)
