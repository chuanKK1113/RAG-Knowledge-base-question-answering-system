import streamlit as st

from components.sidebar import render_sidebar
from components.chat import render_message


def render():
    st.title("💬 智能问答")
    st.markdown("基于已上传的文档内容提问，系统将检索相关知识并使用 LLM 生成回答。")

    # Init chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        render_message(msg["role"], msg["content"], msg.get("sources"))

    # Chat input
    if prompt := st.chat_input("请输入你的问题..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        render_message("user", prompt)

        with st.spinner("正在检索并生成回答..."):
            try:
                result = st.session_state.client.query(
                    question=prompt,
                    top_k=st.session_state.get("top_k", 5),
                )
                answer = result.get("answer", "无法获取回答")
                sources = result.get("sources", [])

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })
                render_message("assistant", answer, sources)

            except Exception as e:
                error_msg = f"❌ 请求失败: {e}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                })
                render_message("assistant", error_msg)
                st.error(error_msg)

    # Clear history button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.session_state.messages and st.button("🗑️ 清空对话"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="智能问答", page_icon="💬")
    if "client" not in st.session_state:
        from api_client import APIClient
        st.session_state.client = APIClient("http://localhost:8000")
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    render_sidebar(st.session_state.client)
    render()
