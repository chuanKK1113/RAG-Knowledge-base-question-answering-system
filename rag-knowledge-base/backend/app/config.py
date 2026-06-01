from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": [".env", "../.env"], "env_file_encoding": "utf-8"}

    # Embedding (local sentence-transformers model)
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"
    embedding_dimensions: int = 384

    # LLM
    llm_api_base: str = "https://api.openai.com/v1"
    llm_api_key: str = "sk-..."
    llm_model: str = "gpt-4o-mini"
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


settings = Settings()
