import pandas as pd

def process_warehouse_data(df: pd.DataFrame) -> pd.DataFrame:
    orig_df = df[df['orig_wh_id'].notnull()][
        ['orig_wh_id', 'orig_wh_city', 'orig_capacity', 'shipment_id', 'vehicle_type', 'weight']
    ].copy()
    orig_df.columns = ['warehouse_id', 'city', 'capacity', 'shipment_id', 'vehicle_type', 'weight']

    dest_df = df[df['dest_wh_id'].notnull()][
        ['dest_wh_id', 'dest_wh_city', 'dest_capacity', 'shipment_id', 'vehicle_type', 'weight']
    ].copy()
    dest_df.columns = ['warehouse_id', 'city', 'capacity', 'shipment_id', 'vehicle_type', 'weight']

    return pd.concat([orig_df, dest_df], ignore_index=True)

# region KPIs
def calculate_warehouse_metrics(df: pd.DataFrame) -> dict:
    metrics = {
        'total_warehouses': 0,
        'total_capacity': 0,
        'highest_activity_hub': 'N/A',
        'highest_activity_count': 0,
        'most_underutilized_hub': 'N/A',
        'lowest_utilization_ratio': 0.0
    }

    if df.empty:
        return metrics

    combined_df = process_warehouse_data(df)
    if combined_df.empty:
        return metrics

    unique_wh = combined_df[['warehouse_id', 'city', 'capacity']].drop_duplicates()
    metrics['total_warehouses'] = unique_wh['warehouse_id'].nunique()
    metrics['total_capacity'] = unique_wh['capacity'].sum()

    wh_activity = combined_df.groupby(['warehouse_id', 'city', 'capacity'], as_index=False).agg(
        activity_count=('shipment_id', 'count')
    )
    
    wh_activity['utilization_ratio'] = (wh_activity['activity_count'] / wh_activity['capacity'].replace(0, 1)) * 100

    if not wh_activity.empty:
        high_act = wh_activity.sort_values(by='activity_count', ascending=False).iloc[0]
        metrics['highest_activity_hub'] = high_act['city']
        metrics['highest_activity_count'] = high_act['activity_count']

        under_act = wh_activity.sort_values(by='utilization_ratio', ascending=True).iloc[0]
        metrics['most_underutilized_hub'] = under_act['city']
        metrics['lowest_utilization_ratio'] = under_act['utilization_ratio']

    return metrics
# end region KPIs

# region Warehouse Datasets
def prepare_warehouse_datasets(df: pd.DataFrame, sort_by: str = 'capacity', is_ascending: bool = False, display_limit: int = 10) -> dict:
    datasets = {
        'capacity_bar': None,
        'activity_bar': None,
        'correlation': None,
        'vehicle_mix': None,
        'network_table': None
    }

    if df.empty:
        return datasets

    combined_df = process_warehouse_data(df)
    if combined_df.empty:
        return datasets

    wh_group = combined_df.groupby(['warehouse_id', 'city', 'capacity'], as_index=False).agg(
        activity_count=('shipment_id', 'count'),
        total_volume=('weight', 'sum')
    )
    wh_group['utilization_ratio'] = (wh_group['activity_count'] / wh_group['capacity'].replace(0, 1)) * 100

    # ----------------- Controlled Data (Tied to UI Slider) -----------------
    controlled_df = wh_group.sort_values(by=sort_by, ascending=is_ascending).head(display_limit)
    # Reverse sort so Plotly renders the #1 rank at the very top of the horizontal chart
    controlled_df = controlled_df.sort_values(by=sort_by, ascending=not is_ascending)

    datasets['capacity_bar'] = controlled_df[['warehouse_id', 'city', 'capacity']].copy()
    datasets['activity_bar'] = controlled_df[['warehouse_id', 'city', 'activity_count']].copy()

    # ----------------- Freed Data -----------------
    datasets['correlation'] = wh_group.copy()

    datasets['vehicle_mix'] = combined_df.groupby('vehicle_type', as_index=False).agg(
        activity_count=('shipment_id', 'count')
    )

    table_df = wh_group[['warehouse_id', 'city', 'capacity', 'activity_count', 'utilization_ratio']].copy()
    table_df.columns = ['Warehouse ID', 'City', 'Capacity', 'Shipment Activity', 'Utilization Ratio (%)']
    
    def assess_risk(ratio):
        if ratio > 80: return 'High (Bottleneck)'
        elif ratio < 20: return 'High (Underutilized)'
        else: return 'Low (Optimal)'
        
    table_df['Utilization Risk'] = table_df['Utilization Ratio (%)'].apply(assess_risk)
    table_df['Utilization Ratio (%)'] = table_df['Utilization Ratio (%)'].round(2)
    
    datasets['network_table'] = table_df.sort_values(by='Shipment Activity', ascending=False)

    return datasets
# end region Warehouse Datasets