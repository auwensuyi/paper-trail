from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..config import settings
from ..services import llm
from ..services.store import store

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Source(BaseModel):
    number: int
    filename: str
    part: int
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    chunks = store.search(req.question, k=settings.top_k)
    if not chunks:
        return ChatResponse(
            answer="I couldn't find anything related in your documents. Try uploading one first.",
            sources=[],
        )
    try:
        text = llm.answer(req.question, chunks)
    except RuntimeError as e:
        raise HTTPException(500, str(e))

    sources = [
        Source(number=n, filename=c.filename, part=c.index + 1, text=c.text)
        for n, c in enumerate(chunks, start=1)
    ]
    return ChatResponse(answer=text, sources=sources)
