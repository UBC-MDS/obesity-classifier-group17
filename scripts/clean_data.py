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
import pickle
from sklearn.model_selection import train_test_split
from sklearn import set_config
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--seed', type=int, help="Random seed", default=123)
def main(raw_data, data_to, seed):
    '''This script splits the raw data into train and test sets, 
    and then preprocesses the data to be used in exploratory data analysis.
    It also saves the preprocessor to be used in the model training script.'''
    np.random.seed(seed)
    set_config(transform_output="pandas")
    
    obesity_df = pd.read_csv(raw_data)
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

    obesity_df = obesity_df.rename(columns = rename_dict)
    
    validate_data(obesity_df)

    obesity_df_cleaned = obesity_df.drop_duplicates().dropna(how="all")
    obesity_df_cleaned.to_csv(data_to)

if __name__ == '__main__':
    main()