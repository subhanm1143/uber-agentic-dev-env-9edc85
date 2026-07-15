"""LLM-layer errors. RateLimited is retryable; the rest are not."""
from __future__ import annotations


class LLMError(Exception):
    pass


class RateLimited(LLMError):
    """Provider asked us to back off — safe to retry."""


class PromptTooLarge(LLMError):
    """The prompt exceeds our guard; never sent to the provider."""
