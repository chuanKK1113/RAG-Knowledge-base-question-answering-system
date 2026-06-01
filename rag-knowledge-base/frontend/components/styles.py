"""Shared global CSS injected into every page for consistent white-pink theme."""
import streamlit as st

GLOBAL_CSS = """
<style>
    /* ========================================
       Base — page & sidebar
       ======================================== */
    .stApp { background: #fff5f7; }
    section[data-testid="stSidebar"] { background: #ffe4e8; }
    section[data-testid="stSidebar"] * { color: #2d2d2d; }

    /* Sidebar captions */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #8b5e66; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.02em;
    }
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #8b5e66 !important;
    }

    /* Sidebar metric values */
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #d81b60 !important; font-weight: 700 !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #6d4c55 !important; font-size: 0.72rem !important;
    }

    /* Sidebar slider */
    section[data-testid="stSidebar"] [data-testid="stThumbValue"] {
        color: #d81b60 !important; font-weight: 700;
    }

    /* Sidebar dividers */
    section[data-testid="stSidebar"] hr {
        border-color: #f0cad4; margin: 0.8rem 0;
    }

    /* Sidebar bottom API link */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"]:last-of-type {
        color: #b08890; font-size: 0.7rem;
    }

    /* ========================================
       Main content — typography
       ======================================== */
    h1, h2, h3, h4, h5, h6 { color: #2d2d2d; }
    p, span, div { color: #333333; }
    label { color: #5a4048; }

    /* Caption in main area */
    [data-testid="stCaptionContainer"] { color: #8b5e66; }
    [data-testid="stCaptionContainer"] p { color: #8b5e66 !important; }

    /* ========================================
       Alert boxes — info / success / error / warning
       ======================================== */
    /* info */
    [data-testid="stNotification"] .stAlert,
    div[data-testid="stNotificationContent"] {
        background-color: #fce4ec !important;
        border: 1px solid #f0cad4 !important;
        color: #6d3a48 !important;
        border-radius: 10px;
    }

    /* success */
    div[data-baseweb="notification"]:has(svg[title="CheckCircle"]) {
        background-color: #f3e5f5 !important;
        border-color: #e1bee7 !important;
    }

    /* info text */
    .stAlert p, .stAlert span { color: #6d3a48 !important; }

    /* Expander */
    [data-testid="stExpander"] { background: #ffffff; border: 1px solid #f0cad4; border-radius: 12px; }
    [data-testid="stExpander"] summary { color: #d81b60; font-weight: 600; }

    /* ========================================
       Chat
       ======================================== */
    /* User message bubble */
    [data-testid="stChatMessage"] {
        border-radius: 14px !important; padding: 0.8rem 1.2rem !important;
        background: #ffffff !important; border: 1px solid #f0cad4 !important;
        box-shadow: 0 1px 4px rgba(210,70,110,0.06);
    }

    /* Chat input bar */
    [data-testid="stChatInput"] > div {
        background: #ffffff !important; border: 1.5px solid #f0cad4 !important;
        border-radius: 14px !important; box-shadow: 0 2px 8px rgba(210,70,110,0.06);
    }
    [data-testid="stChatInput"] input {
        color: #2d2d2d !important;
    }
    [data-testid="stChatInput"] input::placeholder {
        color: #b08890 !important;
    }
    [data-testid="stChatInput"] button {
        color: #d81b60 !important;
    }

    /* ========================================
       Metrics
       ======================================== */
    [data-testid="stMetricValue"] { color: #d81b60 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #8b5e66 !important; }

    /* ========================================
       Status container
       ======================================== */
    [data-testid="stStatus"] {
        background: #ffffff !important; border: 1px solid #f0cad4 !important;
        border-radius: 12px; padding: 1rem !important;
    }

    /* ========================================
       Spinner
       ======================================== */
    [data-testid="stSpinner"] { border-top-color: #d81b60 !important; }

    /* ========================================
       File uploader
       ======================================== */
    [data-testid="stFileUploader"] section {
        background: #ffffff !important; border: 2px dashed #e8bcc6 !important;
        border-radius: 14px !important; padding: 1.5rem !important;
    }
    [data-testid="stFileUploader"] section:hover { border-color: #ec407a !important; }

    /* ========================================
       Buttons
       ======================================== */
    .stButton > button {
        border-radius: 10px !important; font-weight: 600 !important;
        transition: all 0.15s !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px); box-shadow: 0 4px 12px rgba(216,27,96,0.2);
    }

    /* Primary button (already uses primaryColor via config.toml) */
    .stButton > button[kind="primary"] {
        background: #d81b60 !important; border-color: #d81b60 !important; color: #fff !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: #c2185b !important; border-color: #c2185b !important;
    }

    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background: #ffffff !important; border-color: #f0cad4 !important; color: #d81b60 !important;
    }

    /* ========================================
       Horizontal rule / divider
       ======================================== */
    hr { border-color: #f0cad4 !important; }

    /* ========================================
       Hero (app.py homepage)
       ======================================== */
    .hero { text-align:center; padding:3rem 1rem 1.5rem; }
    .hero h1 { font-size:2.4rem; font-weight:800; margin-bottom:0.5rem; color:#c2185b; }
    .hero p { color:#8b5e66; font-size:1.05rem; max-width:600px; margin:0 auto; }

    /* ========================================
       Feature cards (app.py homepage)
       ======================================== */
    .card-row { display:flex; gap:1.2rem; justify-content:center; flex-wrap:wrap; margin:1.5rem 0 2rem; }
    .card { flex:1; min-width:220px; max-width:320px; padding:1.8rem 1.2rem; border-radius:14px;
            background:#ffffff; border:1px solid #f0cad4; text-align:center; cursor:pointer;
            transition:border-color 0.2s, transform 0.15s, box-shadow 0.15s;
            text-decoration:none; display:block; box-shadow:0 2px 8px rgba(210,70,110,0.07); }
    .card:hover { border-color:#ec407a; transform:translateY(-2px); box-shadow:0 4px 18px rgba(210,70,110,0.14); }
    .card .icon { font-size:2.2rem; margin-bottom:0.8rem; }
    .card .title { font-size:1.1rem; font-weight:700; color:#2d2d2d; margin-bottom:0.4rem; }
    .card .desc { font-size:0.82rem; color:#8b5e66; }

    /* ========================================
       Stats (app.py homepage)
       ======================================== */
    .stats-row { display:flex; gap:1rem; justify-content:center; margin:2rem 0; }
    .stat-box { padding:1rem 1.8rem; border-radius:12px; background:#ffffff; border:1px solid #f0cad4;
                text-align:center; box-shadow:0 2px 8px rgba(210,70,110,0.07); }
    .stat-box .num { font-size:1.6rem; font-weight:700; color:#d81b60; }
    .stat-box .label { font-size:0.75rem; color:#8b5e66; }

    /* ========================================
       Upload zone
       ======================================== */
    .upload-zone { border:2px dashed #e8bcc6; border-radius:14px; padding:2.5rem; text-align:center;
                   background:#ffffff; margin:1rem 0; }
    .upload-zone:hover { border-color:#ec407a; }

    /* ========================================
       Doc card
       ======================================== */
    .doc-card { display:flex; align-items:center; justify-content:space-between;
                padding:0.9rem 1.2rem; border-radius:10px; background:#ffffff;
                border:1px solid #f0cad4; margin-bottom:0.6rem;
                box-shadow:0 1px 4px rgba(210,70,110,0.05); }
    .doc-card:hover { border-color:#e8bcc6; }

    /* ========================================
       Source tags (chat citations)
       ======================================== */
    .source-tag { display:inline-block; padding:2px 10px; border-radius:20px;
                  background:#fce4ec; color:#ad1457; font-size:0.75rem; margin:2px 4px; }
</style>
"""


def inject_global_styles():
    """Inject the shared white-pink CSS into the current page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
