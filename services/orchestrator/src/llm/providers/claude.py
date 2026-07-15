from __future__ import annotations

import os
import time

from anthropic import Anthropic, RateLimitError

from ..errors import RateLimited
from ..prompting import guard_size
from .base import LLMProvider, LLMResponse

_TIMEOUT_S = 30.0
_MAX_RETRIES = 3


class ClaudeProvider(LLMProvider):
    def __init__(self, model: str = "claude-haiku-4-5") -> None:
        self._model = model
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], timeout=_TIMEOUT_S)

    def complete(self, system: str, user: str, *, max_tokens: int = 1024) -> LLMResponse:
        guard_size(system, user)
        for attempt in range(_MAX_RETRIES):
            try:
                resp = self._client.messages.create(
                    model=self._model,
                    max_tokens=max_tokens,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                text = "".join(block.text for block in resp.content if block.type == "text")
                return LLMResponse(
                    text=text,
                    input_tokens=resp.usage.input_tokens,
                    output_tokens=resp.usage.output_tokens,
                    raw=resp.model_dump(),
                )
            except RateLimitError as exc:
                if attempt == _MAX_RETRIES - 1:
                    raise RateLimited(str(exc)) from exc
                time.sleep(2 ** attempt)
        raise RateLimited("exhausted retries")
