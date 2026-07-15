"""Score chunks against a query using term frequency + path boosts.

A deliberate MVP: no embeddings, no vector store. Good enough to put the right
files in front of an agent, and trivial to reason about and cache.
"""
from __future__ import annotations

import re

from ..cache import redis_client
from .indexer import Chunk, index_repo


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z_][a-zA-Z0-9_]+", text.lower())


def _score(query_terms: list[str], chunk: Chunk) -> float:
    body = chunk.text.lower()
    path = chunk.path.lower()
    score = 0.0
    for term in query_terms:
        score += body.count(term)            # term frequency in the chunk
        if term in path:
            score += 5.0                     # a hit in the path is a strong signal
    return score


def retrieve(repo_path: str, query: str, top_k: int = 5) -> list[dict]:
    cache_key = f"ctx:{repo_path}:{query}:{top_k}"
    cached = redis_client.get_json(cache_key)
    if cached is not None:
        return cached

    terms = _tokenize(query)
    chunks = index_repo(repo_path)
    ranked = sorted(chunks, key=lambda c: _score(terms, c), reverse=True)
    result = [
        {"path": c.path, "start_line": c.start_line, "text": c.text}
        for c in ranked[:top_k]
        if _score(terms, c) > 0
    ]
    redis_client.set_json(cache_key, result, ttl_seconds=300)
    return result
