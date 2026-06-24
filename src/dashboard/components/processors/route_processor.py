# src/dashboard/components/processors/route_processor.py

import pandas as pd

# region KPIs
def calculate_route_performance_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates KPI data for route performance page
    """
    metrics = {
        'avg_delivery_time': 0, 
        'fastest_route': '', 'fastest_origin': '', 'fastest_destination': '',
        'slowest_route': '', 'slowest_origin': '', 'slowest_destination': '', 
        'consistently_delayed_routes': 0, 'total_routes' : 0
    }

    if df.empty:
        return metrics
    
    metrics['avg_delivery_time'] = df['actual_time_hrs'].mean()

    df_route_grp = df.groupby(['route_id', 'origin', 'destination', 'distance_km'], as_index=False).agg(
        expected_time=('expected_time_hrs', 'mean'),
        avg_actual_time=('actual_time_hrs', 'mean')
    )
    
    safe_time = df_route_grp['avg_actual_time'].replace(0, 0.01)
    df_route_grp['speed'] = df_route_grp['distance_km'] / safe_time

    # --- calculate speed for fastest and slowest route ---
    if not df_route_grp.empty:
        fastest_row = df_route_grp['speed'].idxmax()
        metrics['fastest_route'] = df_route_grp['route_id'].iloc[fastest_row]
        metrics['fastest_origin'] = df_route_grp['origin'].iloc[fastest_row]
        metrics['fastest_destination'] = df_route_grp['destination'].iloc[fastest_row]

        slowest_row = df_route_grp['speed'].idxmin()
        metrics['slowest_route'] = df_route_grp['route_id'].iloc[slowest_row]
        metrics['slowest_origin'] = df_route_grp['origin'].iloc[slowest_row]
        metrics['slowest_destination'] = df_route_grp['destination'].iloc[slowest_row]

    # --- calculate consistently delayed routes ---
    delay_hrs = df['actual_time_hrs'] - df['expected_time_hrs']
    # mark shipments delayed by over 30% time as delayed
    df['is_delayed'] = (delay_hrs > (0.3 * df['expected_time_hrs'])).astype(int)      
    
    # group to get delay rate and total volume
    route_delays = df.groupby('route_id', as_index=False).agg(
        delay_rate=('is_delayed', 'mean'),
        total_shipments=('is_delayed', 'count')
    )
    
    # mark routes having atleast 3 shipments and with >20% delayed shipments as consistently delayed routes
    consistently_delayed = route_delays[
        (route_delays['delay_rate'] > 0.20) & 
        (route_delays['total_shipments'] >= 3)
    ]
    metrics['consistently_delayed_routes'] = len(consistently_delayed)
    metrics['total_routes'] = df['route_id'].nunique()

    return metrics
# end region KPIs

# region Route Datasets
def prepare_route_datasets(df: pd.DataFrame, sort_by: str = 'volume', is_ascending: bool = False, display_limit: int = 15) -> dict:
    """
    Prepares dataset dictionary for the Route Analytics charts.
    Separates data into controlled (Top N) and freed (All Network) subsets.
    """
    route_datasets = {
        'avg_del_time_route': None,
        'exp_vs_act_del_time': None,
        'distance_vs_del_time': None,
        'delayed_routes': None,
        'route_volume': None,
        'route_perf_table': None
    }
    
    if df.empty:
        return route_datasets

    # 1. Base Aggregation
    route_group_df = df.groupby(['route_id', 'origin', 'destination', 'distance_km'], as_index=False).agg(
        total_del_time=('actual_time_hrs', 'sum'),
        avg_del_time=('actual_time_hrs', 'mean'),
        total_expected_del_time=('expected_time_hrs', 'sum'),
        avg_expected_del_time=('expected_time_hrs', 'mean'),
        total_shipments_by_group=('shipment_id', 'count'),
        total_weight=('weight', 'sum')                              
    )
    
    route_group_df['avg_delay'] = route_group_df['avg_del_time'] - route_group_df['avg_expected_del_time']
    route_group_df['relative_avg_delay'] = route_group_df['avg_delay'] / route_group_df['avg_expected_del_time'].replace(0, 0.01)
    route_group_df['volume'] = route_group_df['total_shipments_by_group'] * route_group_df['total_weight']
    
    # 2. Controlled Subset
    controlled_df = route_group_df.sort_values(by=sort_by, ascending=is_ascending).head(display_limit)

    # ----------------- Controlled Data: Average Delivery Time -----------------
    avg_del_time_route_df = controlled_df[['route_id', 'origin', 'destination', 'distance_km', 'avg_del_time']].copy()

    # ----------------- Controlled Data: Expected vs Actual -----------------
    exp_vs_act_del_time_df = controlled_df[['route_id', 'origin', 'destination', 'distance_km', 'avg_expected_del_time','avg_del_time']].copy()
    exp_vs_act_del_time_df = exp_vs_act_del_time_df.melt(
        id_vars=['route_id', 'origin', 'destination', 'distance_km'],
        value_vars=['avg_expected_del_time', 'avg_del_time'],        
        var_name='Time Category',                   
        value_name='Hours'
    )
    exp_vs_act_del_time_df['Time Category'] = exp_vs_act_del_time_df['Time Category'].replace({
        'avg_expected_del_time': 'Expected Time',
        'avg_del_time': 'Actual Time'
    })

    # ----------------- Controlled Data: Delayed Routes -----------------
    delayed_route_df = controlled_df[['route_id', 'origin', 'destination', 'distance_km', 'avg_delay']].copy()
    delayed_route_df = delayed_route_df.sort_values(by='avg_delay', ascending=True)

    # ----------------- Freed Data: Distance vs Delivery Time (Scatter) -----------------
    distance_vs_del_time_df = route_group_df[['route_id', 'distance_km', 'avg_del_time']].copy()

    # ----------------- Freed Data: Route Volume (Heatmap) -----------------
    route_volume_df = route_group_df[['route_id', 'origin', 'destination', 'distance_km', 'total_shipments_by_group']].copy()
    route_volume_df = route_volume_df.rename(columns={'total_shipments_by_group': 'Total Shipments'})
    
    # ----------------- Freed Data: Route Performance Table -----------------
    route_performance_df = route_group_df[['route_id', 
                                           'origin', 
                                           'destination', 
                                           'distance_km', 
                                           'avg_del_time',
                                           'avg_expected_del_time',
                                           'avg_delay',
                                           'total_shipments_by_group'
                                           ]].copy()

    route_performance_df.columns = [
        'Route ID', 'Origin', 'Destination', 'Distance (Kms)', 
        'Actual Time (Hrs)', 'Expected Time (Hrs)', 'Avg Delay (Hrs)', 'Total Shipments'
    ]
    
    numeric_cols = ['Distance (Kms)', 'Actual Time (Hrs)', 'Expected Time (Hrs)', 'Avg Delay (Hrs)']
    route_performance_df[numeric_cols] = route_performance_df[numeric_cols].round(1)
    
    route_datasets['avg_del_time_route'] = avg_del_time_route_df
    route_datasets['exp_vs_act_del_time'] = exp_vs_act_del_time_df
    route_datasets['distance_vs_del_time'] = distance_vs_del_time_df
    route_datasets['delayed_routes'] = delayed_route_df
    route_datasets['route_volume'] = route_volume_df
    route_datasets['route_perf_table'] = route_performance_df
    
    return route_datasets
# end region Route Datasets