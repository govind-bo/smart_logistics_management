import streamlit as st
import pandas as pd
from src.database.query_runner import run_sql_file

@st.cache_data
def get_data(folder: str, sql_file: str, params = None) -> pd.DataFrame:
    return run_sql_file(
        folder,
        sql_file,
        params
    )