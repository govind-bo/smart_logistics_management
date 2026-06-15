import streamlit as st
import pandas as pd
from src.dashboard.utils import get_data

def render_filters() -> dict:
    st.sidebar.header("Global Filters")

    # 1. Handle Dates safely
    try:
        bounds_df = get_data('filters', 'date_range_bounds.sql')
        min_date = pd.to_datetime(bounds_df['min_date'].iloc[0]).date()
        max_date = pd.to_datetime(bounds_df['max_date'].iloc[0]).date()
    except Exception:
        min_date = pd.to_datetime('2020-01-01').date()
        max_date = pd.to_datetime('today').date()

    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date))
    start_date = date_range[0] if date_range else min_date
    end_date = date_range[1] if len(date_range) == 2 else start_date

    # 2. Extract current UI state directly
    curr_origin = st.session_state.get('origin_picker', [])
    curr_dest = st.session_state.get('dest_picker', [])
    curr_status = st.session_state.get('status_picker', [])
    curr_courier = st.session_state.get('courier_picker', [])

    # 3. Helper to get valid options for multidirectional filtering
    def get_valid_options(sql_file: str, exclude_key: str):
        # Pass all current selections EXCEPT the widget we are generating options for
        params = {
            "start_date": start_date, "end_date": end_date,
            "origin": curr_origin if exclude_key != 'origin' else [],
            "destination": curr_dest if exclude_key != 'destination' else [],
            "shipment_status": curr_status if exclude_key != 'shipment_status' else [],
            "courier": curr_courier if exclude_key != 'courier' else []
        }
        df = get_data('filters', sql_file, params=params)
        
        # ISSUE 2 FIXED: .unique() prevents duplicates, sorted() alphabetizes them (A-Z)
        return sorted(df.iloc[:, 0].dropna().unique().tolist()) if not df.empty else []

    # Fetch fresh valid options based on cross-filters
    valid_origins = get_valid_options('distinct_origin.sql', 'origin')
    valid_dests = get_valid_options('distinct_destination.sql', 'destination')
    valid_statuses = get_valid_options('distinct_shipment_status.sql', 'shipment_status')
    valid_couriers = get_valid_options('distinct_courier.sql', 'courier')

    # 4. ISSUE 3 FIXED: Safely clean up session state BEFORE rendering to prevent Streamlit crashes
    if 'origin_picker' in st.session_state:
        st.session_state['origin_picker'] = [x for x in curr_origin if x in valid_origins]
    if 'dest_picker' in st.session_state:
        st.session_state['dest_picker'] = [x for x in curr_dest if x in valid_dests]
    if 'status_picker' in st.session_state:
        st.session_state['status_picker'] = [x for x in curr_status if x in valid_statuses]
    if 'courier_picker' in st.session_state:
        st.session_state['courier_picker'] = [x for x in curr_courier if x in valid_couriers]

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