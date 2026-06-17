import streamlit as st
import pandas as pd
from src.dashboard.utils import get_data

# 1. THE CALLBACK: This safely wipes the memory for just the dropdowns
def clear_dropdowns():
    '''
    THE CALLBACK: This safely wipes the memory for just the dropdowns
    '''
    for key in ['origin_picker', 'dest_picker', 'status_picker', 'courier_picker']:
        st.session_state[key] = []

def render_filters() -> dict:
    st.sidebar.header("Global Filters")

    # 2. Handle Dates safely
    try:
        bounds_df = get_data('filters', 'date_range_bounds.sql')
        min_date = pd.to_datetime(bounds_df['min_date'].iloc[0]).date()
        max_date = pd.to_datetime(bounds_df['max_date'].iloc[0]).date()
    except Exception:
        min_date = pd.to_datetime('2020-01-01').date()
        max_date = pd.to_datetime('today').date()

    all_time = st.sidebar.checkbox("Select All Time", value=True)

    if all_time:
        start_date = min_date
        end_date = max_date
        st.sidebar.date_input("Date Range", value=(min_date, max_date), disabled=True)
    else:
        date_range = st.sidebar.date_input(
            "Date Range", 
            value=(min_date, max_date),             # the values selected by default
            min_value=min_date,                     # the min value a user is allowed to select
            max_value=max_date                      
        )
        start_date = date_range[0] if date_range else min_date
        end_date = date_range[1] if len(date_range) == 2 else start_date

    st.sidebar.divider() 

    
    # Button to let user clear all filters at once
    st.sidebar.button("Clear Filters", on_click = clear_dropdowns, use_container_width = True)

    # 3. Extract current UI state directly
    curr_origin = st.session_state.get('origin_picker', [])
    curr_dest = st.session_state.get('dest_picker', [])
    curr_status = st.session_state.get('status_picker', [])
    curr_courier = st.session_state.get('courier_picker', [])

    # 4. Helper to get valid options
    def get_valid_options(sql_file: str, exclude_key: str, current_selections: list):
        params = {
            "start_date": start_date, 
            "end_date": end_date,     
            "origin": curr_origin if exclude_key != 'origin' else [],
            "destination": curr_dest if exclude_key != 'destination' else [],
            "shipment_status": curr_status if exclude_key != 'shipment_status' else [],
            "courier": curr_courier if exclude_key != 'courier' else []
        }
        df = get_data('filters', sql_file, params=params)
        db_options = df.iloc[:, 0].dropna().unique().tolist() if not df.empty else []

        combined_options = list(set(db_options + current_selections))
        return sorted(combined_options)

    # Fetch fresh valid options, passing the current selections to protect them
    valid_origins = get_valid_options('distinct_origin.sql', 'origin', curr_origin)
    valid_dests = get_valid_options('distinct_destination.sql', 'destination', curr_dest)
    valid_statuses = get_valid_options('distinct_shipment_status.sql', 'shipment_status', curr_status)
    valid_couriers = get_valid_options('distinct_courier.sql', 'courier', curr_courier)

    # 5. Render Filters
    selected_origin = st.sidebar.multiselect('Origin City', options=valid_origins, key='origin_picker')
    selected_dest = st.sidebar.multiselect('Destination City', options=valid_dests, key='dest_picker')
    selected_status = st.sidebar.multiselect('Shipment Status', options=valid_statuses, key='status_picker')
    selected_courier = st.sidebar.multiselect('Courier Name', options=valid_couriers, key='courier_picker')

    return {
        "start_date": start_date,
        "end_date": end_date,
        "origin": selected_origin,
        "destination": selected_dest,
        "shipment_status": selected_status,
        "courier": selected_courier
    }