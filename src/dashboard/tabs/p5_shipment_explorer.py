import pandas as pd
import streamlit as st
from src.dashboard.utils import get_data
from src.dashboard.components.processors.explorer_processor import get_shipment_details, \
                                                                    get_shipment_tracking_details, \
                                                                    get_shipment_cost_details

def render_shipment_search_page() ->None:
    '''
    Renders the Shipment Search Page of the dashboard
    '''

    st.title('Shipment Search & Tracking')

    shipment_explorer_filter = {}

    # display search bar
    shipment_id_user_input = st.text_input(
                                label = 'Shipment Search',
                                placeholder = 'Please enter a Shipment ID to search'
                                )
    
    if shipment_id_user_input:
        shipment_explorer_filter['shipment_id'] = shipment_id_user_input

        # region get data for the shipment id passed by user    
        df = get_data('tabs', 'shipment_explorer.sql', params = shipment_explorer_filter)
        
        if df.empty:
            st.warning('No Shipment data for the entered Shipment ID.')
        else:
            shipment_details = get_shipment_details(df)
            shipment_tracking_details = get_shipment_tracking_details(df)
            shipment_cost_details = get_shipment_cost_details(df)

            # display shipment data
            row1 = st.columns([2,3])
            with row1[0]:
                st.markdown('##### Shipment Details')
            with row1[1]:
                st.markdown('##### Tracking details')
            
            row2 = st.columns([2,3])
            with row2[0]:
                st.table(shipment_details)
            with row2[1]:
                st.dataframe(shipment_tracking_details)
            
            st.markdown('---')

            
  
