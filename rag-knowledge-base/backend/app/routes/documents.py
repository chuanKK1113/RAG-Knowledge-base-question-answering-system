import uuid
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.config import settings
from app.dependencies import get_parser, get_chunker
from app.models.document import DocumentResponse
from app.services.parser import DocumentParser
from app.services.chunker import TextChunker

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    parser: DocumentParser = Depends(get_parser),
    chunker: TextChunker = Depends(get_chunker),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in DocumentParser.SUPPORTED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type: {suffix}. "
                   f"Supported: {', '.join(DocumentParser.SUPPORTED_TYPES)}",
        )

    content = await file.read()
    if len(content) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.max_upload_size_mb}MB",
        )

    upload_dir = Path(settings.chroma_persist_dir).parent / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    doc_id = str(uuid.uuid4())
    temp_path = upload_dir / f"{doc_id}_{file.filename}"
    temp_path.write_bytes(content)

    try:
        text = parser.parse(temp_path)
        if not text.strip():
            raise HTTPException(status_code=400, detail="File contains no extractable text")

        chunks = chunker.chunk(text, file.filename)

        return DocumentResponse(
            id=doc_id,
            filename=file.filename,
            chunk_count=len(chunks),
            char_count=len(text),
        )
    finally:
        if temp_path.exists():
            temp_path.unlink()
