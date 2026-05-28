import os
from src.etl.extract_data import load_raw_data
from src.etl.inspect_data import inspect_dataframes
from src.etl.data_validation import validate_data
from src.etl.data_cleaning import clean_data
from src.etl.load_to_mysql import load_data_to_mysql
from src.database.run_sql_script import run_sql_script


# base path store the directory where the raw files are stored
raw_data_path = os.path.join('D:\\',
                             'AI ML',
                             '04. project',
                             'smart_logistics_management',
                             'data',
                             'raw_data')

processed_data_folder_path = os.path.join('D:\\',
                             'AI ML',
                             '04. project',
                             'smart_logistics_management',
                             'data',
                             'processed_data')

dup_id = "c2c0ddd0"

def etl_pipeline():
    '''
    Runs the complete ETL pipeline:
        1. Extract raw datasets
        2. Inspect datasets
        3. Validate datasets
        4. Clean datasets
        5. Validate cleaned datasets
        6. Load cleaned datasets into MySQL
    '''

    print('\n[EXTRACTING] Loading raw datasets...')

    dataframes = load_raw_data(raw_data_path)

    if not dataframes:
        print('[ERROR] No dataframes loaded')
        return
    
    print('\n[INSPECTING] Inspecting datasets...')
    inspect_dataframes(dataframes)      # inspects structural inspection, duplicates, missingness and summary statistics of the tables

    print('\n[VALIDATING] Validating raw datasets...')
    validate_data(dataframes)

    print('\n[CLEANING] Cleaning datasets...')
    clean_dataframes = clean_data(dataframes, processed_data_folder_path, dup_id)

    print('\n[VALIDATING] Validating cleaned datasets...')
    validate_data(clean_dataframes)

    print('\n[LOADING] Loading cleaned datasets to MySQL...')
    load_data_to_mysql(clean_dataframes)

 
    print('\n[SUCCESS] ETL Pipeline completed successfully\n')

    

if __name__ == "__main__":
    etl_pipeline()
