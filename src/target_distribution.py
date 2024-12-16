# target_distribution.py
# author: Yun Zhou
# date: 2024-12-15

import pandas as pd

def prepare_distribution_data(df, column):
    """
    Prepares a DataFrame to check the counts of the categories in the target variable.
    Actual counts, expected counts, and thresholds are produced for visualization.
    (This is to check if the dataset is balanced).

    Parameters:
    ----------
    df: pd.DataFrame
        The input DataFrame.
    column: str
        The column name for which to calculate the distribution data - specifically the target variable.

    Returns:
    --------
    actual_counts: pd.DataFrame
        A DataFrame with actual counts, expected counts, and thresholds.

    Raises:
    --------
    KeyError
        If the specified column does not exist in the DataFrame.
    ZeroDivisionError
        If the DataFrame is empty or the specified column has no unique values.
    """
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in the DataFrame.")
    if df.empty or df[column].nunique() == 0:
        raise ZeroDivisionError("DataFrame is empty or the specified column has no unique values.")
    
    actual_counts = df[column].value_counts().reset_index()
    actual_counts.columns = [column, 'count']
    expect_counts = df.shape[0] / df[column].nunique()
    actual_counts['expected'] = expect_counts
    # Add threshold +/-20%
    actual_counts['expected_lower'] = actual_counts['expected'] - expect_counts * 0.2
    actual_counts['expected_upper'] = actual_counts['expected'] + expect_counts * 0.2
    return actual_counts
