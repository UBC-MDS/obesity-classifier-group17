# split_n_preprocessor.py
# author: Yun Zhou
# date: 2024-12-5

import click
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import make_column_transformer, make_column_selector
from sklearn.pipeline import make_pipeline

@click.command()
@click.option('--clean-data', type=str, help="Path to the data after cleaning")
@click.option('--data-to', type=str, help="Path to directory where splitted data will be written to")
#@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="seed for random state", default=522)
def main(clean_data, data_to, seed):
    '''This script splits the data after cleaning for training and testing.
    EDA will be performed on training data set.
    The preprocessor will be applied for model training.'''

    # Set random state
    seed_random_state = seed

    # Input data
    merged_df = pd.read_csv(clean_data)
    X = merged_df.drop('obesity_level', axis=1)
    y = merged_df['obesity_level']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=seed_random_state, stratify=y)
   
    X_train_df = pd.DataFrame(X_train, columns=X.columns)  
    y_train_df = pd.DataFrame(y_train, columns=['obesity_level'])
    train_df = pd.concat([X_train_df, y_train_df], axis=1)

    X_test_df = pd.DataFrame(X_test, columns=X.columns)  
    y_test_df = pd.DataFrame(y_test, columns=['obesity_level'])
    test_df = pd.concat([X_test_df, y_test_df], axis=1)

    # Store splitted data
    train_df.to_csv(os.path.join(data_to, "obesity_train.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "obesity_test.csv"), index=False)

if __name__ == '__main__':
    main()