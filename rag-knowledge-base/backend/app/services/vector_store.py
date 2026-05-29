import chromadb
from chromadb.config import Settings as ChromaSettings


class VectorStoreService:
    def __init__(self, persist_dir: str, collection_name: str):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(
        self,
        chunk_ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> int:
        self.collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
        )
        return len(chunk_ids)

    def delete_by_source(self, source_name: str) -> int:
        results = self.collection.get(where={"source": source_name})
        ids = results.get("ids", [])
        if ids:
            self.collection.delete(ids=ids)
        return len(ids)

    def delete_by_id(self, doc_id: str) -> int:
        results = self.collection.get(where={"doc_id": doc_id})
        ids = results.get("ids", [])
        if ids:
            self.collection.delete(ids=ids)
        return len(ids)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        where_filter: dict | None = None,
    ) -> list[dict]:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )
        if not results["ids"] or not results["ids"][0]:
            return []

        return [
            {
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
            for i in range(len(results["ids"][0]))
        ]

    def get_all_documents(self) -> list[dict]:
        """List all documents with their metadata."""
        results = self.collection.get(include=["metadatas"])
        seen = {}
        for i, doc_id in enumerate(results.get("ids", [])):
            meta = results["metadatas"][i] if results.get("metadatas") else {}
            source = meta.get("source", "unknown")
            doc_id_val = meta.get("doc_id", doc_id)
            if doc_id_val not in seen:
                seen[doc_id_val] = {
                    "id": doc_id_val,
                    "filename": source,
                    "chunk_count": 1,
                }
            else:
                seen[doc_id_val]["chunk_count"] += 1
        return list(seen.values())

    def get_collection_count(self) -> int:
        return self.collection.count()
