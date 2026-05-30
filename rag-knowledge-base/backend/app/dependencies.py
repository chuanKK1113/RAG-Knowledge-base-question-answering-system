from functools import lru_cache

from app.config import settings
from app.services.parser import DocumentParser
from app.services.chunker import TextChunker
from app.services.embedder import EmbeddingService
from app.services.vector_store import VectorStoreService
from app.services.retriever import RetrieverService
from app.services.generator import GeneratorService


@lru_cache()
def get_parser() -> DocumentParser:
    return DocumentParser()


@lru_cache()
def get_chunker() -> TextChunker:
    return TextChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


@lru_cache()
def get_embedder() -> EmbeddingService:
    return EmbeddingService(model_name=settings.embedding_model)


@lru_cache()
def get_vector_store() -> VectorStoreService:
    return VectorStoreService(
        persist_dir=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection_name,
    )


@lru_cache()
def get_retriever() -> RetrieverService:
    return RetrieverService(
        embedder=get_embedder(),
        vector_store=get_vector_store(),
        top_k=settings.top_k,
        threshold=settings.similarity_threshold,
    )


@lru_cache()
def get_generator() -> GeneratorService:
    return GeneratorService(
        api_base=settings.llm_api_base,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
