# Code below is adapted from work by Tiffany A. Timbers in breast-cancer-predictor repository
# https://github.com/ttimbers/breast-cancer-predictor/blob/main/scripts/split_n_preprocess.py
# download_data.py
# author: Zanan Pech
# date: 2024-12-04

import click
import os
import sys
import numpy as np
import pandas as pd
from sklearn import set_config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--name', type=str, help="name of processed the file")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(raw_data, name, data_to, seed):

    '''This script checks the number of rows and columns of the data frame against the documentation.
    It checks whether type is Panda data frame and that the column names match the documentation.
    Additionally the column names are changes to a more interpretable name.
    Finally it validates the data based on the function from validate_data.py file
    and drop duplicates/invalid rows.
    The cleaned data is saved in a directory path.
    '''
    np.random.seed(seed)
    set_config(transform_output="pandas")
    
    merged_df = pd.read_csv(raw_data, index_col=0)

    # 1. Check correct data file format
    # The number of instances and features are retrieved from the dataset information in the documentation linked below
    # https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition

    # Check if number of instances are the same as documentation 
    assert merged_df.shape[0] == 2111, "merged_df does not have number of instances mentioned in the documentation"

    # check if number of features are the same as documentation (17 including the target)
    assert merged_df.shape[1] == 17, "merged_df does not have number of features mentioned in the documentation"

    # check if DataFrame is correct type
    assert isinstance(merged_df, pd.DataFrame), "merged_df is not a pandas DataFrame" 

    # Create variable with features listed in the documentation cited in cell above 
    original_column_names = ['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
        'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',
        'CALC', 'MTRANS', 'NObeyesdad']
    
    # 2. Check columns names (Data Validation)
    assert sorted(original_column_names) == sorted(merged_df.columns), "merged_df does not have the same column names as original_column_names"

    # Rename columns into meaningful names
    rename_dict = {
        'Gender': 'gender',
        'Age': 'age',
        'Height': 'height',
        'Weight': 'weight',
        'FAVC': 'frequent_high_calorie_intake',
        'FCVC': 'vegetable_intake_in_meals',
        'NCP': 'meals_per_day',
        'CAEC': 'food_intake_between_meals',
        'SMOKE': 'smoker',
        'CH2O': 'daily_water_intake',
        'SCC': 'monitor_calories',
        'FAF': 'days_per_week_with_physical_activity',
        'TUE': 'daily_screen_time',
        'CALC': 'frequent_alcohol_intake',
        'MTRANS': 'mode_of_transportation',
        'NObeyesdad': 'obesity_level'
    }

    merged_df = merged_df.rename(columns = rename_dict)
    
    # validate_data() is imported from validate_data.py in src folder
    validate_data(merged_df)

    merged_df_cleaned = merged_df.drop_duplicates().dropna(how="all")

     # Check if the directory exists, else create one.
    os.makedirs(data_to, exist_ok=True)
    merged_df_cleaned.to_csv(f'{data_to}/{name}')

if __name__ == '__main__':
    main()