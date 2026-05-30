import httpx


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> dict:
        try:
            r = httpx.get(self._url("/health"), timeout=5)
            return r.json()
        except Exception:
            return {"status": "error"}

    def upload_document(self, file_bytes: bytes, filename: str) -> dict:
        files = {"file": (filename, file_bytes)}
        r = httpx.post(self._url("/documents/upload"), files=files, timeout=120)
        r.raise_for_status()
        return r.json()

    def query(self, question: str, top_k: int = 5) -> dict:
        r = httpx.post(
            self._url("/query"),
            json={"question": question, "top_k": top_k},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def list_documents(self) -> list[dict]:
        r = httpx.get(self._url("/documents"), timeout=10)
        r.raise_for_status()
        return r.json()

    def delete_document(self, doc_id: str) -> dict:
        r = httpx.delete(self._url(f"/documents/{doc_id}"), timeout=10)
        r.raise_for_status()
        return r.json()

    def list_collections(self) -> list[dict]:
        r = httpx.get(self._url("/collections"), timeout=10)
        r.raise_for_status()
        return r.json()
