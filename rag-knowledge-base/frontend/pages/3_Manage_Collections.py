import streamlit as st
from session_state import init_session
from components.sidebar import render_sidebar
from components.styles import inject_global_styles

init_session()
render_sidebar(st.session_state.client)
inject_global_styles()

st.markdown("""
<div style="text-align:center; padding:1.5rem 0 1rem;">
    <div style="font-size:2.5rem;">📋</div>
    <h2 style="margin:0.3rem 0; color:#c2185b;">知识库管理</h2>
    <p style="color:#8b5e66;">浏览、管理已上传的文档</p>
</div>
""", unsafe_allow_html=True)

try:
    docs = st.session_state.client.list_documents()
except Exception as e:
    st.error(f"获取文档列表失败: {e}")
    docs = []

if not docs:
    st.info("暂无已上传的文档，前往 **上传文档** 页面添加。", icon="ℹ️")
else:
    st.caption(f"共 {len(docs)} 个文档")
    for doc in docs:
        with st.container():
            c_left, c_mid, c_right = st.columns([4, 2, 1])
            with c_left:
                st.markdown(f"📄 **{doc['filename']}**")
                st.caption(f"ID: {doc['id']}")
            with c_mid:
                st.metric("Chunks", doc["chunk_count"])
            with c_right:
                if st.button("🗑️", key=f"del_{doc['id']}", help="删除此文档"):
                    try:
                        result = st.session_state.client.delete_document(doc["id"])
                        st.session_state.collections_cache = None
                        st.success(f"已移除 {result['chunks_removed']} chunks")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            st.markdown("---")
