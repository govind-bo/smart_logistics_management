import pandas as pd

# region KPIs
def calculate_cost_metrics(df: pd.DataFrame) -> dict:
    """
    Calculates KPIs for the Cost Analytics page of the dashboard.
    """
    cost_metrics = {
        'total_operational_cost': 0.0,
        'avg_cost_per_shipment': 0.0,
        'highest_cost_val': 0.0,
        'highest_cost_shipment_id': '-',
        'highest_cost_origin': '-',
        'highest_cost_destination': '-',
        'highest_cost_route_id': '-'
    }

    if df.empty:
        return cost_metrics
        
    df['total_cost'] = df.get('fuel_cost', 0) + df.get('labor_cost', 0) + df.get('misc_cost', 0)
    total = len(df)
    max_idx = df['total_cost'].idxmax()

    cost_metrics['total_operational_cost'] = df['total_cost'].sum()
    cost_metrics['avg_cost_per_shipment'] = cost_metrics['total_operational_cost'] / total
    cost_metrics['highest_cost_val'] = df['total_cost'].max()
    cost_metrics['highest_cost_shipment_id'] = df.loc[max_idx, 'shipment_id']

    # Extract highest cost route details safely
    route_cost_row = (
        df.groupby(['route_id', 'origin', 'destination'], as_index=False)['total_cost']
        .sum()
        .sort_values(by='total_cost', ascending=False)
        .head(1)
    )
    
    if not route_cost_row.empty:
        cost_metrics['highest_cost_route_id'] = route_cost_row['route_id'].iloc[0]
        cost_metrics['highest_cost_origin'] = route_cost_row['origin'].iloc[0]
        cost_metrics['highest_cost_destination'] = route_cost_row['destination'].iloc[0]

    return cost_metrics
# endregion

# region Datasets for Charts
def prepare_cost_datasets(df: pd.DataFrame, sort_by: str = 'total_cost', is_ascending: bool = False, display_limit: int = 15) -> dict:
    """
    Prepares dataset dictionaries for the Cost Analytics charts.
    """
    df['total_cost'] = df.get('fuel_cost', 0) + df.get('labor_cost', 0) + df.get('misc_cost', 0)

    # --- 1. Route Performance Hub (Master Route Data) ---
    route_master = df.groupby(['route_id', 'origin', 'destination', 'distance_km'], as_index=False).agg(
        total_cost=('total_cost', 'sum'),
        fuel_cost=('fuel_cost', 'sum'),
        labor_cost=('labor_cost', 'sum'),
        misc_cost=('misc_cost', 'sum'),
        total_weight=('weight', 'sum')
    )
    

    
    # Calculate efficiencies on the unified sorted slice safely
    route_master['cost_per_kg'] = route_master['total_cost'] / route_master['total_weight'].replace(0, 1)
    route_master['cost_per_km'] = route_master['total_cost'] / route_master['distance_km'].replace(0, 1)
    
    # Sort ONCE to lock the X-axis order for all three route charts
    route_master = route_master.sort_values(by=sort_by, ascending=is_ascending).head(display_limit)


    route_costs_df = route_master.melt(
        id_vars=['route_id', 'origin', 'destination', 'distance_km', 'total_cost'],
        value_vars=['fuel_cost', 'labor_cost', 'misc_cost'],
        var_name='cost_category',
        value_name='category_cost'
    )
    route_costs_df['cost_category'] = route_costs_df['cost_category'].str.replace('_cost', '').str.title()
    route_costs_df['category_cost'] = route_costs_df['category_cost'].fillna(0).round().astype(int)

    # --- 2. Cost Trends (Line Chart) ---
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    trend_df = df.dropna(subset=['order_date']).copy()
    cost_trend_df = trend_df.groupby(trend_df['order_date'].dt.to_period('M').dt.to_timestamp())['total_cost'].sum().reset_index()

    # --- 3. Cost Mix Data (Pie Chart) ---
    cost_mix_df = pd.DataFrame({
        'Cost Category': ['Fuel', 'Labor', 'Miscellaneous'],
        'Total Amount': [
            df['fuel_cost'].sum(), 
            df['labor_cost'].sum(), 
            df['misc_cost'].sum()
        ]
    })

    # --- 4. Cost Scaling Data (Scatter Plot) ---
    cost_scaling_df = df[['shipment_id', 'weight', 'total_cost', 'distance_km']].copy()
    n = min(len(cost_scaling_df), 300)
    cost_scaling_df = cost_scaling_df.sample(n=n, random_state=42)

    # --- 5. High Cost Shipments Data (Data Table) ---
    high_cost_shipments_df = df[['shipment_id', 'route_id', 'weight', 'fuel_cost', 'labor_cost', 'misc_cost', 'total_cost']].copy()
    high_cost_shipments_df = high_cost_shipments_df.sort_values(by=['total_cost', 'weight'], ascending=False)

    return {
        'route_master': route_master,               # Passed to: Cost Efficiency per Kg & Cost Efficiency per Km Bar Charts
        'route_costs': route_costs_df,              # Passed to: Stacked Cost per Route Bar Chart
        'cost_trend': cost_trend_df,                # Passed to: Monthly Operational Cost Line Chart
        'cost_mix': cost_mix_df,                    # Passed to: Operational Cost Mix Pie Chart
        'cost_scaling': cost_scaling_df,            # Passed to: Cost Distribution Scatter Plot
        'high_cost_shipments': high_cost_shipments_df # Passed to: Interactive Cost Explorer Dataframe
    }
# endregion