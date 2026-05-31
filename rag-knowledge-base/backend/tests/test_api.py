import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestDocumentUpload:
    def test_upload_txt_file(self, client, tmp_path):
        file_path = tmp_path / "doc.txt"
        file_path.write_text("This is a test document about Python programming.", encoding="utf-8")
        with open(file_path, "rb") as f:
            response = client.post(
                "/documents/upload",
                files={"file": ("doc.txt", f, "text/plain")},
            )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["filename"] == "doc.txt"
        assert data["chunk_count"] >= 1

    def test_upload_unsupported_type(self, client, tmp_path):
        file_path = tmp_path / "doc.jpg"
        file_path.write_text("fake image")
        with open(file_path, "rb") as f:
            response = client.post(
                "/documents/upload",
                files={"file": ("doc.jpg", f, "image/jpeg")},
            )
        assert response.status_code == 415

    def test_upload_empty_file(self, client, tmp_path):
        file_path = tmp_path / "empty.txt"
        file_path.write_text("", encoding="utf-8")
        with open(file_path, "rb") as f:
            response = client.post(
                "/documents/upload",
                files={"file": ("empty.txt", f, "text/plain")},
            )
        assert response.status_code in [400, 500]

    def test_list_documents(self, client):
        response = client.get("/documents")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestQueryEndpoints:
    def test_query_retrieve_empty_question(self, client):
        response = client.post("/query/retrieve", json={"question": ""})
        assert response.status_code == 400

    def test_query_empty_question(self, client):
        response = client.post("/query", json={"question": ""})
        assert response.status_code == 400

    def test_query_retrieve_returns_results(self, client, tmp_path):
        # Upload a document first
        file_path = tmp_path / "doc.txt"
        file_path.write_text("Machine learning is a subset of artificial intelligence.", encoding="utf-8")
        with open(file_path, "rb") as f:
            client.post("/documents/upload", files={"file": ("doc.txt", f, "text/plain")})

        response = client.post("/query/retrieve", json={"question": "machine learning"})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert isinstance(data["results"], list)


class TestCollections:
    def test_list_collections(self, client):
        response = client.get("/collections")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
