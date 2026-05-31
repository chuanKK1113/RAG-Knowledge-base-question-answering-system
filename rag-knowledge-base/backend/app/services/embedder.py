import hashlib
import os
from functools import lru_cache
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        cache_dir = Path(__file__).resolve().parents[3] / "data" / "models"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer(model_name, cache_folder=str(cache_dir))
        self._cache = {}

    def embed(self, texts: list[str]) -> list[list[float]]:
        results = []
        uncached_texts = []
        uncached_indices = []

        for i, text in enumerate(texts):
            key = hashlib.md5(text.encode()).hexdigest()
            if key in self._cache:
                results.append((i, self._cache[key]))
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)

        if uncached_texts:
            new_embeddings = self.model.encode(uncached_texts, show_progress_bar=False)
            for idx, text, emb in zip(uncached_indices, uncached_texts, new_embeddings):
                emb_list = emb.tolist()
                key = hashlib.md5(text.encode()).hexdigest()
                self._cache[key] = emb_list
                results.append((idx, emb_list))

        results.sort(key=lambda x: x[0])
        return [r[1] for r in results]

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]

    @property
    def cache_size(self) -> int:
        return len(self._cache)
