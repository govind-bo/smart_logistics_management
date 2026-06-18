from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.database.engine import get_engine

def load_sql_file(folder: str, sql_file: str) -> str:
    file_path = Path("sql") / "analytics_sql" / folder / sql_file                  
    if not file_path.is_file():
        raise FileNotFoundError(f"SQL file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:      
        return file.read()

def fetch_filtered_data(folder: str, sql_file: str, params: dict | None = None) -> pd.DataFrame: 
    engine = get_engine()
    query_string = load_sql_file(folder, sql_file)
    params = params or {}
    query_params = {}               
    
    # 1. Apply Dates if present
    if params.get('start_date') and params.get('end_date'):
        # Only append date filter if the SQL query doesn't already have it written inside
        if ":start_date" not in query_string:
            query_string += " AND s.order_date BETWEEN :start_date AND :end_date"
        query_params['start_date'] = params['start_date']
        query_params['end_date'] = params['end_date']

    # 2. Explicit Mapping with db columns - to maintain Abstraction (separation of concerns), cleanliness and SECURITY ????HOW???????
    filter_map = {
        'origin': 's.origin',
        'destination': 's.destination',
        'shipment_status': 's.status',
        'courier': 'cs.name',
        'shipment_id': 's.shipment_id'
    }

    # 3. Build the IN clauses dynamically
    for dict_key, db_column in filter_map.items():
        selected_values = params.get(dict_key, [])
        if selected_values: 
            # check for shipment_id and convert to list
            if isinstance(selected_values, str):
                selected_values = [selected_values]

            placeholders = []
            for i, val in enumerate(selected_values):
                param_name = f"{dict_key}_{i}"
                placeholders.append(f":{param_name}")
                query_params[param_name] = val
                
            # Safely append to the WHERE clause
            query_string += f" AND {db_column} IN ({', '.join(placeholders)})"

    with engine.connect() as conn:
        df = pd.read_sql(text(query_string), con=conn, params=query_params)

    return df