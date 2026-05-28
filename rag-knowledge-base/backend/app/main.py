from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import documents


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="RAG Knowledge Base API",
    description="RAG-based document Q&A system",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(documents.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
