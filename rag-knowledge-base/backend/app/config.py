import logging
import sys

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

PLACEHOLDER_API_KEYS = {
    "sk-...",
    "sk-your-key-here",
    "your-api-key",
    "",
}


class Settings(BaseSettings):
    model_config = {"env_file": [".env", "../.env"], "env_file_encoding": "utf-8"}

    # Embedding (local sentence-transformers model)
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dimensions: int = 384

    # LLM
    llm_api_base: str = "https://api.deepseek.com/v1"
    llm_api_key: str = ""
    llm_model: str = "deepseek-v4-flash"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 1024

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "knowledge_base"

    # Chunking
    chunk_size: int = 800
    chunk_overlap: int = 150

    # Retrieval
    top_k: int = 8
    similarity_threshold: float = 0.55

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # File upload
    max_upload_size_mb: int = 50

    def validate_required(self) -> None:
        """Fail fast on startup if critical config is missing or placeholder."""
        errors: list[str] = []

        if self.llm_api_key in PLACEHOLDER_API_KEYS:
            errors.append(
                "LLM_API_KEY is not set or is a placeholder. "
                "Create a .env file in the backend/ directory with:\n"
                "  LLM_API_KEY=sk-your-real-key\n"
                f"  LLM_API_BASE={self.llm_api_base}"
            )

        if errors:
            for err in errors:
                logger.error("Configuration error: %s", err)
            sys.exit("❌ Server startup failed due to configuration errors.")


settings = Settings()
