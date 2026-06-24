# src/dashboard/components/processors/courier_perf_processor.py

import pandas as pd

# region KPIs
def calculate_courier_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates KPI data for the courier performance page.
    """
    metrics = {
        'total_couriers': 0,
        'avg_courier_rating': 0.0,
        'best_courier': 'N/A',
        'best_courier_rating': 0.0,
        'best_courier_shipments': 0,
        'best_courier_volume': 0.0,
        'highest_volume_courier': 'N/A',
        'highest_volume': 0,
        'highest_volume_rating': 0.0,
        'highest_volume_volume': 0.0
    }

    if df.empty:
        return metrics

    couriers_df = df[['courier_id', 'courier_name', 'courier_rating']].drop_duplicates()
    metrics['total_couriers'] = couriers_df['courier_id'].nunique()
    metrics['avg_courier_rating'] = couriers_df['courier_rating'].mean()

    perf_df = df.groupby(['courier_id', 'courier_name', 'courier_rating'], as_index=False).agg(
        total_shipments=('shipment_id', 'count'),
        total_weight=('weight', 'sum')
    )
    
    perf_df['volume'] = perf_df['total_shipments'] * perf_df['total_weight']

    if not perf_df.empty:
        best_rated_row = perf_df.sort_values(by=['courier_rating', 'total_shipments'], ascending=[False, False]).iloc[0]
        metrics['best_courier'] = best_rated_row['courier_name']
        metrics['best_courier_rating'] = best_rated_row['courier_rating']
        metrics['best_courier_shipments'] = best_rated_row['total_shipments']
        metrics['best_courier_volume'] = best_rated_row['volume']

        high_vol_row = perf_df.sort_values(by='total_shipments', ascending=False).iloc[0]
        metrics['highest_volume_courier'] = high_vol_row['courier_name']
        metrics['highest_volume'] = high_vol_row['total_shipments']
        metrics['highest_volume_rating'] = high_vol_row['courier_rating']
        metrics['highest_volume_volume'] = high_vol_row['volume']

    return metrics
# end region KPIs

# region Courier Datasets
def prepare_courier_datasets(df: pd.DataFrame, sort_by: str = 'total_shipments', is_ascending: bool = False, display_limit: int = 15) -> dict:
    """
    Prepares dataset dictionary for the Courier Analytics charts.
    """
    datasets = {
        'shipments_handled': None,
        'success_rate_chart': None,
        'rating_vs_success': None,
        'vehicle_distribution': None,
        'courier_leaderboard': None
    }
    
    if df.empty:
        return datasets

    df['is_success'] = (df['status'].str.lower() == 'delivered').astype(int)

    courier_group = df.groupby(['courier_id', 'courier_name', 'courier_rating', 'vehicle_type'], as_index=False).agg(
        total_shipments=('shipment_id', 'count'),
        successful_deliveries=('is_success', 'sum'),
        total_weight=('weight', 'sum')
    )
    
    courier_group['success_rate'] = (courier_group['successful_deliveries'] / courier_group['total_shipments']) * 100
    courier_group['volume'] = courier_group['total_shipments'] * courier_group['total_weight']

    controlled_df = courier_group.sort_values(by=sort_by, ascending=is_ascending).head(display_limit)

    # ----------------- Controlled Data -----------------
    datasets['shipments_handled'] = controlled_df[['courier_id', 'courier_name', 'total_shipments']].copy()
    datasets['success_rate_chart'] = controlled_df[['courier_id', 'courier_name', 'success_rate']].copy()

    # ----------------- Freed Data -----------------
    scatter_df = courier_group[['courier_id', 'courier_name', 'courier_rating', 'success_rate', 'total_shipments']].copy()
    if len(scatter_df) > 300:
        scatter_df = scatter_df.sample(n=300, random_state=42)
    datasets['rating_vs_success'] = scatter_df

    datasets['vehicle_distribution'] = courier_group.groupby('vehicle_type', as_index=False).agg(
        volume=('volume', 'sum')
    )

    leaderboard = courier_group[['courier_id', 'courier_name', 'vehicle_type', 'courier_rating', 'total_shipments', 'volume', 'success_rate']].copy()
    
    leaderboard.columns = [
        'Courier ID', 'Courier Name', 'Vehicle Type', 'Rating', 'Total Shipments', 'Volume', 'Delivery Success Rate (%)'
    ]
    
    leaderboard['Rating'] = leaderboard['Rating'].round(2)
    leaderboard['Volume'] = leaderboard['Volume'].round(1)
    leaderboard['Delivery Success Rate (%)'] = leaderboard['Delivery Success Rate (%)'].round(1)
    
    leaderboard = leaderboard.sort_values(by=['Rating', 'Total Shipments'], ascending=[False, False])
    
    datasets['courier_leaderboard'] = leaderboard

    return datasets
# end region Courier Datasets