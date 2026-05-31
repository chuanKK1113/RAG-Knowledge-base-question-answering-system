import pytest
from pathlib import Path
from app.services.parser import DocumentParser


class TestDocumentParser:
    def test_parse_txt_file(self, tmp_path):
        file_path = tmp_path / "test.txt"
        file_path.write_text("Hello world!", encoding="utf-8")
        parser = DocumentParser()
        result = parser.parse(file_path)
        assert result == "Hello world!"

    def test_parse_unsupported_type(self, tmp_path):
        file_path = tmp_path / "test.jpg"
        file_path.write_text("not an image")
        parser = DocumentParser()
        with pytest.raises(ValueError, match="Unsupported file type"):
            parser.parse(file_path)

    def test_supported_types(self):
        parser = DocumentParser()
        assert ".pdf" in parser.SUPPORTED_TYPES
        assert ".txt" in parser.SUPPORTED_TYPES
        assert ".md" in parser.SUPPORTED_TYPES

    def test_parse_empty_txt(self, tmp_path):
        file_path = tmp_path / "empty.txt"
        file_path.write_text("", encoding="utf-8")
        parser = DocumentParser()
        result = parser.parse(file_path)
        assert result == ""
