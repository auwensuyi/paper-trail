"""Split long text into overlapping chunks.

Why chunk? LLMs have limited context, and retrieval works best on small,
focused pieces of text. Overlap keeps a sentence that straddles a boundary
from being cut in half and lost.
"""

from dataclasses import dataclass


@dataclass
class Chunk:
    doc_id: str
    filename: str
    index: int  # position of this chunk within its document
    text: str


def chunk_text(text: str, size: int = 800, overlap: int = 100) -> list[str]:
    """Return a list of text chunks, each at most `size` characters."""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= overlap < size:
        raise ValueError("overlap must be >= 0 and smaller than size")

    text = text.strip()
    if not text:
        return []

    chunks: list[str] = []
    step = size - overlap
    for start in range(0, len(text), step):
        piece = text[start : start + size].strip()
        if piece:
            chunks.append(piece)
        if start + size >= len(text):
            break
    return chunks

# TODO (Milestone 2): split on paragraph/sentence boundaries instead of raw
# characters, and compare answer quality before and after.
