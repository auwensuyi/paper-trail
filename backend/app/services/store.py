"""A deliberately simple, in-memory document store with keyword search.

This gets the app working end to end on day one. It is NOT how you'd do it
in production: everything is lost on restart, and keyword matching misses
answers phrased with different words.

Milestone 2 replaces this with embeddings + Postgres/pgvector (see README).
"""

import re
import uuid
from collections import Counter

from .chunking import Chunk, chunk_text

_WORD = re.compile(r"[a-z0-9]+")
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "how",
    "in", "is", "it", "of", "on", "or", "that", "the", "this", "to", "was",
    "what", "when", "where", "which", "who", "why", "with", "does", "do",
}


def _tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall(text.lower()) if w not in _STOPWORDS]


class DocumentStore:
    def __init__(self) -> None:
        self.documents: dict[str, dict] = {}
        self.chunks: list[Chunk] = []

    def add(self, filename: str, text: str, size: int, overlap: int) -> dict:
        doc_id = uuid.uuid4().hex[:12]
        pieces = chunk_text(text, size=size, overlap=overlap)
        for i, piece in enumerate(pieces):
            self.chunks.append(Chunk(doc_id, filename, i, piece))
        doc = {"id": doc_id, "filename": filename, "chunks": len(pieces)}
        self.documents[doc_id] = doc
        return doc

    def all(self) -> list[dict]:
        return list(self.documents.values())

    def search(self, query: str, k: int = 4) -> list[Chunk]:
        """Rank chunks by how many query words they contain."""
        q = set(_tokens(query))
        if not q:
            return []
        scored = []
        for chunk in self.chunks:
            counts = Counter(_tokens(chunk.text))
            score = sum(counts[w] for w in q)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [chunk for _, chunk in scored[:k]]


store = DocumentStore()
