import pandas as pd

def get_shipment_details(df: pd.DataFrame) -> dict:
    shipment_details = {
        'Shipment ID': '-',
        'Status' : '-',
        'Order Date': '-',
        'Delivery Date': '-',
        'Origin': '-',
        'Destination': '-', 
        'Weight': '-',
        'Vehicle Type': '-',
        'Courier': '-',
        'Fuel Cost': '-',
        'Labor Cost': '-',
        'Miscellaneous Cost': '-'
    }
    if df.empty:
        return shipment_details
    
    record = df.iloc[0]

    shipment_details['Shipment ID'] = record.get('shipment_id', '-')
    shipment_details['Status'] = record.get('status', '-')
    shipment_details['Order Date'] = record.get('order_date', '-')
    shipment_details['Delivery Date'] = record.get('delivery_date', '-')
    shipment_details['Origin'] = record.get('origin', '-')
    shipment_details['Destination'] = record.get('destination', '-')
    shipment_details['Weight'] = f"{record.get('weight', '-')} kgs"
    shipment_details['Vehicle Type'] = record.get('vehicle_type', '-')
    
    shipment_details['Fuel Cost'] = record.get('fuel_cost', 0.0)
    shipment_details['Labor Cost'] = record.get('labor_cost', 0.0)
    shipment_details['Miscellaneous Cost'] = record.get('misc_cost', 0.0)

    if pd.notna(record.get('courier_name')):
        shipment_details['Courier'] = f"{record.get('courier_name')} ({record.get('courier_id', '-')})"
    
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