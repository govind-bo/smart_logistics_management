import streamlit as st

from src.dashboard.utils import get_data
from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import (
    create_bar_chart, 
    create_line_chart, 
    create_scatter_chart,
    display_data_table
)

from src.dashboard.components.processors.cancellation_processor import (
    calculate_cancellation_metrics,
    prepare_cancellation_datasets
)

def render_cancellation_page() -> None:
    """
    Renders the Cancellation Analysis page of the dashboard
    """
    st.title('Cancellation Analysis')

    # region Data Fetching
    filters = render_filters()
    df = get_data('tabs', 'cancellation_analytics.sql', params=filters)

    if df.empty:
        st.warning('No data available for the chosen filters')
        return
    # end region 

    # region KPIs
    summary_metrics = calculate_cancellation_metrics(df)
    st.markdown('### Failure Overview')
    row1 = st.columns([2,2,3,3])

    with row1[0]:
        display_kpi('Total Cancellations', f"{summary_metrics['total_cancelled']:,}")
        
    with row1[1]:
        display_kpi('Cancellation Rate', f"{summary_metrics['cancellation_rate']:.1f}%")
    
    with row1[2]:
        worst_org = summary_metrics['worst_origin']
        org_rate = summary_metrics['worst_origin_rate']
        display_kpi('Highest Failure Origin',
                    str(worst_org),
                    caption=f"Cancel Rate: {org_rate:.1f}%" if worst_org != 'N/A' else None)
        
    with row1[3]:
        worst_cour = summary_metrics['worst_courier']
        cour_rate = summary_metrics['worst_courier_rate']
        display_kpi('Highest Failure Courier',
                    str(worst_cour),
                    caption=f"Cancel Rate: {cour_rate:.1f}%" if worst_cour != 'N/A' else None)
    # end region

    st.markdown('---')
    
    # region Macro Trends
    st.markdown('### Cancellation Trend')
    # Generate initial fallback dataset for the top trendline
    datasets_macro = prepare_cancellation_datasets(df, display_limit=10)
    
    if datasets_macro['trend'] is not None and not datasets_macro['trend'].empty:
        st.plotly_chart(create_line_chart(
            df=datasets_macro['trend'],
            x='month_year',
            y='cancellations',
            title='Monthly Cancellation Volume',
            xaxis_title='Month',
            yaxis_title='Total Cancellations'
        ), use_container_width=True)
    else:
        st.info("No cancellations recorded in this time period.")
    # end region

    # region Failure Rankings
    st.markdown('---')
    st.markdown('### Failure Rankings')

    available_entities = df['origin'].nunique()
    if available_entities == 0: 
        available_entities = 1

    charts_col, sort_controls_col = st.columns([3, 1])

    # --------------- Interactive Controls ---------------
    with sort_controls_col:
        st.markdown('##### Chart Controls')
        st.caption('Applies to Failure Rankings')
        
        available_entities = df['route_id'].nunique()

        # Only render the slider if there are at least 2 routes to slide between
        if available_entities > 1:
            display_limit = st.slider(
                'Number of Routes to Display', 
                min_value=1, 
                max_value=available_entities, 
                value=min(available_entities, 15)
            )
        else:
            # Fallback for 0 or 1 route
            display_limit = available_entities
            if available_entities == 1:
                st.caption("Only 1 route available for current filters.")
        
        sort_choice = st.radio(
            'Sort by:',
            ['Highest', 'Lowest'],
            index=0,
            horizontal=True
        )
        is_ascending = True if sort_choice == 'Lowest' else False

        sort_metric_dict = {
            'cancel_rate': 'Cancellation Rate',
            'cancelled': 'Total Cancellations'
        }
        
        sort_by = st.selectbox(
            'Sort by Metric',
            options=['cancel_rate', 'cancelled'],
            format_func=lambda x: sort_metric_dict[x],
            index=0
        )

    datasets = prepare_cancellation_datasets(df, sort_by=sort_by, is_ascending=is_ascending, display_limit=display_limit)

    with charts_col:
        rowA_col1, rowA_col2 = st.columns(2)
        
        with rowA_col1:
            st.plotly_chart(create_bar_chart(
                df=datasets['origin_ranks'],
                x=sort_by,
                y='origin',
                orientation='h',
                title='Highest Failure Origins',
                xaxis_title='Cancel Rate (%)' if sort_by == 'cancel_rate' else 'Total Cancellations',
                yaxis_title='Origin City',
                texttemplate='%{x:.1f}%' if sort_by == 'cancel_rate' else '%{x:.0f}',
                hover_data={'cancelled': True, 'total': True}
            ), use_container_width=True)

        with rowA_col2:
            st.plotly_chart(create_bar_chart(
                df=datasets['dest_ranks'],
                x=sort_by,
                y='destination',
                orientation='h',
                title='Highest Failure Destinations',
                xaxis_title='Cancel Rate (%)' if sort_by == 'cancel_rate' else 'Total Cancellations',
                yaxis_title='Destination City',
                texttemplate='%{x:.1f}%' if sort_by == 'cancel_rate' else '%{x:.0f}',
                hover_data={'cancelled': True, 'total': True}
            ), use_container_width=True)
    # end region

    # region Failure Correlation & Route Logs
    st.markdown('---')
    st.markdown('### Operational Deep Dive')
    
    # Place Courier Chart and Scatter Plot side-by-side to save vertical space
    rowB_col1, rowB_col2 = st.columns(2)

    with rowB_col1:
        st.plotly_chart(create_bar_chart(
            df=datasets['courier_ranks'],
            x=sort_by,
            y='courier_name',
            orientation='h',
            title='Highest Failure Couriers',
            xaxis_title='Cancel Rate (%)' if sort_by == 'cancel_rate' else 'Total Cancellations',
            yaxis_title='Courier Name',
            texttemplate='%{x:.1f}%' if sort_by == 'cancel_rate' else '%{x:.0f}',
            hover_data={'cancelled': True, 'total': True}
        ), use_container_width=True)

    with rowB_col2:
        st.plotly_chart(create_scatter_chart(
            df=datasets['correlation'],
            x='distance_km',
            y='weight',
            title='Cancellations by Distance & Weight',
            xaxis_title='Route Distance (Kms)',
            yaxis_title='Shipment Weight (Kgs)',
            opacity=0.6,
            hover_data=['shipment_id', 'route_id']
        ), use_container_width=True)

    st.markdown("##### Most Cancelled Routes Directory")
    display_data_table(
        df=datasets['route_table'],
        height=400
    )
    # end region