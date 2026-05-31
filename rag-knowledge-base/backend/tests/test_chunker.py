import pytest
from app.services.chunker import TextChunker


class TestTextChunker:
    def setup_method(self):
        self.chunker = TextChunker(chunk_size=800, chunk_overlap=150)

    def test_chunk_single_short_paragraph(self):
        text = "Hello world, this is a short text."
        chunks = self.chunker.chunk(text, "test.txt")
        assert len(chunks) == 1
        assert chunks[0].text == text
        assert chunks[0].metadata["source"] == "test.txt"

    def test_chunk_empty_string(self):
        chunks = self.chunker.chunk("", "empty.txt")
        assert len(chunks) == 0

    def test_chunk_whitespace_only(self):
        chunks = self.chunker.chunk("   \n\n   ", "whitespace.txt")
        assert len(chunks) == 0

    def test_chunk_metadata_has_source(self):
        chunks = self.chunker.chunk("Some content here.", "demo.pdf")
        assert len(chunks) == 1
        assert chunks[0].metadata["source"] == "demo.pdf"
        assert "chunk_index" in chunks[0].metadata

    def test_chunk_paragraphs_below_size_stay_together(self):
        text = "\n\n".join(["Para one", "Para two", "Para three"])
        chunks = self.chunker.chunk(text, "test.txt")
        assert len(chunks) == 1

    def test_chunk_forces_split_on_long_content(self):
        text = "x" * 2000
        chunks = self.chunker.chunk(text, "long.txt")
        assert len(chunks) > 1
        for c in chunks:
            assert len(c.text) <= 800 + self.chunker.chunk_overlap + 100

    def test_chunk_overlap_applied(self):
        chunker = TextChunker(chunk_size=400, chunk_overlap=100)
        text = "x" * 1000
        chunks = chunker.chunk(text, "test.txt")
        assert len(chunks) >= 2

    def test_chunk_ids_are_unique(self):
        text = "x" * 2000
        chunks = self.chunker.chunk(text, "unique.txt")
        ids = [c.chunk_id for c in chunks]
        assert len(ids) == len(set(ids))

    def test_chunk_preserves_sentence_boundaries(self):
        text = "First sentence. Second sentence. Third sentence."
        chunks = self.chunker.chunk(text, "test.txt")
        assert len(chunks) == 1
        assert "First sentence" in chunks[0].text
