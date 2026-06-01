import streamlit as st
from session_state import get_health, get_collections


def render_sidebar(client):
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:1rem;">
            <div style="font-size:2.5rem;">📚</div>
            <div style="font-size:1.1rem; font-weight:700; color:#e0e0e0;">RAG 知识库</div>
            <div style="font-size:0.75rem; color:#888;">智能文档问答系统</div>
        </div>
        """, unsafe_allow_html=True)

        # Cached health indicator (TTL 30s)
        ok = get_health(client, ttl=30)
        if ok:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:6px;padding:6px 10px;'
                'background:#1a3a2a;border-radius:8px;font-size:0.82rem;">'
                '<span style="width:8px;height:8px;border-radius:50%;background:#4caf50;display:inline-block;"></span>'
                ' 后端服务正常'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:6px;padding:6px 10px;'
                'background:#3a1a1a;border-radius:8px;font-size:0.82rem;">'
                '<span style="width:8px;height:8px;border-radius:50%;background:#f44336;display:inline-block;"></span>'
                ' 后端未连接'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.caption("⚙️ 检索设置")
        top_k = st.slider("Top-K", 1, 20, st.session_state.get("top_k", 8),
                          help="每次检索返回的文本块数量")
        st.session_state.top_k = top_k

        st.markdown("---")

        # Cached collection stats (TTL 30s)
        collections = get_collections(client, ttl=30)
        if collections:
            st.caption("📊 知识库统计")
            for c in collections:
                st.metric(c['name'], f"{c['count']} chunks")

        st.markdown("---")
        st.caption(f"API: {client.base_url}")
