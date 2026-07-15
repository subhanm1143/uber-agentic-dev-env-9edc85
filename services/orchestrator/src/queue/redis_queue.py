"""A minimal at-least-once queue and run-lock over Redis."""
from __future__ import annotations

from ..cache.redis_client import _client

_QUEUE_KEY = "runs:queue"
_LOCK_TTL = 600  # a run lock auto-expires so a crashed worker can't wedge a run


def enqueue(run_id: str) -> None:
    _client.rpush(_QUEUE_KEY, run_id)


def dequeue(timeout: int = 5) -> str | None:
    """Block up to `timeout` seconds for the next run id."""
    item = _client.blpop(_QUEUE_KEY, timeout=timeout)
    return item[1] if item else None


def acquire_lock(run_id: str) -> bool:
    """Set the lock only if absent (NX); returns False if already held."""
    return bool(_client.set(f"run:lock:{run_id}", "1", nx=True, ex=_LOCK_TTL))


def release_lock(run_id: str) -> None:
    _client.delete(f"run:lock:{run_id}")


def heartbeat(run_id: str) -> None:
    """Refresh the lock TTL to signal the run is still alive."""
    _client.expire(f"run:lock:{run_id}", _LOCK_TTL)
