import streamlit as st


def render_message(role: str, content: str, sources: list[dict] | None = None):
    with st.chat_message(role):
        st.markdown(content)
        if sources and role == "assistant":
            with st.expander("📎 参考来源"):
                seen = set()
                for i, src in enumerate(sources):
                    source_name = src.get("source", "unknown")
                    chunk_idx = src.get("chunk_index", "-")
                    key = f"{source_name}:{chunk_idx}"
                    if key not in seen:
                        seen.add(key)
                        st.caption(f"📄 {source_name} (chunk {chunk_idx})")
