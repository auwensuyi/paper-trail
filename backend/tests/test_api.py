from fastapi.testclient import TestClient

from app.main import app
from app.services.store import store

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_upload_and_search(tmp_path, monkeypatch):
    monkeypatch.setattr("app.config.settings.upload_dir", str(tmp_path))
    files = {"file": ("notes.txt", b"Amazon S3 stores objects in buckets.", "text/plain")}
    res = client.post("/documents", files=files)
    assert res.status_code == 200
    assert res.json()["chunks"] == 1

    hits = store.search("where are S3 objects stored?")
    assert hits and "buckets" in hits[0].text


def test_rejects_unsupported_type():
    files = {"file": ("image.png", b"\x89PNG", "image/png")}
    assert client.post("/documents", files=files).status_code == 400


def test_chat_without_documents_match():
    res = client.post("/chat", json={"question": "zebra quantum"})
    assert res.status_code == 200
    assert res.json()["sources"] == []
