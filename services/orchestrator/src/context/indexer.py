"""Walk a repo and split eligible files into line-bounded chunks."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .file_filters import should_index

_CHUNK_LINES = 40  # small enough to fit many chunks in a prompt window


@dataclass(slots=True)
class Chunk:
    path: str
    start_line: int
    text: str


def index_repo(repo_path: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    root = Path(repo_path)
    for file in sorted(root.rglob("*")):
        if not file.is_file() or not should_index(file):
            continue
        lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
        rel = str(file.relative_to(root))
        for start in range(0, len(lines), _CHUNK_LINES):
            window = lines[start : start + _CHUNK_LINES]
            chunks.append(Chunk(path=rel, start_line=start + 1, text="\n".join(window)))
    return chunks
