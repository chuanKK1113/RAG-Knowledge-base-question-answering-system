import streamlit as st
import time

from components.sidebar import render_sidebar


def render():
    st.title("📤 上传文档")
    st.markdown("支持 **PDF** 和 **TXT** 格式的文件，上传后自动解析、分块并向量化存储。")

    uploaded_file = st.file_uploader(
        "选择文件",
        type=["pdf", "txt", "md", "csv"],
        help="上传 PDF/TXT 文件",
    )

    if uploaded_file is not None:
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        st.info(f"文件名: **{uploaded_file.name}** | 大小: {file_size_kb:.1f} KB")

        if st.button("🚀 开始上传并处理", type="primary"):
            with st.status("处理中...", expanded=True) as status:
                st.write("📄 正在解析文档...")
                try:
                    result = st.session_state.client.upload_document(
                        uploaded_file.getvalue(), uploaded_file.name
                    )
                    st.write(f"✅ 解析完成：{result['char_count']} 字符")
                    st.write(f"✂️ 分块完成：{result['chunk_count']} 个文本块")
                    st.write("🔢 向量化并存入 ChromaDB...")
                    st.write("✅ 全部完成！")
                    status.update(
                        label=f"上传成功！共 {result['chunk_count']} 个 chunks",
                        state="complete",
                    )
                    st.success(
                        f"文档 **{result['filename']}** 已成功摄入知识库 "
                        f"（{result['chunk_count']} chunks, {result['char_count']} 字符）"
                    )
                except Exception as e:
                    status.update(label="上传失败", state="error")
                    st.error(f"处理失败: {e}")


if __name__ == "__main__":
    st.set_page_config(page_title="上传文档", page_icon="📤")
    if "client" not in st.session_state:
        from api_client import APIClient
        st.session_state.client = APIClient("http://localhost:8000")
    if "top_k" not in st.session_state:
        st.session_state.top_k = 5
    render_sidebar(st.session_state.client)
    render()
