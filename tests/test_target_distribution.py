# Code template adapted is from work by Tiffany A. Timbers in breast-cancer-predictor repository:
# https://github.com/ttimbers/breast-cancer-predictor/blob/3.0.0/tests/test_write_csv.py

import pytest
from pytest import approx
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.target_distribution import prepare_distribution_data

# Generate toy dataset
# Balanced distribution: 4A; 4B; 4C; 4D 
valid_data = pd.DataFrame({'target': ['A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C', 'A', 'B', 'C']})

# Test cases

def test_valid_data():
    '''Test with a valid dataset to check if the function calculates correct counts, 
    expected values, and correct thresholds.'''
    result = prepare_distribution_data(valid_data, 'target')
    assert result['count'].tolist() == [4, 4, 4], "Incorrect counts." 
    assert result['expected'].iloc[0] == 12 / 3, "Incorrect expected count."
    assert result['expected_lower'].iloc[0] == (12 / 3) * 0.8, "Incorrect lower threshold."
    assert result['expected_upper'].iloc[0] == (12 / 3) * 1.2, "Incorrect upper threshold."

def test_missing_column():
    '''Test with missing target column to ensure it raises a KeyError.'''
    invalid_data = valid_data.drop(columns=['target'])
    with pytest.raises(KeyError):
        prepare_distribution_data(invalid_data, 'target')

def test_empty_dataframe():
    '''Test with an empty DataFrame to ensure it raises a ValueError.'''
    empty_data = pd.DataFrame(columns=['target'])
    with pytest.raises(ZeroDivisionError):
        prepare_distribution_data(empty_data, 'target')

def test_single_category():
    '''Test with a DataFrame that includes only one unique value in the target column.'''
    single_category_data = pd.DataFrame({'target': ['A'] * 12})
    result = prepare_distribution_data(single_category_data, 'target')
    assert result['count'].tolist() == [12], "Incorrect count for single category."
    assert result['expected'].iloc[0] == 12, "Incorrect expected count for single category."
    assert result['expected_lower'].iloc[0] == approx(12 * 0.8), "Incorrect lower threshold for single category."
    assert result['expected_upper'].iloc[0] == approx(12 * 1.2), "Incorrect upper threshold for single category."

def test_unbalanced_data():
    '''Test by an unbalanced dataset to make sure thresholds are calculated correctly.'''
    unbalanced_data = pd.DataFrame({'target': ['A', 'A', 'A', 'B', 'B', 'C']}) # Unbalanced dataset
    result = prepare_distribution_data(unbalanced_data, 'target')
    assert result['count'].tolist() == [3, 2, 1], "Incorrect counts for unbalanced data."
    assert result['expected'].iloc[0] == 6 / 3, "Incorrect expected count for unbalanced data."
    assert result['expected_lower'].iloc[0] == 2 * 0.8, "Incorrect lower threshold for unbalanced data."
    assert result['expected_upper'].iloc[0] == 2 * 1.2, "Incorrect upper threshold for unbalanced data."

def test_non_string_category():
    '''Test with a target column that doesn't include categorcal values (using integers for test).'''
    numeric_data = pd.DataFrame({'target': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]})
    result = prepare_distribution_data(numeric_data, 'target')
    assert result['count'].tolist() == [4, 4, 4], "Incorrect counts for numeric categories."
    assert result['expected'].iloc[0] == 12 / 3, "Incorrect expected count for numeric categories."
    assert result['expected_lower'].iloc[0] == (12 / 3) * 0.8, "Incorrect lower threshold for numeric categories."
    assert result['expected_upper'].iloc[0] == (12 / 3) * 1.2, "Incorrect upper threshold for numeric categories."


