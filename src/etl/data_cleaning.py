import os
import pandas as pd


def _clear_processed_data_folder(processed_data_folder_path: str) -> None:
    '''
    Deletes existing files inside the processed data folder,
    this will prevent extra file creation or errors when we rerun this code
    '''
    os.makedirs(processed_data_folder_path, exist_ok = True)

    for name in os.listdir(processed_data_folder_path):
        path = os.path.join(processed_data_folder_path, name)
        if os.path.isfile(path):
            os.remove(path)


def _data_cleaner(dataframes: dict, dup_id: str ) -> dict:
    '''
    This function cleans the duplicate ids from the dataframe passed into it
    for the known duplicate id it will keep the delievered row and remove the cancelled row
    '''
    clean_dataframes = {}
    for df_name in dataframes:
        if df_name == 'shipments':
            shipment_df = dataframes[df_name]
            shipment_df = shipment_df[~(
                                (shipment_df['shipment_id'] == dup_id) & 
                                (shipment_df['status'].str.lower() == 'cancelled')
            )]          
            clean_dataframes[df_name] = shipment_df
        elif df_name == 'shipment_tracking':
            s_tracking_df = dataframes[df_name]
            s_tracking_df['timestamp'] = pd.to_datetime(s_tracking_df['timestamp'])
            s_tracking_df = s_tracking_df[~(
                                (s_tracking_df['shipment_id'] == dup_id) &
                                (s_tracking_df['timestamp'].dt.year == 2026)                # best way to make it dynamic ?????????????????????
            )]
            clean_dataframes[df_name] = s_tracking_df
        elif df_name =='costs':
            cost_df = dataframes[df_name]
            # kept last because in shipment and shipment tracking id tables, the cancelled shipment has a lower index number. 
            # So assuming the same shipment's cost was also entered first into costs table
            cost_df = cost_df.drop_duplicates(subset = 'shipment_id', keep = "last")        
            clean_dataframes[df_name] = cost_df
        else:
            clean_dataframes[df_name] = dataframes[df_name]

    return clean_dataframes

def _processed_files_saver(clean_dataframes: dict, processed_data_folder_path: str) -> None:
    for df_name in clean_dataframes:
        clean_dataframes[df_name].to_csv(os.path.join(processed_data_folder_path, f"{df_name}.csv"), index = False)

def clean_data(dataframes: dict, processed_data_folder_path: str, dup_id: str) -> dict:
    '''
    This function:
    - clears the processed_data folder
    - cleans duplicates from the shipment and shipment_tracking file
    - saves processed files

    and at the end returns the dictionary with the cleaned dataframes
    '''
    _clear_processed_data_folder(processed_data_folder_path)

    clean_dataframes = _data_cleaner(dataframes, dup_id)

    _processed_files_saver(clean_dataframes, processed_data_folder_path)
    
    return clean_dataframes