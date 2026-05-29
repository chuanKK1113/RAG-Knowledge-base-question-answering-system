from fastapi import APIRouter, Depends, HTTPException

from app.models.query import QueryRequest, RetrieveResponse
from app.services.retriever import RetrieverService
from app.dependencies import get_retriever

router = APIRouter(tags=["query"])


@router.post("/query/retrieve", response_model=RetrieveResponse)
async def retrieve_only(
    req: QueryRequest,
    retriever: RetrieverService = Depends(get_retriever),
):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    results = retriever.retrieve(
        query=req.question,
        top_k=req.top_k,
        source_filter=req.collection,
    )

    return RetrieveResponse(question=req.question, results=results)
