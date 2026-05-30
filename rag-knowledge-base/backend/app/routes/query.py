from fastapi import APIRouter, Depends, HTTPException

from app.models.query import QueryRequest, QueryResponse, RetrieveResponse
from app.services.retriever import RetrieverService
from app.services.generator import GeneratorService
from app.dependencies import get_retriever, get_generator

router = APIRouter(tags=["query"])


@router.post("/query", response_model=QueryResponse)
async def ask_question(
    req: QueryRequest,
    retriever: RetrieverService = Depends(get_retriever),
    generator: GeneratorService = Depends(get_generator),
):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    results = retriever.retrieve(
        query=req.question,
        top_k=req.top_k,
        source_filter=req.collection,
    )

    response = generator.generate(req.question, results)

    return QueryResponse(
        question=req.question,
        answer=response["answer"],
        sources=response["sources"],
        model=generator.model,
    )


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
