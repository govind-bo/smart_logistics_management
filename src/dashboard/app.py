from pathlib import Path
import sys
import streamlit as st

# setup path variables to import our modules correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.dashboard.tabs.overview import render_overview_page
from src.dashboard.tabs.route_performance import render_route_performance_page
from src.dashboard.tabs.cost_analytics import render_cost_analytics_page
from src.dashboard.tabs.shipment_explorer import render_shipment_search_page
from src.dashboard.tabs.courier_performance import render_courier_performance_page
from src.dashboard.tabs.cancellation_analytics import render_cancellation_page
from src.dashboard.tabs.warehouse_utilization import render_warehouse_page

st.set_page_config(page_title="Smart Logistics Analytics", layout="wide")


# region - Side bar - navigation
st.sidebar.markdown('### Navigation')
pages = ['Operations Overview', 
         'Route Performance',
         'Courier Performance', 
         'Cost Analytics', 
         'Warehouse Utilization',
         'Cancellation Analytics',
         'Shipment Explorer']
page_selection = st.sidebar.pills(
    'Go to:',
    options = pages,
    default = 'Operations Overview',
    label_visibility = 'collapsed',
    width = 250
)
st.sidebar.divider()

# endregion


# region - page orchestration

if page_selection == 'Operations Overview':
    render_overview_page()
elif page_selection == 'Courier Performance':
    render_courier_performance_page()
elif page_selection == 'Cancellation Analytics':
    render_cancellation_page()
elif page_selection == 'Route Performance':
    render_route_performance_page()
elif page_selection == 'Warehouse Utilization':
    render_warehouse_page()
elif page_selection == 'Cost Analytics':
    render_cost_analytics_page()
elif page_selection == 'Shipment Explorer':
    render_shipment_search_page()


# endregion
