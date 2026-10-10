"""App settings, loaded from environment variables or a .env file.

Keeping config in one place means secrets (like your API key) never get
hard-coded. On AWS you'll later load these from Secrets Manager or SSM.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-5-5"

    # Chunking: how documents are split before retrieval
    chunk_size: int = 800  # characters per chunk
    chunk_overlap: int = 100  # characters shared between neighbouring chunks

    # How many chunks to send to the LLM as context
    top_k: int = 4

    upload_dir: str = "data/uploads"
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
