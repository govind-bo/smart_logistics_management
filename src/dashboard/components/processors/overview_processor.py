import pandas as pd

def calculate_overview_metrics(df: pd.DataFrame) -> dict:
    '''
    Calculates KPI values from raw shipment data.
    '''
    metrics = {
        "total_shipments": 0, "delivered_pct": 0.0, "in_transit_pct": 0.0,
        "cancelled_pct": 0.0, "avg_duration": 0.0, "total_cost": 0.0,
        "active_routes": 0, "total_couriers": 0
    }
    
    if df.empty:
        return metrics

    # Basic counts
    metrics["total_shipments"] = len(df)
    
    # Status percentages
    status_counts = df['status'].value_counts()
    total = len(df)                     # USE total = metrics["total_shipments"] - TO IMPROVE SPEED ?
    metrics["delivered_pct"] = (status_counts.get('Delivered', 0) / total * 100)
    metrics["in_transit_pct"] = (status_counts.get('In Transit', 0) / total * 100)
    metrics["cancelled_pct"] = (status_counts.get('Cancelled', 0) / total * 100)
    
    # Average duration
    df['delivery_date'] = pd.to_datetime(df['delivery_date'], errors='coerce')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    delivered = df[df['status'] == 'Delivered']
    if not delivered.empty:
        metrics["avg_duration"] = (delivered['delivery_date'] - delivered['order_date']).dt.days.mean()
    
    metrics["total_cost"] = df['total_cost'].sum()
    metrics["active_routes"] = df['route_id'].nunique()
    metrics["total_couriers"] = df['courier_id'].nunique()
    
    return metrics

def prepare_overview_datasets(df: pd.DataFrame, granularity: str = "Month") -> dict:
    '''
    Prepares datasets for charts using Month or Day granularity.
    '''
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    
    # Create time period for grouping ------------------------------------------
    if granularity == "Day":
        df['time_period'] = df['order_date'].dt.strftime('%Y-%m-%d')
    else:
        df['time_period'] = df['order_date'].dt.to_period('M').astype(str)

    # Prepare datasets ---------------------------------------------------------
    status_mix = df['status'].value_counts().reset_index()
    status_mix.columns = ['status', 'shipment_count']
    
    timeline_trend = df.groupby('time_period').agg(
        timeline_shipments=('shipment_id', 'count'),
        timeline_costs=('total_cost', 'sum')
    ).reset_index()
    
    wh_capacity = df.groupby('warehouse_city')['warehouse_capacity'].first().reset_index()
    wh_traffic = df.groupby('warehouse_city')['shipment_id'].count().reset_index()
    wh_traffic.columns = ['warehouse_city', 'shipment_count']
    
    return {
        "status_mix": status_mix,
        "timeline_trend": timeline_trend,
        "wh_capacity": wh_capacity,
        "wh_traffic": wh_traffic
    }