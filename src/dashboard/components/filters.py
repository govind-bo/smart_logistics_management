
import streamlit as st
import pandas as pd
from src.dashboard.utils import get_data

def render_filters() -> dict:
    """
    Render dashboard filters and return the selected values.
    """
    # 1. Initialize the dictionary
    filters = {
        "start_date": None,
        "end_date": None,
        "origin": [],
        "destination": [],
        "shipment_status": [],
        "courier": []
    }

    st.sidebar.header("Global Filters")

    # 2. DATE FILTER (This MUST happen first so the other filters have a date boundary!)
   
    date_bounds_df = get_data('filters', 'date_range_bounds.sql') 
    min_date = pd.to_datetime(date_bounds_df['min_date'].iloc[0]).date()
    max_date = pd.to_datetime(date_bounds_df['max_date'].iloc[0]).date()

    selected_dates = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Safely unpack dates
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        filters["start_date"] = selected_dates[0]
        filters["end_date"] = selected_dates[1]
    else:
        filters["start_date"] = min_date
        filters["end_date"] = max_date

    # 3. CASCADING FILTERS
    # Now that start_date and end_date are in the 'filters' dict, we pass it down!

    # -- Origin Filter --
    origin_df = get_data('filters', 'distinct_origin.sql', params=filters)
    # Sort in python using .sort() for clean UI
    origins = origin_df['origin'].dropna().tolist()
    origins.sort()
    filters["origin"] = st.sidebar.multiselect("Origin City", options=origins)

    # -- Destination Filter --
    dest_df = get_data('filters', 'distinct_destination.sql', params=filters)
    destinations = dest_df['destination'].dropna().tolist()
    destinations.sort()
    filters["destination"] = st.sidebar.multiselect("Destination City", options=destinations)

    # -- Shipment Status Filter (Where your error was!) --
    status_df = get_data('filters', 'distinct_shipment_status.sql', params=filters)
    statuses = status_df['shipment_status'].dropna().tolist()
    statuses.sort()
    filters["shipment_status"] = st.sidebar.multiselect("Shipment Status", options=statuses)

    # -- Courier Filter --
    courier_df = get_data('filters', 'distinct_courier.sql', params=filters)
    couriers = courier_df['courier_name'].dropna().tolist()
    couriers.sort()
    filters["courier"] = st.sidebar.multiselect("Courier Name", options=couriers)

    return filters


'''
import streamlit as st
from src.dashboard.utils import get_data

def render_filters() -> dict:
    """
    Render dashboard filters and return the selected values.
    """
    filters = {
        "start_date": None,
        "end_date": None,
        "origin": [],
        "destination": [],
        "shipment_status": [],
        "courier": []
    }

    st.sidebar.header("Filters")

    # Order Date Range Bounds
    date_bounds_df = get_data('filters', 'date_range_bounds.sql')
    min_date = date_bounds_df.loc[0, 'min_date']
    max_date = date_bounds_df.loc[0, 'max_date']

    selected_dates = st.sidebar.date_input(
        'Order Date range',
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        filters['start_date'] = selected_dates[0]
        filters['end_date'] = selected_dates[1]
    else:
        filters["start_date"] = selected_dates
        filters["end_date"] = selected_dates

    # Shipment Status Filter
    status_df = get_data('filters', 'distinct_shipment_status.sql', params=filters)
    filters['shipment_status'] = st.sidebar.multiselect(
        'Shipment status',
        options=status_df['shipment_status'].tolist()
    )

    # Origin Filter
    origin_df = get_data('filters', 'distinct_origin.sql')
    filters['origin'] = st.sidebar.multiselect(
        'Origin',
        options=origin_df['origin'].tolist()
    )

    # Destination Filter
    destination_df = get_data('filters', 'distinct_destination.sql')
    filters['destination'] = st.sidebar.multiselect(
        'Destination',
        options=destination_df['distinct_destination'].tolist() if 'distinct_destination' in destination_df.columns else destination_df.iloc[:,0].tolist()
    )

    # Courier Filter
    courier_df = get_data('filters', 'distinct_courier.sql')
    filters['courier'] = st.sidebar.multiselect(
        'Courier name',
        options=courier_df['name'].tolist()
    )
     
    return {
        "start_date": filters["start_date"],
        "end_date": filters["end_date"],
        "origin": filters["origin"],
        "destination": filters["destination"],
        "shipment_status": filters["shipment_status"],
        "courier": filters["courier"]
    }

'''