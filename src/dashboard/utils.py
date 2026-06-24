import streamlit as st
import pandas as pd
from src.database.query_runner import fetch_filtered_data

@st.cache_data(ttl=3600, show_spinner="Fetching latest logistics data...")
def get_data(folder: str, sql_file: str, params: dict | None = None) -> pd.DataFrame:
    """
    Centralized data gateway. Converts mutable lists into tuples before caching to prevent errors.
    """
    safe_params = {}
    if params:
        for k, v in params.items():
            safe_params[k] = tuple(v) if isinstance(v, list) else v
            
    return fetch_filtered_data(folder, sql_file, safe_params)