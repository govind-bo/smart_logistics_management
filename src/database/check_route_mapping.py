import pandas as pd
from sqlalchemy import text
from src.database.engine import get_engine

query = text(
    '''
    SELECT shipment_id, origin, destination, route_id
    FROM shipments
    LIMIT 10
    '''
    )

db_engine = get_engine()
with db_engine.connect() as connection:
    df = pd.read_sql(query, connection)

print(df)
