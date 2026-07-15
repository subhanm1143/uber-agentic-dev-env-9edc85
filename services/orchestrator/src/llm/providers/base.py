"""The provider-agnostic contract every LLM client implements."""
from __future__ import annotations

import abc
from dataclasses import dataclass


@dataclass(slots=True)
class LLMResponse:
    text: str
    input_tokens: int
    output_tokens: int
    raw: dict  # the untouched provider payload, kept for debugging


class LLMProvider(abc.ABC):
    @abc.abstractmethod
    def complete(self, system: str, user: str, *, max_tokens: int = 1024) -> LLMResponse:
        """Return a normalized completion. Implementations add retries/timeouts."""
        raise NotImplementedError
