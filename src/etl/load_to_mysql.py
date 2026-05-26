import pandas as pd
from sqlalchemy import text
from src.database.connection import get_engine
from config.schema_config import LOAD_ORDER


def prepare_data(dataframes: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    
    '''
    Converts:
        - shipments.order_date and shipments.delivery_date to date
        - shipment_tracking.timestamp to datetime

    Returns updated dataframe dictionary.
    '''
    

    if "shipments" in dataframes:

        dataframes["shipments"]["order_date"] = pd.to_datetime(
            dataframes["shipments"]["order_date"],
            errors="coerce"
        ).dt.date

        dataframes["shipments"]["delivery_date"] = pd.to_datetime(
            dataframes["shipments"]["delivery_date"],
            errors="coerce"
        ).dt.date

    if "shipment_tracking" in dataframes:

        dataframes["shipment_tracking"]["timestamp"] = pd.to_datetime(
            dataframes["shipment_tracking"]["timestamp"],
            errors="coerce"
        )

    return dataframes


def clear_tables(engine) -> None:
    '''
    - Performs full refresh cleanup by truncating all MySQL tables.
    - Foreign key checks are temporarily disabled for truncation of dependent child tables.
    - Tables are truncated in reverse dependency order (children first, parents last).
    '''

    with engine.begin() as conn:

        # disable FK checks for full refresh
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        # truncate in reverse order (children first)
        for table in reversed(LOAD_ORDER):
            conn.execute(text(f"TRUNCATE TABLE {table};"))

        # re-enable FK checks
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))


def load_data_to_mysql(dataframes: dict[str, pd.DataFrame]) -> None:
    '''
    Loads cleaned dataframe into MySQL tables.

    Workflow:
        1. Prepare dataframe datatypes
        2. Clear existing table data (full refresh)
        3. Load tables in dependency order

    Data is inserted using pandas.to_sql() with batch loading.
    '''
    # datatype fixes
    dataframes = prepare_data(dataframes)

    # full refresh cleanup
    engine = get_engine()
    clear_tables(engine)

    # load tables in dependency order
    for table in LOAD_ORDER:
        if table not in dataframes:
            print(f"[SKIP] {table} not found")
            continue
        df = dataframes[table]

        print(f"[LOADING] {table} to MySQL | rows = {len(df)}")

        df.to_sql(
            name = table,
            con = engine,
            if_exists = "append",   
            index = False,
            chunksize = 5000
        )

        print(f"[LOADED] {table}")

    print("\nALL TABLES LOADED SUCCESSFULLY")