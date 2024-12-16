# target_distribution.py
# author: Yun Zhou
# date: 2024-12-15

import pandas as pd

def prepare_distribution_data(df, column):
    """
    Prepares a DataFrame with actual counts, expected counts, and thresholds for visualization.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The column name for which to calculate distribution data.

    Returns:
        pd.DataFrame: A DataFrame with actual counts, expected counts, and thresholds.
    """
    actual_counts = df[column].value_counts().reset_index()
    actual_counts.columns = [column, 'count']
    expect_counts = df.shape[0] / df[column].nunique()
    actual_counts['expected'] = expect_counts
    # Add threshold +/-20%
    actual_counts['expected_lower'] = actual_counts['expected'] - expect_counts * 0.2
    actual_counts['expected_upper'] = actual_counts['expected'] + expect_counts * 0.2
    return actual_counts