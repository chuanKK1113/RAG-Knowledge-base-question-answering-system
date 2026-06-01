import streamlit as st
from session_state import get_health, get_collections


def render_sidebar(client):
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; margin-bottom:1rem;">
            <div style="font-size:2.5rem;">📚</div>
            <div style="font-size:1.15rem; font-weight:800; color:#c2185b;">RAG 知识库</div>
            <div style="font-size:0.75rem; color:#8b5e66;">智能文档问答系统</div>
        </div>
        """, unsafe_allow_html=True)

        # Cached health indicator (TTL 30s)
        ok = get_health(client, ttl=30)
        if ok:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:6px;padding:6px 10px;'
                'background:#fce4ec;border-radius:8px;font-size:0.82rem;color:#6d3a48;">'
                '<span style="width:8px;height:8px;border-radius:50%;background:#e91e63;display:inline-block;"></span>'
                ' 后端服务正常'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="display:flex;align-items:center;gap:6px;padding:6px 10px;'
                'background:#fce4ec;border-radius:8px;font-size:0.82rem;color:#6d3a48;">'
                '<span style="width:8px;height:8px;border-radius:50%;background:#e53935;display:inline-block;"></span>'
                ' 后端未连接'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")

        st.markdown(
            '<div style="color:#c2185b; font-weight:700; font-size:0.82rem; '
            'margin-bottom:0.3rem; letter-spacing:0.03em;">⚙️ 检索设置</div>',
            unsafe_allow_html=True,
        )
        top_k = st.slider("Top-K", 1, 20, st.session_state.get("top_k", 8),
                          help="每次检索返回的文本块数量")
        st.session_state.top_k = top_k

        st.markdown("---")

        # Cached collection stats (TTL 30s)
        collections = get_collections(client, ttl=30)
        if collections:
            st.markdown(
                '<div style="color:#c2185b; font-weight:700; font-size:0.82rem; '
                'margin-bottom:0.3rem; letter-spacing:0.03em;">📊 知识库统计</div>',
                unsafe_allow_html=True,
            )
            for c in collections:
                st.metric(c['name'], f"{c['count']} chunks")

        st.markdown("---")
        st.markdown(
            f'<div style="font-size:0.7rem; color:#b08890; '
            f'text-align:center; word-break:break-all;">API: {client.base_url}</div>',
            unsafe_allow_html=True,
        )
