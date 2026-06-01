import streamlit as st
from session_state import init_session, get_health
from components.sidebar import render_sidebar

st.set_page_config(page_title="RAG 知识库", page_icon="📚", layout="wide")

init_session()
render_sidebar(st.session_state.client)

# === Global CSS ===
st.markdown("""
<style>
    /* Base */
    .stApp { background: #0e1117; }
    section[data-testid="stSidebar"] { background: #161b22; }

    /* Hero */
    .hero { text-align:center; padding:3rem 1rem 1.5rem; }
    .hero h1 { font-size:2.4rem; font-weight:800; margin-bottom:0.5rem; }
    .hero p { color:#8b949e; font-size:1.05rem; max-width:600px; margin:0 auto; }

    /* Feature cards */
    .card-row { display:flex; gap:1.2rem; justify-content:center; flex-wrap:wrap; margin:1.5rem 0 2rem; }
    .card { flex:1; min-width:220px; max-width:320px; padding:1.8rem 1.2rem; border-radius:14px;
            background:#161b22; border:1px solid #21262d; text-align:center; cursor:pointer;
            transition:border-color 0.2s, transform 0.15s; text-decoration:none; display:block; }
    .card:hover { border-color:#58a6ff; transform:translateY(-2px); }
    .card .icon { font-size:2.2rem; margin-bottom:0.8rem; }
    .card .title { font-size:1.1rem; font-weight:700; color:#e6edf3; margin-bottom:0.4rem; }
    .card .desc { font-size:0.82rem; color:#8b949e; }

    /* Stats */
    .stats-row { display:flex; gap:1rem; justify-content:center; margin:2rem 0; }
    .stat-box { padding:1rem 1.8rem; border-radius:12px; background:#161b22; border:1px solid #21262d;
                text-align:center; }
    .stat-box .num { font-size:1.6rem; font-weight:700; color:#58a6ff; }
    .stat-box .label { font-size:0.75rem; color:#8b949e; }

    /* Upload area */
    .upload-zone { border:2px dashed #30363d; border-radius:14px; padding:2.5rem; text-align:center;
                   background:#161b22; margin:1rem 0; }
    .upload-zone:hover { border-color:#58a6ff; }

    /* Doc card */
    .doc-card { display:flex; align-items:center; justify-content:space-between;
                padding:0.9rem 1.2rem; border-radius:10px; background:#161b22;
                border:1px solid #21262d; margin-bottom:0.6rem; }
    .doc-card:hover { border-color:#30363d; }

    /* Chat tweaks */
    [data-testid="stChatMessage"] { border-radius:12px; padding:0.8rem 1rem; }
    .source-tag { display:inline-block; padding:2px 10px; border-radius:20px;
                  background:#1a3a2a; color:#7ee787; font-size:0.75rem; margin:2px 4px; }
</style>
""", unsafe_allow_html=True)

# === Hero ===
st.markdown("""
<div class="hero">
    <h1>📚 RAG 知识库问答系统</h1>
    <p>上传文档 · 智能检索 · AI 驱动回答 — 基于文档内容精准答疑，每一条回答均可溯源</p>
</div>
""", unsafe_allow_html=True)

# === Stats row ===
health_ok = get_health(st.session_state.client, ttl=10)
try:
    docs = st.session_state.client.list_documents()
except Exception:
    docs = []
try:
    cols_info = st.session_state.client.list_collections()
    total_chunks = sum(c["count"] for c in cols_info)
except Exception:
    total_chunks = 0

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
