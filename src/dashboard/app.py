from pathlib import Path
import sys
import streamlit as st

# setup path variables to import our modules correctly
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.dashboard.tabs.p1_overview import render_overview_page
from src.dashboard.tabs.p4_cost_analytics import render_cost_analytics_page
from src.dashboard.tabs.p5_shipment_explorer import render_shipment_search_page

st.set_page_config(page_title="Smart Logistics Analytics", layout="wide")


# region - Side bar - navigation
st.sidebar.markdown('### Navigation')
pages = ['Operations Overview', 'Courier Performance', 'Cost Analytics', 'Warehouse Utilization', 'Shipment Explorer']
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
    pass
elif page_selection == 'Warehouse Utilization':
    pass
elif page_selection == 'Cost Analytics':
    render_cost_analytics_page()
elif page_selection == 'Shipment Explorer':
    render_shipment_search_page()


# endregion
