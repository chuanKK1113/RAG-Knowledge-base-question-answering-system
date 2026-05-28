from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    chunk_count: int
    char_count: int
