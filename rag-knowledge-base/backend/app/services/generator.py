from openai import OpenAI
import httpx

RAG_PROMPT_TEMPLATE = """你是一个知识库助手。仅基于以下上下文回答问题，遵循以下规则：

1. 如果上下文中包含答案，提供清晰简洁的回答，引用相关来源。
2. 如果上下文不足，请回答："基于已有文档，我无法回答此问题。"
3. 绝不编造上下文中不存在的信息。
4. 在回答末尾列出使用的来源（文件名）。

上下文：
{context}

问题：{question}

回答："""


class GeneratorService:
    def __init__(self, api_base: str, api_key: str, model: str,
                 temperature: float = 0.1, max_tokens: int = 1024):
        self.client = OpenAI(
            base_url=api_base,
            api_key=api_key,
            timeout=httpx.Timeout(180.0, connect=30.0, read=120.0),
            max_retries=1,
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def generate(self, question: str, context_chunks: list[dict]) -> dict:
        if not context_chunks:
            return {
                "answer": "基于已有文档，我无法回答此问题。",
                "sources": [],
            }

        context_text = self._format_context(context_chunks)
        prompt = RAG_PROMPT_TEMPLATE.format(context=context_text, question=question)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": [
                {"source": c["metadata"].get("source", "unknown"),
                 "chunk_index": c["metadata"].get("chunk_index", 0)}
                for c in context_chunks
            ],
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
            },
        }

    def _format_context(self, chunks: list[dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            source = chunk["metadata"].get("source", "unknown")
            parts.append(f"[{i}] 来源: {source}\n{chunk['text']}")
        return "\n\n".join(parts)
