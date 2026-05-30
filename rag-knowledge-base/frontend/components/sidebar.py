import streamlit as st


def render_sidebar(client):
    with st.sidebar:
        st.title("RAG 知识库")

        health = client.health_check()
        if health.get("status") == "ok":
            st.success("后端服务正常")
        else:
            st.error("后端服务未连接")

        st.divider()

        st.caption(f"API: {client.base_url}")

        st.divider()

        st.markdown("### 设置")
        top_k = st.slider("检索数量 (Top-K)", 1, 20, 5, key="sidebar_top_k")
        st.session_state.top_k = top_k

        st.divider()

        try:
            collections = client.list_collections()
            if collections:
                st.markdown("### 知识库统计")
                for c in collections:
                    st.metric(f"📚 {c['name']}", f"{c['count']} chunks")
        except Exception:
            pass

    return top_k
