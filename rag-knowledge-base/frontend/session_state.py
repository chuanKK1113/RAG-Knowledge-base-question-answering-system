"""Shared session state initialization. Called once per page load."""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def _fetch_health(client):
    return client.health_check().get("status") == "ok"


def _fetch_collections(client):
    try:
        return client.list_collections()
    except Exception:
        return []


def prefetch_sidebar_data(client):
    """
    Fetch health and collections in parallel, updating session state caches.
    Respects TTL — if cache is still fresh, skips the network call entirely.
    """
    now = time.time()
    need_health = (
        st.session_state.health_ok is None
        or (now - st.session_state.health_checked_at) > 60
    )
    need_collections = (
        st.session_state.collections_cache is None
        or (now - st.session_state.collections_checked_at) > 60
    )

    if not need_health and not need_collections:
        return  # both caches are fresh

    futures = {}
    with ThreadPoolExecutor(max_workers=2) as pool:
        if need_health:
            futures[pool.submit(_fetch_health, client)] = "health"
        if need_collections:
            futures[pool.submit(_fetch_collections, client)] = "collections"

        for future in as_completed(futures):
            key = futures[future]
            try:
                if key == "health":
                    st.session_state.health_ok = future.result()
                    st.session_state.health_checked_at = now
                elif key == "collections":
                    st.session_state.collections_cache = future.result()
                    st.session_state.collections_checked_at = now
            except Exception:
                if key == "health":
                    st.session_state.health_ok = False
                    st.session_state.health_checked_at = now
                elif key == "collections":
                    st.session_state.collections_cache = []
                    st.session_state.collections_checked_at = now


def get_health(client, ttl: int = 60):
    """Cached health check: only re-check after TTL seconds."""
    now = time.time()
    if st.session_state.health_ok is None or (now - st.session_state.health_checked_at) > ttl:
        st.session_state.health_ok = client.health_check().get("status") == "ok"
        st.session_state.health_checked_at = now
    return st.session_state.health_ok


def get_collections(client, ttl: int = 60):
    """Cached collections list: only re-fetch after TTL seconds."""
    now = time.time()
    if st.session_state.collections_cache is None or (now - st.session_state.collections_checked_at) > ttl:
        try:
            st.session_state.collections_cache = client.list_collections()
        except Exception:
            st.session_state.collections_cache = []
        st.session_state.collections_checked_at = now
    return st.session_state.collections_cache
