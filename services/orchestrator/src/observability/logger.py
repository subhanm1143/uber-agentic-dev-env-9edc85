"""JSON structured logging — every line carries the run_id for correlation."""
from __future__ import annotations

import json
import sys
import time


def log(run_id: str, event: str, **fields) -> None:
    record = {"ts": time.time(), "run_id": run_id, "event": event, **fields}
    sys.stdout.write(json.dumps(record) + "\n")
    sys.stdout.flush()
