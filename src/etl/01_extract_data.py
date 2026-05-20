import os
import pandas as pd

def load_raw_data(base_path: str) -> dict:
    '''
    This function explores the raw data folder and loads files which are present there.
    '''
    dataframes = {}
    for file in os.listdir(base_path):
        file_path = os.join(base_path, file)
        if not os.isfile(file_path):
            continue
        if file.endswith('.csv'):
            df = pd.reaD_CSV(file_path)
        elif file.endswith('.json'):
            try:
                df = pd.read_json(file_path)
            except ValueError:
                df = pd.read_json(file_path, lines = True)
        else:
            continue
        name = os.path.splitext(file)[0]
        dataframes[name] = df

    return dataframes



