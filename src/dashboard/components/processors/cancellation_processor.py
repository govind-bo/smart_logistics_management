import pandas as pd

# region KPIs
def calculate_cancellation_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates KPI data for the cancellation analysis page.
    """
    metrics = {
        'total_cancelled': 0,
        'cancellation_rate': 0.0,
        'worst_origin': 'N/A',
        'worst_origin_rate': 0.0,
        'worst_courier': 'N/A',
        'worst_courier_rate': 0.0
    }

    if df.empty:
        return metrics

    df['is_cancelled'] = (df['status'].str.lower() == 'cancelled').astype(int)
    
    total_shipments = len(df)
    total_cancelled = df['is_cancelled'].sum()
    
    metrics['total_cancelled'] = total_cancelled
    
    if total_shipments > 0:
        metrics['cancellation_rate'] = (total_cancelled / total_shipments) * 100

    if total_cancelled > 0:
        # Worst Origin (Minimum 3 shipments to be considered)
        origin_grp = df.groupby('origin').agg(
            total=('shipment_id', 'count'),
            cancelled=('is_cancelled', 'sum')
        )
        origin_grp = origin_grp[origin_grp['total'] >= 3]
        if not origin_grp.empty:
            origin_grp['rate'] = (origin_grp['cancelled'] / origin_grp['total']) * 100
            worst_org = origin_grp.sort_values(by='rate', ascending=False).iloc[0]
            metrics['worst_origin'] = worst_org.name
            metrics['worst_origin_rate'] = worst_org['rate']

        # Worst Courier (Minimum 3 shipments to be considered)
        courier_grp = df.groupby('courier_name').agg(
            total=('shipment_id', 'count'),
            cancelled=('is_cancelled', 'sum')
        )
        courier_grp = courier_grp[courier_grp['total'] >= 3]
        if not courier_grp.empty:
            courier_grp['rate'] = (courier_grp['cancelled'] / courier_grp['total']) * 100
            worst_cour = courier_grp.sort_values(by='rate', ascending=False).iloc[0]
            metrics['worst_courier'] = worst_cour.name
            metrics['worst_courier_rate'] = worst_cour['rate']

    return metrics
# end region KPIs

# region Cancellation Datasets
def prepare_cancellation_datasets(df: pd.DataFrame, sort_by: str = 'cancel_rate', is_ascending: bool = False, display_limit: int = 10) -> dict:
    """
    Prepares dataset dictionary for the Cancellation Analytics charts.
    """
    datasets = {
        'trend': None,
        'origin_ranks': None,
        'dest_ranks': None,
        'courier_ranks': None,
        'correlation': None,
        'route_table': None
    }
    
    if df.empty:
        return datasets

    df['is_cancelled'] = (df['status'].str.lower() == 'cancelled').astype(int)
    cancelled_only_df = df[df['is_cancelled'] == 1].copy()

    # ----------------- Freed Data: Trend -----------------
    if not cancelled_only_df.empty:
        cancelled_only_df['month_year'] = pd.to_datetime(cancelled_only_df['order_date']).dt.to_period('M')
        trend_df = cancelled_only_df.groupby('month_year').size().reset_index(name='cancellations')
        trend_df['month_year'] = trend_df['month_year'].astype(str)
        datasets['trend'] = trend_df

    # ----------------- Freed Data: Correlation Scatter -----------------
    scatter_df = cancelled_only_df[['shipment_id', 'distance_km', 'weight', 'route_id']].copy()
    if len(scatter_df) > 300:
        scatter_df = scatter_df.sample(n=300, random_state=42)
    datasets['correlation'] = scatter_df

    # Helper function for calculating rates safely and applying unified sorting
    def get_ranked_rates(group_col: str):
        grp = df.groupby(group_col, as_index=False).agg(
            total=('shipment_id', 'count'),
            cancelled=('is_cancelled', 'sum')
        )
        grp = grp[grp['total'] >= 3].copy()
        
        if grp.empty:
            return pd.DataFrame(columns=[group_col, 'total', 'cancelled', 'cancel_rate'])
            
        grp['cancel_rate'] = (grp['cancelled'] / grp['total']) * 100
        
        # Sort to get the Top N based on UI controls
        top_n = grp.sort_values(sort_by, ascending=is_ascending).head(display_limit)
        
        # Plotly plots bottom-to-top for horizontal bars. To ensure the #1 rank stays at the very top visually, we reverse sort here.
        return top_n.sort_values(sort_by, ascending=not is_ascending)

    # ----------------- Controlled Data: Rankings (All Unified) -----------------
    datasets['origin_ranks'] = get_ranked_rates('origin')
    datasets['dest_ranks'] = get_ranked_rates('destination')
    datasets['courier_ranks'] = get_ranked_rates('courier_name')

    # ----------------- Freed Data: Route Table -----------------
    route_table = df.groupby(['route_id', 'origin', 'destination'], as_index=False).agg(
        Total_Shipments=('shipment_id', 'count'),
        Cancellations=('is_cancelled', 'sum')
    )
    route_table = route_table[route_table['Cancellations'] > 0].copy()
    route_table['Cancellation Rate (%)'] = (route_table['Cancellations'] / route_table['Total_Shipments']) * 100
    route_table['Cancellation Rate (%)'] = route_table['Cancellation Rate (%)'].round(1)
    
    route_table = route_table.sort_values(by='Cancellations', ascending=False)
    route_table.columns = ['Route ID', 'Origin', 'Destination', 'Total Shipments', 'Cancellations', 'Cancel Rate (%)']
    datasets['route_table'] = route_table

    return datasets
# end region Cancellation Datasets