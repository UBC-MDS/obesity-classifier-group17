# Code template below is adapted from work by Tiffany A. Timbers in breast-cancer-predictor repository:
# https://github.com/ttimbers/breast-cancer-predictor/blob/3.0.0/tests/test_write_csv.py

import numpy as np
import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data


data = [{"gender":"Female","age":21.0,"height":1.62,"weight":64.0,"family_history_with_overweight":"yes","FAVC":"no","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":0.0,"TUE":1.0,"CALC":"no","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Female","age":21.0,"height":1.52,"weight":56.0,"family_history_with_overweight":"yes","FAVC":"no","FCVC":3.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"yes","CH2O":3.0,"SCC":"yes","FAF":3.0,"TUE":0.0,"CALC":"Sometimes","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Male","age":-1,"height":1.8,"weight":77.0,"family_history_with_overweight":"yes","FAVC":"no","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":2.0,"TUE":1.0,"CALC":"Frequently","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Male","age":27.0,"height":1.8,"weight":87.0,"family_history_with_overweight":"no","FAVC":"no","FCVC":3.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":2.0,"TUE":0.0,"CALC":"Frequently","MTRANS":"Walking","obesity_level":"Overweight_Level_I"},
        {"gender":"Male","age":20.0,"height":1.78,"weight":89.8,"family_history_with_overweight":"no","FAVC":"no","FCVC":2.0,"NCP":1.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":0.0,"TUE":0.0,"CALC":"Sometimes","MTRANS":"Public_Transportation","obesity_level":"Overweight_Level_II"},
        {"gender":"Male","age":29.0,"height":1.62,"weight":np.nan,"family_history_with_overweight":"no","FAVC":"yes","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":0.0,"TUE":0.0,"CALC":"Sometimes","MTRANS":"Automobile","obesity_level":"Normal_Weight"},
        {"gender":"Female","age":23.0,"height":1.5,"weight":55.0,"family_history_with_overweight":"yes","FAVC":"yes","FCVC":3.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":1.0,"TUE":np.nan,"CALC":"Sometimes","MTRANS":"Motorbike","obesity_level":"Normal_Weight"},
        {"gender":"Male","age":22.0,"height":1.64,"weight":53.0,"family_history_with_overweight":"no","FAVC":"no","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":3.0,"TUE":0.0,"CALC":"Sometimes","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Male","age":24.0,"height":1.78,"weight":64.0,"family_history_with_overweight":"yes","FAVC":"yes","FCVC":3.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":1.0,"TUE":1.0,"CALC":"Frequently","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Male","age":22.0,"height":1.72,"weight":68.0,"family_history_with_overweight":"yes","FAVC":"yes","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":1.0,"TUE":1.0,"CALC":"no","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"},
        {"gender":"Female","age":21.0,"height":1.62,"weight":64.0,"family_history_with_overweight":"yes","FAVC":"no","FCVC":2.0,"NCP":3.0,"CAEC":"Sometimes","smoke":"no","CH2O":2.0,"SCC":"no","FAF":0.0,"TUE":1.0,"CALC":"no","MTRANS":"Public_Transportation","obesity_level":"Normal_Weight"}]



@pytest.fixture
def mock_dataframe():
    """Create a mock dataframe using above data."""
    mock_df = pd.DataFrame(data)
    return mock_df


def test_validate_data_success(mock_dataframe):
    """Test when validation passes."""
    assert validate_data(mock_dataframe) is None


def test_validate_data_invalid_input_type():
    """Test the raised exception when the input type is invalid."""
    with pytest.raises(ValueError, match="The input object type is not Dataframe."):
        validate_data(1)


def test_validate_data_empty_dataframe():
    """Test the raised exception when the input dataframe is empty"""
    with pytest.raises(ValueError, match="The input Dataframe is empty."):
        validate_data(pd.DataFrame())

