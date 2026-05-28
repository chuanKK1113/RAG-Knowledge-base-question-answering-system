from pydantic import BaseModel


class Source(BaseModel):
    source: str
    chunk_index: int


class QueryRequest(BaseModel):
    question: str
    collection: str | None = None
    top_k: int | None = None


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]
    model: str


class RetrieveResponse(BaseModel):
    question: str
    results: list[dict]
