import pandas as pd

def get_shipment_details(df: pd.DataFrame) -> dict:
    shipment_details = {
        'Shipment ID': df.get('shipment_id', '-')[0],
        'Status' : df.get('status', '-')[0],
        'Order Date': df.get('order_date', '-')[0],
        'Delivery Date': df.get('delivery_date', '-')[0],
        'Origin': df.get('origin', '-')[0],
        'Destination': df.get('destination', '-')[0], 
        'Weight': f'{df.get('weight', '-')[0]} kgs',
        'Vehicle Type': df.get('vehicle_type', '-')[0],
        'Courier': f"{df.get('courier_name','-')[0]} ({df.get('courier_id','-')[0]})" \
                                        if df.get('courier_name','-')[0] != '-' else '-',
        'Fuel Cost': df.get('fuel_cost', '-')[0],
        'Labor Cost': df.get('labor_cost', '-')[0],
        'Miscellaneous Cost': df.get('misc_cost', '-')[0]
               
            }
    #shipment_details['Courier'] = f"{df.get('courier_name','-')[0]} ({df.get('courier_id','-')[0]})" \
     #                                   if df.get('courier_name','-')[0] != '-' else '-' 

    return shipment_details

def get_shipment_tracking_details(df: pd.DataFrame ) -> pd.DataFrame:
    tracking_df = df[['tracking_id', 'tracking_status', 'timestamp']]
    tracking_df['timestamp'] = pd.to_datetime(tracking_df['timestamp'], errors = 'coerce')
    tracking_df['Date'] = df['timestamp'].dt.date
    tracking_df['Time'] = df['timestamp'].dt.time
    tracking_df = tracking_df.drop(columns = ['timestamp'])
    tracking_df.columns = ['Tracking ID', 'Tracking Status', 'Date', 'Time']
    tracking_df = tracking_df.sort_values(by = ['Date', 'Time'])

    return tracking_df

def get_shipment_cost_details(df) -> dict:
    shipment_cost_details = {
        'Fuel Cost': df.get('fuel_cost', '-')[0],
        'Labor Cost': df.get('labor_cost', '-')[0],
        'Miscellaneous Cost': df.get('misc_cost', '-')[0]
    }
    return shipment_cost_details