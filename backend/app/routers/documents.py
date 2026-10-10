from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile

from ..config import settings
from ..services.store import store

router = APIRouter(prefix="/documents", tags=["documents"])

ALLOWED = {".txt", ".md"}  # TODO (Milestone 2): add PDF support with pypdf


@router.post("")
async def upload(file: UploadFile) -> dict:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(400, f"Unsupported file type. Allowed: {sorted(ALLOWED)}")

    raw = await file.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(400, "File must be UTF-8 text")

    # Keep a copy on disk. On AWS this becomes an S3 upload (Milestone 5).
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    (upload_dir / Path(file.filename).name).write_bytes(raw)

    return store.add(file.filename, text, settings.chunk_size, settings.chunk_overlap)


@router.get("")
def list_documents() -> list[dict]:
    return store.all()
