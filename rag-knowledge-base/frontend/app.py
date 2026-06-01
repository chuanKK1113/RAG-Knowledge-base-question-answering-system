from concurrent.futures import ThreadPoolExecutor, as_completed

import streamlit as st
from session_state import init_session, get_health
from components.sidebar import render_sidebar
from components.styles import inject_global_styles

st.set_page_config(page_title="RAG 知识库", page_icon="📚", layout="wide")

init_session()
render_sidebar(st.session_state.client)

# === Global CSS ===
inject_global_styles()

# === Hero ===
st.markdown("""
<div class="hero">
    <h1>📚 RAG 知识库问答系统</h1>
    <p>上传文档 · 智能检索 · AI 驱动回答 — 基于文档内容精准答疑，每一条回答均可溯源</p>
</div>
""", unsafe_allow_html=True)

# === Stats row ===
health_ok = get_health(st.session_state.client, ttl=60)

# Fetch docs and chunk count in parallel
client = st.session_state.client
docs: list = []
total_chunks = 0
with ThreadPoolExecutor(max_workers=2) as pool:
    fut_docs = pool.submit(client.list_documents)
    fut_cols = pool.submit(client.list_collections)
    results = {"docs": [], "chunks": 0}
    for fut in as_completed([fut_docs, fut_cols]):
        if fut is fut_docs:
            try:
                results["docs"] = fut.result()
            except Exception:
                pass
        else:
            try:
                cols_info = fut.result()
                results["chunks"] = sum(c["count"] for c in cols_info)
            except Exception:
                pass
    docs = results["docs"]
    total_chunks = results["chunks"]

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
    <div class="stat-box">
        <div class="num">{'🟢' if health_ok else '🔴'}</div>
        <div class="label">后端状态</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="num">{len(docs)}</div>
        <div class="label">已上传文档</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="stat-box">
        <div class="num">{total_chunks}</div>
        <div class="label">向量块总数</div>
    </div>
    """, unsafe_allow_html=True)

# === Feature cards ===
st.markdown("### 🚀 快速入口")
cols = st.columns(3)
card_data = [
    ("📤", "上传文档", "将 PDF / TXT 文件拖入系统\n自动解析、分块、向量化存储",
     "pages/1_Upload_Documents.py"),
    ("💬", "智能问答", "基于文档内容自由提问\nAI 精准回答并标注引用来源",
     "pages/2_Ask_Questions.py"),
    ("📋", "知识库管理", "浏览已上传文档列表\n支持按需删除与整理",
     "pages/3_Manage_Collections.py"),
]
for col, (icon, title, desc, page) in zip(cols, card_data):
    with col:
        st.markdown(f"""
        <a href="{page}" class="card">
            <div class="icon">{icon}</div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
        </a>
        """, unsafe_allow_html=True)
