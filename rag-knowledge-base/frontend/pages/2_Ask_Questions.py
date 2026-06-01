import streamlit as st
from session_state import init_session
from components.sidebar import render_sidebar
from components.chat import render_message
from components.styles import inject_global_styles

init_session()
render_sidebar(st.session_state.client)
inject_global_styles()

st.markdown("""
<div style="text-align:center; padding:1.5rem 0 1rem;">
    <div style="font-size:2.5rem;">💬</div>
    <h2 style="margin:0.3rem 0; color:#c2185b;">智能问答</h2>
    <p style="color:#8b5e66;">基于已上传文档检索并生成回答，每次回答均标注引用来源</p>
</div>
""", unsafe_allow_html=True)

# Chat messages
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"], msg.get("sources"))

# Prompt input
if prompt := st.chat_input("输入你的问题，基于知识库文档回答..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    render_message("user", prompt)

    with st.spinner("检索中..."):
        try:
            result = st.session_state.client.query(
                question=prompt,
                top_k=st.session_state.get("top_k", 5),
            )
            answer = result.get("answer", "")
            sources = result.get("sources", [])

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
            })
            render_message("assistant", answer, sources)
        except Exception as e:
            error_msg = f"请求失败: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            render_message("assistant", error_msg)

# Footer controls
if st.session_state.messages:
    c1, c2 = st.columns([1, 10])
    with c1:
        if st.button("🗑️ 清空", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
