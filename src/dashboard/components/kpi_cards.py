import streamlit as st

def display_kpi(label: str, value, suffix: str = "", caption: str = None) -> None:
    '''
    Display individual kpi.
    '''
    st.metric(
        label = label,
        value = f"{value}{suffix}"
    )
    if caption:
        st.caption(caption)