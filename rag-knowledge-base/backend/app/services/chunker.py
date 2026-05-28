import re
from dataclasses import dataclass, field


@dataclass
class Chunk:
    text: str
    metadata: dict
    chunk_id: str


class TextChunker:
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 150):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, text: str, source_name: str) -> list[Chunk]:
        paragraphs = re.split(r"\n\s*\n", text)
        chunks: list[Chunk] = []
        current_chunk = ""
        chunk_idx = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) <= self.chunk_size:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                if current_chunk:
                    chunks.append(self._make_chunk(current_chunk, source_name, chunk_idx))
                    chunk_idx += 1

                if len(para) > self.chunk_size:
                    for sub in self._split_long_paragraph(para):
                        chunks.append(self._make_chunk(sub, source_name, chunk_idx))
                        chunk_idx += 1
                    current_chunk = ""
                else:
                    current_chunk = para

        if current_chunk:
            chunks.append(self._make_chunk(current_chunk, source_name, chunk_idx))

        return self._apply_overlap(chunks)

    def _make_chunk(self, text: str, source: str, idx: int) -> Chunk:
        return Chunk(
            text=text.strip(),
            metadata={"source": source, "chunk_index": idx},
            chunk_id=f"{source}:{idx}",
        )

    def _split_long_paragraph(self, paragraph: str) -> list[str]:
        sentences = re.split(r"(?<=[.!?])\s+", paragraph)
        result = []
        current = ""

        for sent in sentences:
            if len(current) + len(sent) <= self.chunk_size:
                current += (" " if current else "") + sent
            else:
                if current:
                    result.append(current)
                if len(sent) > self.chunk_size:
                    result.extend(self._hard_split(sent))
                    current = ""
                else:
                    current = sent

        if current:
            result.append(current)
        return result

    def _hard_split(self, text: str) -> list[str]:
        result = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            result.append(text[i:i + self.chunk_size])
        return result

    def _apply_overlap(self, chunks: list[Chunk]) -> list[Chunk]:
        if self.chunk_overlap <= 0 or len(chunks) <= 1:
            return chunks

        for i in range(1, len(chunks)):
            prev_text = chunks[i - 1].text
            if len(prev_text) > self.chunk_overlap:
                overlap_text = prev_text[-self.chunk_overlap:]
                chunks[i].text = overlap_text + "\n\n" + chunks[i].text

        return chunks
