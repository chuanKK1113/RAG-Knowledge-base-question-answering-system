"""Shared session state initialization. Called once per page load."""
import streamlit as st
from api_client import APIClient


def init_session():
    if "client" not in st.session_state:
        st.session_state.client = APIClient("http://localhost:8000")
    if "top_k" not in st.session_state:
        st.session_state.top_k = 8
    if "health_ok" not in st.session_state:
        st.session_state.health_ok = None
    if "health_checked_at" not in st.session_state:
        st.session_state.health_checked_at = 0
    if "collections_cache" not in st.session_state:
        st.session_state.collections_cache = None
    if "collections_checked_at" not in st.session_state:
        st.session_state.collections_checked_at = 0
    if "messages" not in st.session_state:
        st.session_state.messages = []


def get_health(client, ttl: int = 30):
    """Cached health check: only re-check after TTL seconds."""
    import time
    now = time.time()
    if st.session_state.health_ok is None or (now - st.session_state.health_checked_at) > ttl:
        st.session_state.health_ok = client.health_check().get("status") == "ok"
        st.session_state.health_checked_at = now
    return st.session_state.health_ok


def get_collections(client, ttl: int = 30):
    """Cached collections list: only re-fetch after TTL seconds."""
    import time
    now = time.time()
    if st.session_state.collections_cache is None or (now - st.session_state.collections_checked_at) > ttl:
        try:
            st.session_state.collections_cache = client.list_collections()
        except Exception:
            st.session_state.collections_cache = []
        st.session_state.collections_checked_at = now
    return st.session_state.collections_cache
