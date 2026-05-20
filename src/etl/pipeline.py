import os
from extract_data import load_raw_data
from inspect_data import inspect_dataframes


def main():
    '''
    This function runs all related function and controls the flow
    '''
    print('\nloading raw datasets...')
    # base path store the directory where the raw files are stored
    base_path = os.path.join('D:\\',
                             'AI ML',
                             '04. project',
                             'smart_logistics_management',
                             'data',
                             'raw_data')
    dataframes = load_raw_data(base_path)

    if not dataframes:
        print('No dataframes loaded')
        return
    
    print('\nInspecting datasets...')

    inspect_dataframes(dataframes)      # inspects structural inspection, duplicates, missingness and summary statistics of the tables

    print('\nPipeline completed\n')

if __name__ == "__main__":
    main()
