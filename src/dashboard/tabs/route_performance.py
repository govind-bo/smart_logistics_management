# src/dashboard/pages/route_performance.py

import streamlit as st

from src.dashboard.utils import get_data
from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import (
    create_bar_chart, 
    create_line_chart, 
    create_pie_chart, 
    create_scatter_chart,
    create_heatmap,
    display_data_table
)
from src.dashboard.components.processors.route_processor import (
    calculate_route_performance_metrics,
    prepare_route_datasets
)

def render_route_performance_page() -> None:
    """
    Renders the Route Performance page of the dashboard
    """
    st.title('Route Performance')

    # region Data Fetching
    filters = render_filters()
    df = get_data('tabs', 'route_performance.sql', params=filters)

    if df.empty:
        st.warning('No Shipment data available for the chosen filters')
        return
    # end region 

    # region KPIs
    summary_route_metrics = calculate_route_performance_metrics(df)
    st.markdown('### Route KPIs')
    row1 = st.columns(4)

    # kpi 1 - average delivery time
    with row1[0]:
        avg_delivery_time = summary_route_metrics['avg_delivery_time']
        days = int(avg_delivery_time / 24)
        hrs = int(avg_delivery_time % 24)
        
        if days == 1 and hrs == 1:
            day_hrs = f"{days} day {hrs} hr"
        elif days == 1 and hrs > 1:
            day_hrs = f"{days} day {hrs} hrs"
        elif days > 1 and hrs == 1:
            day_hrs = f"{days} days {hrs} hr"
        else:
            day_hrs = f"{days} days {hrs} hrs"
        
        display_kpi('Average Delivery Time',
                    f"{avg_delivery_time:,.1f}",
                    suffix=' hrs',
                    caption=day_hrs if days > 0 else None
        )
        
    # kpi 2 - fastest route
    with row1[1]:
        fast_route_id = summary_route_metrics['fastest_route']
        fast_route_origin = summary_route_metrics['fastest_origin']
        fast_route_destination = summary_route_metrics['fastest_destination']
        display_kpi('Fastest Route',
                    str(fast_route_id),
                    caption=f"{fast_route_origin} -> {fast_route_destination}" if fast_route_origin else "N/A")
    
    # kpi 3 - slowest route
    with row1[2]:
        slow_route_id = summary_route_metrics['slowest_route']
        slow_route_origin = summary_route_metrics['slowest_origin']
        slow_route_destination = summary_route_metrics['slowest_destination']
        display_kpi('Slowest Route',
                    str(slow_route_id),
                    caption=f"{slow_route_origin} -> {slow_route_destination}" if slow_route_origin else "N/A")
        
    # kpi 4 - consistently delayed routes
    with row1[3]:
        consistently_delayed_routes = summary_route_metrics['consistently_delayed_routes']
        total_routes = summary_route_metrics['total_routes']
        display_kpi('Consistently Delayed Routes',
                    str(consistently_delayed_routes),
                    caption=f"Total Routes - {total_routes}")
    # end region

    # region Route Rankings
    st.markdown('---')
    st.markdown('### Route Rankings')

    available_routes = df['route_id'].nunique()
    delayed_chart_col, sort_controls_col = st.columns([5, 2])

    # --------------- Interactive Controls ---------------
    with sort_controls_col:
        st.markdown('##### Chart Controls')
        st.caption('Applies to Route Rankings')
        
        available_routes = df['route_id'].nunique()

        # Only render the slider if there are at least 2 routes to slide between
        if available_routes > 1:
            display_limit = st.slider(
                'Number of Routes to Display', 
                min_value=1, 
                max_value=available_routes, 
                value=min(available_routes, 15)
            )
        else:
            # Fallback for 0 or 1 route
            display_limit = available_routes
            if available_routes == 1:
                st.caption("Only 1 route available for current filters.")
        
        sort_choice = st.radio(
            'Sort by:',
            ['Highest', 'Lowest'],
            index=0,
            horizontal=True
        )
        is_ascending = True if sort_choice == 'Lowest' else False

        sort_metric_dict = {
            'route_id': 'Route ID',
            'volume': 'Total Volume',
            'total_weight': 'Total Weight',
            'total_shipments_by_group': 'Total Shipments',
            'avg_delay': 'Average Delay',
            'relative_avg_delay': 'Average Delay (Relative)'
        }
        
        sort_by = st.selectbox(
            'Sort by Metric',
            options=sorted(['relative_avg_delay', 'avg_delay', 'volume', 'total_weight', 'total_shipments_by_group']),
            format_func=lambda x: sort_metric_dict[x],
            index=1
        )

    route_datasets = prepare_route_datasets(df, sort_by=sort_by, is_ascending=is_ascending, display_limit=display_limit)
    
    if route_datasets['avg_del_time_route'] is not None:
        
        # 1. Most Delayed Routes (Main horizontal bar beside controls)
        with delayed_chart_col:
            st.plotly_chart(create_bar_chart(
                df=route_datasets['delayed_routes'],
                x='avg_delay',
                y='route_id',
                orientation='h',
                title=f"Most Delayed Routes",
                xaxis_title='Average Delay (Hrs)',
                yaxis_title='Route ID',
                hover_data={
                    'route_id': True,
                    'origin': True,
                    'destination': True,
                    'avg_delay': ':.1f hrs'
                },
                labels={
                    'route_id': 'Route ID',
                    'origin': 'Origin',
                    'destination': 'Destination',
                    'avg_delay': 'Avg Delay'
                },
                texttemplate='%{x:.1f}h'
            ), use_container_width=True)

        # 2 & 3. Side-by-Side Efficiency Charts
        eff_col1, eff_col2 = st.columns(2)
        
        with eff_col1:
            st.plotly_chart(create_bar_chart(
                df=route_datasets['avg_del_time_route'],
                x='route_id',
                y='avg_del_time',
                title='Average Delivery Time by Route',
                xaxis_title='Route ID',
                yaxis_title='Average Delivery Time (Hrs)',
                hover_data={
                    'route_id': True, 
                    'origin': True, 
                    'destination': True,
                    'avg_del_time': ':.1f hrs',  
                    'distance_km': True          
                },
                labels={
                    'route_id': 'Route ID',
                    'origin': 'Origin',
                    'destination': 'Destination',
                    'distance_km': 'Distance (kms)',
                    'avg_del_time': 'Delivery Time (avg)'
                },
                texttemplate='%{y:.1f}h'
            ), use_container_width=True)

        with eff_col2:
            st.plotly_chart(create_bar_chart(
                df=route_datasets['exp_vs_act_del_time'],
                x='route_id',
                y='Hours',
                color='Time Category',
                barmode='group',
                title='Expected vs Actual Delivery Time',
                xaxis_title='Route ID',
                yaxis_title='Time (Hrs)',
                hover_data={
                    'route_id': True,
                    'origin': True,
                    'destination': True,
                    'distance_km': True,
                    'Hours': ':.1f',       
                    'Time Category': False 
                },
                labels={
                    'route_id': 'Route ID',
                    'origin': 'Origin',
                    'destination': 'Destination',
                    'distance_km': 'Distance (kms)'
                },
                texttemplate='%{y:.1f}h'
            ), use_container_width=True)
    # end region

    # region Network Overview
    st.markdown('---')
    st.markdown('### Network Overview')
    
    st.plotly_chart(create_scatter_chart(
        df=route_datasets['distance_vs_del_time'],
        x='distance_km',
        y='avg_del_time',
        title='Network Correlation: Distance vs Delivery Time',
        xaxis_title='Distance (Kms)',
        yaxis_title='Delivery Time (Hrs)',
        hover_data=['route_id']
    ), use_container_width=True)
    
    st.plotly_chart(create_heatmap(
        df=route_datasets['route_volume'],
        x='destination',
        y='origin',
        z='Total Shipments',
        title='Network Density: Route Volume (Origin-Destination)',
        xaxis_title='Destination City',
        yaxis_title='Origin City',
        height=700
    ), use_container_width=True)

    
    st.markdown("##### Full Route Performance Log")
    display_data_table(
        df=route_datasets['route_perf_table'],
        height=600
    )
    # end region