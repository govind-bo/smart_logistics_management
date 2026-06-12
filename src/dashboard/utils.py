import streamlit as st
import pandas as pd
from src.database.query_runner import fetch_filtered_data

@st.cache_data(ttl = 3600)  # caching wuill expire after an hour
def get_data(folder: str, sql_file: str, params: dict = None) -> pd.DataFrame:
    """
    Centralized data gateway. Checks cache first, then queries the database.
    If params is passed, fetch_filtered_data appends dynamic multi-select strings.
    If params is empty or None, it smoothly runs a standard raw SQL query.
    """
    # Use the smart function so dynamic filters always work
    return fetch_filtered_data(folder, sql_file, params or {})