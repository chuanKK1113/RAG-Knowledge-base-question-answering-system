class RetrieverService:
    def __init__(self, embedder, vector_store, top_k: int = 5, threshold: float = 0.7):
        self.embedder = embedder
        self.vector_store = vector_store
        self.top_k = top_k
        self.threshold = threshold

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        source_filter: str | None = None,
    ) -> list[dict]:
        k = top_k or self.top_k
        query_embedding = self.embedder.embed_query(query)
        where_filter = {"source": source_filter} if source_filter else None
        results = self.vector_store.search(query_embedding, k, where_filter)

        # Convert cosine distance (0=identical, 2=opposite) to similarity (1→0)
        filtered = []
        for r in results:
            similarity = 1.0 - r["distance"] / 2.0
            if similarity >= self.threshold:
                r["similarity"] = round(similarity, 4)
                filtered.append(r)

        return filtered
