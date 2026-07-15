"""In-process counters and a duration accumulator. Minimal by design."""
from __future__ import annotations

from collections import defaultdict
from threading import Lock

_counters: dict[str, int] = defaultdict(int)
_durations: dict[str, float] = defaultdict(float)
_lock = Lock()


def incr(name: str, by: int = 1) -> None:
    with _lock:
        _counters[name] += by


def observe_duration(name: str, seconds: float) -> None:
    with _lock:
        _durations[name] += seconds


def snapshot() -> dict:
    with _lock:
        return {"counters": dict(_counters), "durations": dict(_durations)}
