import pandas as pd
from sqlalchemy import text
from src.database.engine import get_engine

def show_indexes(table_name: str) -> None:
    '''
    Displays indexes for a given table
    '''

    engine = get_engine()
    query = text(f"SHOW INDEX FROM {table_name}")
    with engine.connect() as connection:
        indexes_df = pd.read_sql(query, connection)
    print(f"\nIndexes for table : {table_name}\n")
    print(
        indexes_df[
            [
                'Key_name',
                'Column_name',
                'Non_unique'
            ]
        ]
    )


if __name__ == '__main__':

    show_indexes('shipments')
    show_indexes('shipment_tracking')
    show_indexes('routes')