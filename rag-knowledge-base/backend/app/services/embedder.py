import os
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        cache_dir = Path(__file__).resolve().parents[3] / "data" / "models"
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.model = SentenceTransformer(model_name, cache_folder=str(cache_dir))

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        return self.embed([text])[0]
