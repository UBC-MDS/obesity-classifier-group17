# Code below is adapted from work by Tiffany A. Timbers in breast-cancer-predictor repository
# https://github.com/ttimbers/breast-cancer-predictor/blob/main/scripts/download_data.py
# download_data.py
# author: Zanan Pech
# date: 2024-12-04

import click
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write_to', type=str, help="Path to directory where raw data will be written to")
def main(url, write_to):
    """Downloads data from the web to a local filepath."""
    try:
        data = pd.read_csv(url)
        data.to_csv(write_to)
    except:
        os.makedirs(write_to)
        data.to_csv(write_to)

if __name__ == '__main__':
    main()