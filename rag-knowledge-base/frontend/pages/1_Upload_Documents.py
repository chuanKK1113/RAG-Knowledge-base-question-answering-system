import streamlit as st
from session_state import init_session
from components.sidebar import render_sidebar
from components.styles import inject_global_styles

init_session()
render_sidebar(st.session_state.client)
inject_global_styles()

st.markdown("""
<div style="text-align:center; padding:1.5rem 0 1rem;">
    <div style="font-size:2.5rem;">📤</div>
    <h2 style="margin:0.3rem 0; color:#c2185b;">上传文档</h2>
    <p style="color:#8b5e66;">支持 PDF、TXT、MD、CSV — 自动解析 · 分块 · 向量化</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "拖拽文件到此处或点击选择",
    type=["pdf", "txt", "md", "csv"],
    label_visibility="collapsed",
)

if uploaded_file is not None:
    file_size_kb = len(uploaded_file.getvalue()) / 1024
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"**{uploaded_file.name}** · {file_size_kb:.1f} KB")
    with col_b:
        do_upload = st.button("🚀 开始处理", type="primary", use_container_width=True)

    if do_upload:
        with st.status("正在处理...", expanded=True) as status:
            try:
                st.write("📄 解析文档...")
                result = st.session_state.client.upload_document(
                    uploaded_file.getvalue(), uploaded_file.name
                )
                st.write(f"✅ 解析完成 — {result['char_count']:,} 字符")
                st.write(f"✂️ 生成 {result['chunk_count']} 个文本块")
                st.write("🔢 向量化 & 写入 ChromaDB...")
                status.update(
                    label=f"✅ 完成！{result['filename']} ({result['chunk_count']} chunks)",
                    state="complete",
                )
                st.balloons()

                # Invalidate collection cache
                st.session_state.collections_cache = None

            except Exception as e:
                status.update(label="处理失败", state="error")
                st.error(str(e))
