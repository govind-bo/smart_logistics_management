import os
from src.etl.extract_data import load_raw_data
from src.etl.inspect_data import inspect_dataframes
from src.etl.data_validation import validate_data
from src.etl.data_cleaning import clean_data


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


def main():
    '''
    This function runs all related function and controls the flow
    '''
    print('\nloading raw datasets...')

    dataframes = load_raw_data(raw_data_path)

    if not dataframes:
        print('No dataframes loaded')
        return
    
    print('\nInspecting datasets...')
    inspect_dataframes(dataframes)      # inspects structural inspection, duplicates, missingness and summary statistics of the tables

    print('\nValidating data...')
    validate_data(dataframes)

    print('\nCleaning and saving data...')
    clean_dataframes = clean_data(dataframes, processed_data_folder_path, dup_id)

    print('\nValidating cleaned datasets...')
    validate_data(clean_dataframes)

    

    print('\nPipeline completed\n')

    

if __name__ == "__main__":
    main()
