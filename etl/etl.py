import pandas as pd
import requests
import json


def get_json_from_api(url: str) -> json:
    """Retrieves fear and greed index via API

    Args:
        url (str): requests URL

    Returns:
        json: response to GET request
    """    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as Ex:
        print(f'Error in retriving data from {url}: {Ex}')


def fng_json_to_df(json: json) -> pd.DataFrame:
    """Converts response to GET request (Fear and Greed index) to DataFrame

    Args:
        json (json): response to GET request

    Returns:
        pd.DataFrame: table of two columns: Date and Fear&Greed index
    """    
    try:
        df = pd.DataFrame(json["data"])
        df['date'] = pd.to_datetime(df['timestamp'].astype(int), unit='s')
        df = df[['date', 'value']].set_index('date').sort_index()
        return df
    except Exception as Ex:
        print(f'Error in converting fear&greed json to DataFrame: {Ex}')


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Saves DataFrame to csv in data folder

    Args:
        df (pd.DataFrame): DataFrame
        file_path (str): csv file directory
    """    
    try:
        df_saved = pd.read_csv(file_path, index_col=0)
    except FileNotFoundError:
        try:
            df.to_csv(file_path)
        except Exception as Ex:
            print(f'Error while saving to {file_path}: {Ex}')
    else:
        try:
            df_saved.index = pd.to_datetime(df_saved.index)
            df_union = pd.concat([df_saved, df])
            df_union = df_union[~df_union.index.duplicated(keep='last')]
            df_union = df_union.sort_index()
            df_union.to_csv(file_path)
        except Exception as Ex:
            print(f'Error while concatenating DataFrames and saving to {file_path}: {Ex}')