from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.database.engine import get_engine

def load_sql_file(folder: str, sql_file: str) -> str:
    """Loads SQL query from file."""
    file_path = Path("sql") / "analytics_sql" / folder / sql_file
    if not file_path.exists():
        raise FileNotFoundError(f"SQL file not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def run_query(query: str, params: dict | None = None) -> pd.DataFrame:
    """Executes basic SQL queries (used for filter dropdowns)."""
    engine = get_engine()
    params = params or {}
    with engine.connect() as conn:
        df = pd.read_sql(text(query), con=conn, params=params)
    return df

def run_sql_file(folder: str, sql_file: str, params: dict | None = None) -> pd.DataFrame:
    """Loads a basic SQL file and executes it."""
    query = load_sql_file(folder, sql_file)
    return run_query(query=query, params=params)

def run_smart_query(folder: str, sql_file: str, params: dict) -> pd.DataFrame:
    """Loads SQL file and dynamically appends chosen multi-select arrays securely."""
    engine = get_engine()
    query_string = load_sql_file(folder, sql_file)
    
    query_params = {
        "start_date": params["start_date"],
        "end_date": params["end_date"]
    }
    
    # Map the state variables to their corresponding SQL Column identifiers
    optional_filters = [
        ("s.origin", params.get("origin")),
        ("s.destination", params.get("destination")),
        ("s.status", params.get("shipment_status")),
        ("cs.name", params.get("courier"))
    ]
    
    for column_identifier, selected_values in optional_filters:
        if selected_values:  # Execute only if items are explicitly chosen
            # Strip prefixes like 's.' or 'cs.' to generate clean internal binding keys
            clean_key = column_identifier.split(".")[-1]
            placeholders = [f":{clean_key}_{i}" for i in range(len(selected_values))]
            
            # Form syntax valid list structures: AND column IN (:key_0, :key_1)
            in_clause = f" AND {column_identifier} IN ({', '.join(placeholders)})"
            query_string += in_clause
            
            for i, val in enumerate(selected_values):
                query_params[f"{clean_key}_{i}"] = val

    with engine.connect() as conn:
        df = pd.read_sql(text(query_string), con=conn, params=query_params)
    return df