import streamlit as st


def render_message(role: str, content: str, sources: list[dict] | None = None):
    with st.chat_message(role):
        st.markdown(content)
        if sources and role == "assistant":
            with st.expander("📎 引用来源"):
                seen = set()
                for src in sources:
                    source_name = src.get("source", "unknown")
                    chunk_idx = src.get("chunk_index", "-")
                    key = f"{source_name}:{chunk_idx}"
                    if key not in seen:
                        seen.add(key)
                        st.markdown(
                            f'<span class="source-tag">📄 {source_name}</span>',
                            unsafe_allow_html=True,
                        )
