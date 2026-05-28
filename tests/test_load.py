import pandas as pd

from src.etl.load_to_mysql import load_dataframe

df = pd.DataFrame({
    "courier_id": [1],
    "name": ["Test"],
    "rating": [4.5],
    "vehicle_type": ["Bike"]
})

load_dataframe(df, "courier_staff")