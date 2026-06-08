import streamlit as st

def display_kpi(label: str, value, suffix: str = "") -> None:

    st.metric(
        label = label,
        value = f"{value}{suffix}"
    )