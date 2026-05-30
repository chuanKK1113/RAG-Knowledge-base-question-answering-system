import streamlit as st

from components.sidebar import render_sidebar


def render():
    st.title("📋 管理知识库")
    st.markdown("查看已上传的文档，支持删除操作。")

    if st.button("🔄 刷新列表"):
        st.rerun()

    try:
        docs = st.session_state.client.list_documents()
    except Exception as e:
        st.error(f"获取文档列表失败: {e}")
        return

    if not docs:
        st.info("暂无已上传的文档。去 [上传文档](/1_Upload_Documents) 添加。")
        return

    st.markdown(f"共 **{len(docs)}** 个文档")

    for doc in docs:
        with st.expander(f"📄 {doc['filename']} ({doc['chunk_count']} chunks)"):
            st.caption(f"ID: {doc['id']}")
            st.metric("Chunks", doc["chunk_count"])
            if st.button("🗑️ 删除", key=f"del_{doc['id']}", type="secondary"):
                try:
                    result = st.session_state.client.delete_document(doc["id"])
                    st.success(f"已删除，移除 {result.get('chunks_removed', 0)} 个 chunks")
                    st.rerun()
                except Exception as e:
                    st.error(f"删除失败: {e}")


if __name__ == "__main__":
    st.set_page_config(page_title="管理知识库", page_icon="📋")
    if "client" not in st.session_state:
        from api_client import APIClient
        st.session_state.client = APIClient("http://localhost:8000")
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    render_sidebar(st.session_state.client)
    render()
