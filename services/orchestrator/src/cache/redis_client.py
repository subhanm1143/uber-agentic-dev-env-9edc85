"""A tiny JSON cache over Redis used to memoize retrieval results."""
from __future__ import annotations

import json
import os
from typing import Any, Optional

import redis

_client = redis.Redis.from_url(
    os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    decode_responses=True,
)


def get_json(key: str) -> Optional[Any]:
    raw = _client.get(key)
    return json.loads(raw) if raw is not None else None


def set_json(key: str, value: Any, ttl_seconds: int = 300) -> None:
    _client.set(key, json.dumps(value), ex=ttl_seconds)
