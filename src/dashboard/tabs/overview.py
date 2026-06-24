import streamlit as st
from src.dashboard.utils import get_data
from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import create_bar_chart, create_line_chart
from src.dashboard.components.processors.overview_processor import calculate_overview_metrics, prepare_overview_datasets

def render_overview_page() -> None:
    '''
    Renders the Operations Overview page of the dashboard
    '''

    st.title("Smart Logistics Management & Analytics Platform")

    # render sidebar filter dropdown selectors -------------------------------------
    filters = render_filters()

    # download row level records from the database once ----------------------------
    df = get_data("tabs", "operations_overview.sql", params=filters)

    if df.empty:
        st.warning("No shipment data available for the chosen filters.")
    else:
        # run background functions to do calculations -----------------------------
        summary_metrics = calculate_overview_metrics(df)

        # display core kpi card containers row grid --------------------------------
        st.markdown("### Core Operations KPIs")
        
        # render row 1 of kpi cards ------------------------------------------------
        row1 = st.columns(4)
        with row1[0]:
            display_kpi("Total Shipments", f"{summary_metrics['total_shipments']:,}")
        with row1[1]:
            display_kpi("Delivered %", f"{summary_metrics['delivered_pct']:.2f}%")
        with row1[2]:
            display_kpi("In Transit %", f"{summary_metrics['in_transit_pct']:.2f}%")
        with row1[3]:
            display_kpi("Cancelled %", f"{summary_metrics['cancelled_pct']:.2f}%")

        # render row 2 of kpi cards ------------------------------------------------
        row2 = st.columns(4)
        with row2[0]:
            display_kpi("Avg Duration (Days)", f"{summary_metrics['avg_duration']:.2f}")
        with row2[1]:
            display_kpi("Total Cost", f"${summary_metrics['total_cost']:,.0f}")
        with row2[2]:
            display_kpi("Active Routes", f"{summary_metrics['active_routes']:,}")
        with row2[3]:
            display_kpi("Total Couriers", f"{summary_metrics['total_couriers']:,}")

        st.markdown("---")
        
        # timeline toggle layout options block -------------------------------------
        col_header, col_toggle = st.columns([3, 1])
        with col_header:
            st.markdown("### Performance & Volume Trend Analytics")
        with col_toggle:
            time_view = st.radio("View Trend By:", ["Month", "Day"], index=0, horizontal=True)

        # build charts datasets using selected toggle option -----------------------
        plot_datasets = prepare_overview_datasets(df, granularity = time_view)

        # display tier 1 charts for status mix and volumes -------------------------
        plot_row1 = st.columns(2)
        with plot_row1[0]:
            st.plotly_chart(create_bar_chart(
                plot_datasets["status_mix"], x='status', y='shipment_count',
                title='Shipment Status Distribution', xaxis_title='Current Status', yaxis_title='Number of Shipments',
                text='shipment_count'
            ), use_container_width=True)
            
        with plot_row1[1]:
            st.plotly_chart(create_line_chart(
                plot_datasets["timeline_trend"], x='time_period', y='timeline_shipments',
                title=f'Shipment Volume Trend ({time_view} Wise)', xaxis_title=time_view, yaxis_title='Number of Shipments'
            ), use_container_width=True)

        # display tier 2 financial operational track line plot ---------------------
        st.markdown("#### Financial Tracking")
        st.plotly_chart(create_line_chart(
            plot_datasets["timeline_trend"], x='time_period', y='timeline_costs',
            title=f'Operational Cost Trend ({time_view} Wise)', xaxis_title=time_view, yaxis_title='Total Cost ($)'
        ), use_container_width=True)

        # display tier 3 warehouse capacity limits and storage traffic bars --------
        st.markdown("#### Distribution Center Metrics")
        plot_row2 = st.columns(2)
        with plot_row2[0]:
            st.plotly_chart(create_bar_chart(
                plot_datasets["wh_capacity"], x='warehouse_capacity', y='warehouse_city',
                title='Warehouse Capacity Comparison', xaxis_title='Unit Capacity Limit', yaxis_title='Warehouse Location',
                orientation='h'
            ), use_container_width=True)
            
        with plot_row2[1]:
            st.plotly_chart(create_bar_chart(
                plot_datasets["wh_traffic"], x='warehouse_city', y='shipment_count',
                title='High Traffic Warehouse Cities', xaxis_title='Warehouse Location', yaxis_title='Shipments Handled',
                text='shipment_count'
            ), use_container_width=True)
