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
    status_df = get_data('filters', 'distinct_shipment_status.sql')
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