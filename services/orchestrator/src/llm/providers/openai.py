from __future__ import annotations

import os
import time

from openai import OpenAI, RateLimitError

from ..errors import RateLimited
from ..prompting import guard_size
from .base import LLMProvider, LLMResponse

_TIMEOUT_S = 30.0
_MAX_RETRIES = 3


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self._model = model
        self._client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=_TIMEOUT_S)

    def complete(self, system: str, user: str, *, max_tokens: int = 1024) -> LLMResponse:
        guard_size(system, user)
        for attempt in range(_MAX_RETRIES):
            try:
                resp = self._client.chat.completions.create(
                    model=self._model,
                    max_tokens=max_tokens,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                )
                usage = resp.usage
                return LLMResponse(
                    text=resp.choices[0].message.content or "",
                    input_tokens=usage.prompt_tokens if usage else 0,
                    output_tokens=usage.completion_tokens if usage else 0,
                    raw=resp.model_dump(),
                )
            except RateLimitError as exc:
                if attempt == _MAX_RETRIES - 1:
                    raise RateLimited(str(exc)) from exc
                time.sleep(2 ** attempt)  # exponential backoff
        raise RateLimited("exhausted retries")
