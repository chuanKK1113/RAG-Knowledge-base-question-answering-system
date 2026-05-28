from functools import lru_cache

from app.config import settings
from app.services.parser import DocumentParser
from app.services.chunker import TextChunker


@lru_cache()
def get_parser() -> DocumentParser:
    return DocumentParser()


@lru_cache()
def get_chunker() -> TextChunker:
    return TextChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
