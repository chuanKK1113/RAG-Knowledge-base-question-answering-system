from fastapi import APIRouter, Depends, HTTPException

from app.models.collection import CollectionInfo
from app.services.vector_store import VectorStoreService
from app.dependencies import get_vector_store

router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("", response_model=list[CollectionInfo])
async def list_collections(
    vector_store: VectorStoreService = Depends(get_vector_store),
):
    return [
        CollectionInfo(
            name=vector_store.collection.name,
            count=vector_store.get_collection_count(),
        )
    ]


@router.delete("/{name}")
async def delete_collection(
    name: str,
    vector_store: VectorStoreService = Depends(get_vector_store),
):
    if name != vector_store.collection.name:
        raise HTTPException(status_code=404, detail=f"Collection '{name}' not found")
    vector_store.client.delete_collection(name)
    return {"deleted": True}
