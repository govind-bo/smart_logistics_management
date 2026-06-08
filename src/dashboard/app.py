from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import create_bar_chart
from src.database.query_runner import run_smart_query

st.set_page_config(
    page_title="Smart Logistics Analytics",
    layout="wide"
)

st.title("Smart Logistics Management & Analytics Platform")

# SIDEBAR FILTERS
filters = render_filters()

# DATA PROCESSING LAYER
df = run_smart_query("overview", "executive_kpis.sql", params=filters)

if df.empty:
    st.warning("No shipment data discovered within chosen filter scope.")
else:
    # Vectorized Metric Computations via Pandas
    total_shipments = len(df)
    
    status_counts = df['status'].value_counts()
    delivered_shipment_percentage = (status_counts.get('Delivered', 0) / total_shipments) * 100
    cancelled_shipment_percentage = (status_counts.get('Cancelled', 0) / total_shipments) * 100
    in_transit_shipment_percentage = (status_counts.get('In Transit', 0) / total_shipments) * 100
    
    delivered_df = df[(df['status'] == 'Delivered') & (df['delivery_date'].notna())]
    if not delivered_df.empty:
        delivery_days = (pd.to_datetime(delivered_df['delivery_date']) - pd.to_datetime(delivered_df['order_date'])).dt.days
        avg_delivery_days = delivery_days.mean()
        
        hours_elapsed = (pd.to_datetime(delivered_df['delivery_date']) - pd.to_datetime(delivered_df['order_date'])).dt.total_seconds() / 3600.0
        on_time_mask = hours_elapsed <= delivered_df['avg_time_hours']
        on_time_delivery_percentage = (on_time_mask.sum() / len(delivered_df)) * 100
    else:
        avg_delivery_days = 0.0
        on_time_delivery_percentage = 0.0

    total_operational_cost = df['total_cost'].sum()
    active_routes = df['route_id'].nunique()
    
    # Placeholder or hardcoded fallbacks for metrics outside calculation spectrum
    total_couriers = df['courier_name'].nunique() 

    # RENDER KPI ROW 1
    row1col1, row1col2, row1col3, row1col4 = st.columns(4)
    with row1col1:
        display_kpi("Total Shipments", int(total_shipments))
    with row1col2:
        display_kpi("Delivered %", round(delivered_shipment_percentage, 2), "%")
    with row1col3:
        display_kpi("In Transit %", round(in_transit_shipment_percentage, 2), "%")
    with row1col4:
        display_kpi("Cancelled %", round(cancelled_shipment_percentage, 2), "%")

    # RENDER KPI ROW 2
    row2col1, row2col2, row2col3, row2col4 = st.columns(4)
    with row2col1:
        display_kpi("Average Delivery Duration", round(avg_delivery_days, 2), " Days")
    with row2col2:
        display_kpi("Total Operational Cost", round(total_operational_cost, 2), " $")
    with row2col3:
        display_kpi("Active Routes", int(active_routes))
    with row2col4:
        display_kpi("Total Active Couriers", int(total_couriers))

    # VISUALIZATIONS
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    
    # Structure shipment status aggregates for bar chart feeding
    status_distribution_df = status_counts.reset_index()
    status_distribution_df.columns = ['status', 'shipment_count']

    fig = create_bar_chart(
        status_distribution_df, 
        x='status',
        y='shipment_count',
        xaxis_title='Shipment status',
        yaxis_title='Number of Shipments',
        text='shipment_count'
    )

    with col1:
        st.subheader("Shipment Status Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.empty()