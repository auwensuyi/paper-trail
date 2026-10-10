import pytest

from app.services.chunking import chunk_text


def test_empty_text_gives_no_chunks():
    assert chunk_text("   ") == []


def test_short_text_is_one_chunk():
    assert chunk_text("hello world", size=100, overlap=10) == ["hello world"]


def test_chunks_respect_size_and_overlap():
    text = "abcdefghij" * 10  # 100 chars
    chunks = chunk_text(text, size=30, overlap=10)
    assert all(len(c) <= 30 for c in chunks)
    # Each chunk starts with the last 10 chars of the previous one
    assert chunks[1][:10] == chunks[0][-10:]
    # Nothing is lost at the end
    assert text.endswith(chunks[-1])


def test_bad_overlap_raises():
    with pytest.raises(ValueError):
        chunk_text("text", size=10, overlap=10)
