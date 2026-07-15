"""A single, lazily-initialized psycopg connection pool for the service."""
from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Iterator

from psycopg_pool import ConnectionPool
from psycopg import Connection

_DSN = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/agentic"
)

# One pool per process; opened on first use.
_pool = ConnectionPool(_DSN, min_size=1, max_size=10, open=False)


def pool() -> ConnectionPool:
    if _pool.closed:
        _pool.open()
    return _pool


@contextmanager
def connection() -> Iterator[Connection]:
    """Borrow a connection; commit on success, roll back on error."""
    with pool().connection() as conn:
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
