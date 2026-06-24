import streamlit as st

from src.dashboard.utils import get_data
from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import (
    create_bar_chart, 
    create_pie_chart, 
    create_scatter_chart,
    display_data_table
)

from src.dashboard.components.processors.warehouse_processor import (
    calculate_warehouse_metrics,
    prepare_warehouse_datasets
)

def render_warehouse_page() -> None:
    """
    Renders the Warehouse & Network Insights page of the dashboard
    """
    st.title('Warehouse & Network Insights')

    # region Data Fetching
    filters = render_filters()
    df = get_data('tabs', 'warehouse_utilization.sql', params=filters)

    if df.empty:
        st.warning('No data available for the chosen filters')
        return
    # end region 

    # region KPIs
    summary_metrics = calculate_warehouse_metrics(df)
    st.markdown('### Network Overview')
    row1 = st.columns(4)

    with row1[0]:
        available_hubs = summary_metrics['total_warehouses']
        display_kpi('Total Active Warehouses', f"{available_hubs:,}")
        
    with row1[1]:
        display_kpi('Total Network Capacity', f"{summary_metrics['total_capacity']:,}")
    
    with row1[2]:
        high_hub = summary_metrics['highest_activity_hub']
        high_act = summary_metrics['highest_activity_count']
        display_kpi('Highest Activity Hub',
                    str(high_hub),
                    caption=f"Total Shipments: {high_act:,}" if high_hub != 'N/A' else None)
        
    with row1[3]:
        under_hub = summary_metrics['most_underutilized_hub']
        under_ratio = summary_metrics['lowest_utilization_ratio']
        display_kpi('Most Underutilized Hub',
                    str(under_hub),
                    caption=f"Utilization Ratio: {under_ratio:.1f}%" if under_hub != 'N/A' else None)
    # end region

    # region Capacity vs Demand (Controlled)
    st.markdown('---')
    st.markdown('### Capacity vs Demand Rankings')

    controls_row = st.columns([1, 1, 2])
    
    with controls_row[0]:
        sort_metric_dict = {
            'capacity': 'Total Capacity',
            'activity_count': 'Shipment Activity',
            'utilization_ratio': 'Utilization Ratio'
        }
        sort_by = st.selectbox(
            'Sort by Metric',
            options=['capacity', 'activity_count', 'utilization_ratio'],
            format_func=lambda x: sort_metric_dict[x],
            index=0
        )
        
    with controls_row[1]:
        sort_choice = st.radio(
            'Sort by:',
            ['Highest', 'Lowest'],
            index=0,
            horizontal=True
        )
        is_ascending = True if sort_choice == 'Lowest' else False
        
    with controls_row[2]:
        if available_hubs > 1:
            display_limit = st.slider(
                "Number of Hubs to Display",
                min_value=1,
                max_value=available_hubs,
                value=min(10, available_hubs)
            )
        else:
            display_limit = available_hubs
            if available_hubs == 1:
                st.caption("Only 1 warehouse available for current filters.")

    datasets = prepare_warehouse_datasets(df, sort_by=sort_by, is_ascending=is_ascending, display_limit=display_limit)

    row2 = st.columns(2)
    
    with row2[0]:
        st.plotly_chart(create_bar_chart(
            df=datasets['capacity_bar'],
            x='capacity',
            y='city',
            orientation='h',
            title='Static Capacity by Hub',
            xaxis_title='Total Capacity',
            yaxis_title='Warehouse City',
            texttemplate='%{x:.2s}',
            hover_data=['warehouse_id']
        ), use_container_width=True)

    with row2[1]:
        st.plotly_chart(create_bar_chart(
            df=datasets['activity_bar'],
            x='activity_count',
            y='city',
            orientation='h',
            title='Shipment Activity by Hub',
            xaxis_title='Total Shipments',
            yaxis_title='Warehouse City',
            texttemplate='%{x:.0f}',
            hover_data=['warehouse_id']
        ), use_container_width=True)
    # end region

    # region Core Insights (Freed)
    st.markdown('---')
    st.markdown('### Operational Efficiency')
    
    row3 = st.columns(2)

    with row3[0]:
        st.plotly_chart(create_scatter_chart(
            df=datasets['correlation'],
            x='capacity',
            y='activity_count',
            size='utilization_ratio',
            title='Network Correlation: Capacity vs Activity',
            xaxis_title='Warehouse Capacity',
            yaxis_title='Total Shipment Activity',
            opacity=0.7,
            hover_data={
                'capacity': ':,',
                'activity_count': ':,',
                'utilization_ratio': ':.1f',
                'city': True, 
                'warehouse_id': True
            },
            labels={
                'capacity': 'Capacity',
                'activity_count': 'Activity (Shipments)',
                'utilization_ratio': 'Utilization (%)',
                'city': 'City',
                'warehouse_id': 'Warehouse ID'
            }
        ), use_container_width=True)
    with row3[1]:
        st.plotly_chart(create_pie_chart(
            df=datasets['vehicle_mix'],
            names='vehicle_type',
            values='activity_count',
            title='Vehicle Mix at Network Hubs',
            hole=0.4,
            texttemplate="%{label}<br>%{value:.2s} (%{percent:.1%})"
        ), use_container_width=True)
    # end region
    
    # region Network Table
    st.markdown('---')
    st.markdown("##### Warehouse Network Directory")
    display_data_table(
        df=datasets['network_table'],
        height=400
    )
    # end region