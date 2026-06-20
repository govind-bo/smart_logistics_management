import streamlit as st

from src.dashboard.utils import get_data
from src.dashboard.components.filters import render_filters
from src.dashboard.components.kpi_cards import display_kpi
from src.dashboard.components.charts import (
    create_bar_chart, 
    create_line_chart, 
    create_pie_chart, 
    create_scatter_chart
)
from src.dashboard.components.processors.cost_processor import (
    calculate_cost_metrics, 
    prepare_cost_datasets
)

def render_cost_analytics_page() -> None:
    """
    Renders the Cost Analytics page of the dashboard
    """
    st.title('Cost Analytics')

    # region Data Fetching
    filters = render_filters()
    df = get_data('tabs', 'cost_analytics.sql', params=filters)

    if df.empty:
        st.warning("No shipment data available for the chosen filters.")
        return
        
    summary_cost_metrics = calculate_cost_metrics(df)
    # endregion

    # region KPIs
    st.markdown('### Cost KPIs')
    row1 = st.columns(4)

    with row1[0]:
        total_cost = summary_cost_metrics['total_operational_cost']
        cost_str = f"${total_cost:,.2f}" if total_cost < 1000 else f"${total_cost:,.0f}"
        display_kpi('Total Operational Cost', cost_str)
        
    with row1[1]:
        avg_cost = summary_cost_metrics['avg_cost_per_shipment']
        display_kpi('Avg Cost Per Shipment', f"${avg_cost:,.2f}")
        
    with row1[2]:
        max_cost = summary_cost_metrics['highest_cost_val']
        shipment_id = summary_cost_metrics['highest_cost_shipment_id']
        display_kpi(label='Highest Cost Shipment', value=f"${max_cost:,.2f}", caption=shipment_id)
        
    with row1[3]:
        route_id = summary_cost_metrics['highest_cost_route_id']
        origin = summary_cost_metrics['highest_cost_origin']
        dest = summary_cost_metrics['highest_cost_destination']
        display_kpi(label='Highest Cost Route', value=route_id, caption=f"{origin} -> {dest}")
    # endregion

    # region Route Performance
    st.markdown('---')
    st.markdown('### Route Performance Hub')
    
    # Interactive controls governing all 3 route charts
    #slider_row = st.columns(1)
        
    available_routes = df['route_id'].nunique()
#    with slider_row[0]:




    total_cost_chart, sort_controls_col = st.columns([3, 1])
    with sort_controls_col:

        display_limit = st.slider(
            'Number of Routes to Display', 
            min_value=min(1, available_routes), 
            max_value=available_routes, 
            value=min(available_routes, 15)
        )
        # Highest or lowest sort
        sort_choice = st.radio(
            'Sort Routes by:', 
            ['Highest Cost', 'Lowest Cost'], 
            index=0, 
            horizontal=True
        )
        is_ascending = True if sort_choice == 'Lowest Cost' else False

        sort_metric_dict = {'total_cost':'Total Cost',
                            'cost_per_km': 'Cost per Km',
                            'cost_per_kg':'Cost per Kg'
                            }
        # sort by field
        sort_by = st.selectbox(
            'Sort by Metric',
            options = ['total_cost', 'cost_per_km', 'cost_per_kg'],
            format_func = lambda x:sort_metric_dict[x],
            index = 0
        )

    # Generate datasets using the user's inputs
    cost_datasets = prepare_cost_datasets(df, sort_by=sort_by, is_ascending=is_ascending, display_limit=display_limit)

    with total_cost_chart:
        # 1. Stacked Route Cost Bar Chart
        st.plotly_chart(create_bar_chart(
            df=cost_datasets['route_costs'], 
            x='route_id', 
            y='category_cost',
            color='cost_category',
            title=f"Total Cost Breakdown ({'Lowest' if is_ascending else 'Top'} {display_limit})",
            xaxis_title='Route ID',
            yaxis_title='Total Cost ($)',
            hover_data={
                'route_id': False, 
                'cost_category': True,
                'category_cost': ':$,.0f', 
                'total_cost': ':$,.0f',
                'origin': True, 
                'destination': True,
                'distance_km': True
            },
            labels={
                'total_cost': 'Total Cost',
                'category_cost': 'Cost', 
                'origin': 'Origin', 
                'destination': 'Destination',
                'distance_km': 'Distance (kms)', 
                'cost_category': 'Cost Type'
            },
            texttemplate='%{y:.3s}'
        ), use_container_width=True)

    # 2 & 3. Side-by-Side Efficiency Charts
    eff_col1, eff_col2 = st.columns(2)
    with eff_col1:
        st.plotly_chart(create_bar_chart(
            df=cost_datasets['route_master'], 
            x='route_id', 
            y='cost_per_kg',
            title='Cost Efficiency (per Kg)', 
            xaxis_title='Route ID', 
            yaxis_title='Cost per Kg ($)',
            texttemplate='%{y:$.2f}'
        ), use_container_width=True)
        
    with eff_col2:
        st.plotly_chart(create_bar_chart(
            df=cost_datasets['route_master'], 
            x='route_id', 
            y='cost_per_km',
            title='Cost Efficiency (per Km)', 
            xaxis_title='Route ID', 
            yaxis_title='Cost per Km ($)',
            texttemplate='%{y:$.2f}'
        ), use_container_width=True)
    # endregion

    # region Mix & Trends
    st.markdown('---') 
    row3 = st.columns([3,2])
    
    with row3[0]:
        st.markdown('### Cost Trend')
        st.plotly_chart(create_line_chart(
            df=cost_datasets['cost_trend'], 
            x='order_date', 
            y='total_cost',
            title='Monthly Operational Cost', 
            xaxis_title='Month', 
            yaxis_title='Total Cost ($)'
        ), use_container_width=True)

    with row3[1]:
        st.markdown('### Operational Cost Mix')
        st.plotly_chart(create_pie_chart(
            df=cost_datasets['cost_mix'],
            names='Cost Category',
            values='Total Amount',
            title='Cost Mix Breakdown',
            hole=0.4,
            texttemplate="%{value:$.2s} (%{percent:.1%})"
        ), use_container_width=True)
    # endregion

    # region Cost Distribution Analysis
    st.markdown('---')
    st.markdown('### Cost Distribution Analysis')
    st.plotly_chart(create_scatter_chart(
        df=cost_datasets['cost_scaling'],
        x='weight',
        y='total_cost',
        title='Cost Distribution by Weight and Distance',
        xaxis_title='Weight (kg)',
        yaxis_title='Cost ($)',
        size='distance_km',
        opacity=0.4,
        size_max=12,
        showlegend=True
    ), use_container_width=True)
    # endregion

    # region Cost Explorer
    st.markdown('---')
    st.markdown('### Cost Explorer')
    st.caption("Click a column header to sort. Click inside the table and press **Ctrl+F / Cmd+F** to search.")

    max_total_cost = float(cost_datasets['high_cost_shipments']['total_cost'].max())

    st.dataframe(
        cost_datasets['high_cost_shipments'],
        use_container_width=True,
        hide_index=True,
        height=350,
        column_config={
            "shipment_id": st.column_config.TextColumn("Shipment ID"),
            "route_id": st.column_config.TextColumn("Route ID"),
            "weight": st.column_config.NumberColumn("Weight (kg)", format="%.1f kg"),
            "fuel_cost": st.column_config.NumberColumn("Fuel Cost", format="$ %.2f"),
            "labor_cost": st.column_config.NumberColumn("Labor Cost", format="$ %.2f"),
            "misc_cost": st.column_config.NumberColumn("Misc Cost", format="$ %.2f"),
            "total_cost": st.column_config.ProgressColumn(
                "Total Cost",
                help="Combined total operational cost",
                format="$ %.2f",
                min_value=0,
                max_value=max_total_cost
            )
        }
    )
    # endregion