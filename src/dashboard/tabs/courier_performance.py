# src/dashboard/pages/p_courier_performance.py

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

from src.dashboard.components.processors.courier_processor import (
    calculate_courier_metrics,
    prepare_courier_datasets
)

def render_courier_performance_page() -> None:
    """
    Renders the Courier Performance page of the dashboard
    """
    st.title('Courier Performance')

    # region Data Fetching
    filters = render_filters()
    df = get_data('tabs', 'courier_performance.sql', params=filters)

    if df.empty:
        st.warning('No Courier data available for the chosen filters')
        return
    # end region 

    # region KPIs
    summary_courier_metrics = calculate_courier_metrics(df)
    st.markdown('### Workforce KPIs')
    row1 = st.columns(4)

    # kpi 1 - Total Couriers
    with row1[0]:
        total_couriers = summary_courier_metrics['total_couriers']
        display_kpi('Total Couriers', f"{total_couriers:,}")
        
    # kpi 2 - Avg Courier Rating
    with row1[1]:
        avg_rating = summary_courier_metrics['avg_courier_rating']
        display_kpi('Avg Courier Rating', f"{avg_rating:.1f} / 5.0")
    
    # kpi 3 - Best Rated Courier
    with row1[2]:
        best_courier = summary_courier_metrics['best_courier']
        best_rating = summary_courier_metrics['best_courier_rating']
        best_shipments = summary_courier_metrics['best_courier_shipments']
        best_volume = summary_courier_metrics['best_courier_volume']
        display_kpi('Best Rated Courier',
                    str(best_courier),
                    caption=f"Rating: {best_rating:.1f} | Shipments: {best_shipments:,} | Vol: {best_volume:,.0f}")
        
    # kpi 4 - Highest Volume Courier
    with row1[3]:
        high_vol_courier = summary_courier_metrics['highest_volume_courier']
        high_vol_rating = summary_courier_metrics['highest_volume_rating']
        high_vol = summary_courier_metrics['highest_volume']
        high_vol_volume = summary_courier_metrics['highest_volume_volume']
        display_kpi('Highest Volume Courier',
                    str(high_vol_courier),
                    caption=f"Rating: {high_vol_rating:.1f} | Shipments: {high_vol:,} | Vol: {high_vol_volume:,.0f}")
    # end region

    # region Courier Rankings (Controlled)
    st.markdown('---')
    st.markdown('### Courier Rankings')

    available_couriers = df['courier_id'].nunique()
    charts_col, sort_controls_col = st.columns([3, 1])

    # --------------- Interactive Controls ---------------
    with sort_controls_col:
        st.markdown('##### Chart Controls')
        st.caption('Applies to Courier Rankings')
        
        available_couriers = df['courier_id'].nunique()

        if available_couriers > 1:
            display_limit = st.slider(
                'Number of Couriers to Display', 
                min_value=1, 
                max_value=available_couriers, 
                value=min(available_couriers, 15)
            )
        else:
            display_limit = available_couriers
            if available_couriers == 1:
                st.caption("Only 1 courier available for current filters.")
        
        sort_choice = st.radio(
            'Sort by:',
            ['Highest', 'Lowest'],
            index=0,
            horizontal=True
        )
        is_ascending = True if sort_choice == 'Lowest' else False

        sort_metric_dict = {
            'total_shipments': 'Total Shipments',
            'success_rate': 'Delivery Success Rate',
            'courier_rating': 'Courier Rating'
        }
        
        sort_by = st.selectbox(
            'Sort by Metric',
            options=['total_shipments', 'success_rate', 'courier_rating'],
            format_func=lambda x: sort_metric_dict[x],
            index=0
        )

    courier_datasets = prepare_courier_datasets(df, sort_by=sort_by, is_ascending=is_ascending, display_limit=display_limit)
    
    if courier_datasets['shipments_handled'] is not None:
        
        with charts_col:
            eff_col1, eff_col2 = st.columns(2)
            
            with eff_col1:
                st.plotly_chart(create_bar_chart(
                    df=courier_datasets['shipments_handled'],
                    x='courier_name',
                    y='total_shipments',
                    title=f"Shipments Handled",
                    xaxis_title='Courier Name',
                    yaxis_title='Total Shipments',
                    hover_data={'courier_id': True, 'courier_name': True, 'total_shipments': True},
                    labels={'courier_name': 'Courier', 'total_shipments': 'Shipments'},
                    texttemplate='%{y:.3s}'
                ), use_container_width=True)

            with eff_col2:
                st.plotly_chart(create_bar_chart(
                    df=courier_datasets['success_rate_chart'],
                    x='courier_name',
                    y='success_rate',
                    title=f"Delivery Success Rate",
                    xaxis_title='Courier Name',
                    yaxis_title='Success Rate (%)',
                    hover_data={'courier_id': True, 'courier_name': True, 'success_rate': ':.1f%'},
                    labels={'courier_name': 'Courier', 'success_rate': 'Success Rate'},
                    texttemplate='%{y:.1f}%'
                ), use_container_width=True)
    # end region

    # region Network Overview (Freed Data)
    st.markdown('---')
    st.markdown('### Workforce Overview')
    
    row3 = st.columns(2)
    
    with row3[0]:
        st.plotly_chart(create_scatter_chart(
            df=courier_datasets['rating_vs_success'],
            x='courier_rating',
            y='success_rate',
            size='total_shipments',
            title='Courier Rating vs Delivery Success Rate',
            xaxis_title='Courier Rating (Max 5.0)',
            yaxis_title='Delivery Success Rate (%)',
            hover_data=['courier_name', 'courier_id', 'total_shipments']
        ), use_container_width=True)
        
    with row3[1]:
        st.plotly_chart(create_pie_chart(
            df=courier_datasets['vehicle_distribution'],
            names='vehicle_type',
            values='volume',
            title='Volume Distribution by Vehicle Type',
            hole=0.4,
            texttemplate="%{label}<br>%{value:.2s} (%{percent:.1%})"
        ), use_container_width=True)

    st.markdown("##### Courier Leaderboard")
    display_data_table(
        df=courier_datasets['courier_leaderboard'],
        height=500
    )
    # end region