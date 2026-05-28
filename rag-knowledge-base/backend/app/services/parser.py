import fitz
from pathlib import Path


class DocumentParser:
    SUPPORTED_TYPES = {".pdf", ".txt", ".md", ".csv"}

    def parse(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix == ".pdf":
            return self._parse_pdf(file_path)
        elif suffix in (".txt", ".md", ".csv"):
            return self._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def _parse_pdf(self, file_path: Path) -> str:
        doc = fitz.open(str(file_path))
        text_parts = []
        for page in doc:
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(page_text)
        doc.close()
        if not text_parts:
            raise ValueError(
                "This PDF appears to be scanned/image-based. "
                "OCR support is not yet available."
            )
        return "\n".join(text_parts)

    def _parse_text(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")
