"""Talk to the LLM: build a prompt from retrieved chunks and ask for a cited answer."""

from anthropic import Anthropic

from ..config import settings
from .chunking import Chunk

SYSTEM_PROMPT = """You answer questions using ONLY the numbered sources provided.
Cite sources inline like [1] or [2]. If the sources do not contain the answer,
say you could not find it in the documents. Do not make things up."""


def build_context(chunks: list[Chunk]) -> str:
    lines = []
    for n, c in enumerate(chunks, start=1):
        lines.append(f"[{n}] (from {c.filename}, part {c.index + 1})\n{c.text}")
    return "\n\n".join(lines)


def answer(question: str, chunks: list[Chunk]) -> str:
    if not settings.anthropic_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    client = Anthropic(api_key=settings.anthropic_api_key)
    message = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Sources:\n\n{build_context(chunks)}\n\nQuestion: {question}",
            }
        ],
    )
    return "".join(block.text for block in message.content if block.type == "text")

# TODO (Milestone 3): stream the answer token by token to the frontend.
# TODO (Milestone 5): switch to Amazon Bedrock so the app runs on AWS credentials.
