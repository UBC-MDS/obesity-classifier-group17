# Code template below is adapted from work by Tiffany A. Timbers in breast-cancer-predictor repository:
# https://github.com/ttimbers/breast-cancer-predictor/blob/3.0.0/tests/test_write_csv.py


import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_clean_dataset import split_clean_dataset

@pytest.fixture
def mock_dataframe():
    """Create data frame for testing expected cases"""
    df = pd.DataFrame({
            "column1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "column2": [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "target": ["one", "two", "one", "two", "one", "two", "one", "two", "one", "two"]
        })
    
    return df

# Test: Expected case
def test_split_data_expected(mock_dataframe):
    """Test the expected case with mock dataset"""
    train_df, test_df, X, y_train = split_clean_dataset(df=mock_dataframe, target_variable='target', test_size=0.3, random_state=552)

    # Test size of of the splits
    assert len(train_df) == 7
    assert len(test_df) == 3

    # Test if returned object is pandas dataFrame
    assert isinstance(train_df, pd.DataFrame)
    assert isinstance(test_df, pd.DataFrame)
    assert isinstance(X, pd.DataFrame)
    assert isinstance(y_train, pd.Series)

    # Test if X does not have target column
    assert 'target' not in X.columns

    # Test if all features exist in both test and train splits
    assert list(train_df.columns) == ["column1", "column2", "target"]
    assert list(test_df.columns) == ["column1", "column2", "target"]

# Test: Error cases
def test_invalid_input_df():
    """Test the error case when input data frame is invalid"""
    with pytest.raises(TypeError, match="The input is not a pandas DataFrame."):
        split_clean_dataset(df="invalid_input", target_variable='target', test_size=0.3, random_state=552)

def test_empty_dataframe():
    """Test the error case when the input data frame is empty"""
    empty_mock_df = pd.DataFrame()
    with pytest.raises(ValueError, match="The input DataFrame is empty."):
        split_clean_dataset(df=empty_mock_df, target_variable='target', test_size=0.3, random_state=552)

def test_missing_target(mock_dataframe):
    """Test the error case when target variable is missing from the input dataFrame"""
    with pytest.raises(ValueError, match="'target' is not found in the data frame."):
        split_clean_dataset(df=mock_dataframe.drop(columns=['target']), target_variable='target', test_size=0.3, random_state=552)

def test_incorrect_split_size(mock_dataframe):
    """Test the error case when test_size is invalid."""
    with pytest.raises(TypeError):
        split_clean_dataset(df=mock_dataframe, target_variable='target', test_size="wrong_input", random_state=552)

# Test: Edge cases
def test_dataframe_with_one_row():
    """ Test the edge case when the input dataset only has one row, cannot stratify"""
    one_row_df = pd.DataFrame({
        "col1": [1],
        "col2": [2],
        "target": ["one"]
    })
    with pytest.raises(ValueError):
        split_clean_dataset(df=one_row_df, target_variable='target', test_size=0.3, random_state=552)

def test_large_split_size(mock_dataframe):
    """Test the edge case when test_size is over 1."""
    with pytest.raises(ValueError):
        split_clean_dataset(df=mock_dataframe, target_variable='target', test_size=1.5, random_state=552)