import httpx


class APIClient:
    """HTTP client with connection pooling for fast repeated requests."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            timeout=httpx.Timeout(10.0, connect=2.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def health_check(self) -> dict:
        try:
            r = self._client.get(self._url("/health"), timeout=3)
            return r.json()
        except Exception:
            return {"status": "error"}

    def upload_document(self, file_bytes: bytes, filename: str) -> dict:
        files = {"file": (filename, file_bytes)}
        r = self._client.post(self._url("/documents/upload"), files=files, timeout=120)
        r.raise_for_status()
        return r.json()

    def query(self, question: str, top_k: int = 5) -> dict:
        r = self._client.post(
            self._url("/query"),
            json={"question": question, "top_k": top_k},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def list_documents(self) -> list[dict]:
        r = self._client.get(self._url("/documents"), timeout=10)
        r.raise_for_status()
        return r.json()

    def delete_document(self, doc_id: str) -> dict:
        r = self._client.delete(self._url(f"/documents/{doc_id}"), timeout=10)
        r.raise_for_status()
        return r.json()

    def list_collections(self) -> list[dict]:
        r = self._client.get(self._url("/collections"), timeout=10)
        r.raise_for_status()
        return r.json()
