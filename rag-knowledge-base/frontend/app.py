import streamlit as st

from components.sidebar import render_sidebar
from api_client import APIClient

st.set_page_config(page_title="RAG 知识库", page_icon="📚", layout="wide")

if "client" not in st.session_state:
    st.session_state.client = APIClient("http://localhost:8000")
if "top_k" not in st.session_state:
    st.session_state.top_k = 5

render_sidebar(st.session_state.client)

st.title("📚 RAG 知识库问答系统")

st.markdown("""
欢迎使用 RAG 知识库问答系统！本系统可以：

1. **上传文档** — 在侧边栏或上传页面添加 PDF/TXT 文档
2. **智能问答** — 基于文档内容回答你的问题
3. **管理知识库** — 查看和删除已上传的文档

使用侧边栏导航到不同功能页面。
""")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_Upload_Documents.py", label="📤 上传文档", icon="📤")
with col2:
    st.page_link("pages/2_Ask_Questions.py", label="💬 智能问答", icon="💬")
with col3:
    st.page_link("pages/3_Manage_Collections.py", label="📋 管理知识库", icon="📋")
