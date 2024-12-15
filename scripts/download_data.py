# Code below is adapted from work by uci machine learning repository
# https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition
# download_data.py
# author: Zanan Pech
# date: 2024-12-04

from ucimlrepo import fetch_ucirepo 
import click
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.prepare_dataset import prepare_dataset


@click.command()
@click.option('--id', type=int, help="id of the dataset", default=544)
@click.option('--name', type=str, help="name of the raw file")
@click.option('--write_to', type=str, help="Path to directory where raw data will be written to")
def main(id, name, write_to):
    """Downloads data from the web to a local filepath."""

    result = fetch_ucirepo(id=id)
    merged_df = prepare_dataset(result)

    # Check if the directory exists, else create one.
    os.makedirs(write_to, exist_ok=True)
    merged_df.to_csv(f'{write_to}/{name}')


if __name__ == '__main__':
    main()
