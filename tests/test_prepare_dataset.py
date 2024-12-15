import numpy as np
import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.prepare_dataset import prepare_dataset


class MockData:

    def __init__(self, data):
        self.features = pd.DataFrame(data).drop('NObeyesdad', axis=1)
        self.targets = pd.DataFrame(data)[['NObeyesdad']]


class MockUCIDataSet:

    def __init__(self, data):
        self.data = [] if not data else MockData(data)

data = [
            {"Gender": "Female", "Age": 21.0, "Height": 1.62, "Weight": 64.0, "family_history_with_overweight": "yes", "FAVC": "no", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 0.0, "TUE": 1.0, "CALC": "no", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Female", "Age": 21.0, "Height": 1.52, "Weight": 56.0, "family_history_with_overweight": "yes", "FAVC": "no", "FCVC": 3.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "yes", "CH2O": 3.0, "SCC": "yes", "FAF": 3.0, "TUE": 0.0, "CALC": "Sometimes", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Male", "Age": 23.0, "Height": 1.8, "Weight": 77.0, "family_history_with_overweight": "yes", "FAVC": "no", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 2.0, "TUE": 1.0, "CALC": "Frequently", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Male", "Age": 27.0, "Height": 1.8, "Weight": 87.0, "family_history_with_overweight": "no", "FAVC": "no", "FCVC": 3.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 2.0, "TUE": 0.0, "CALC": "Frequently", "MTRANS": "Walking", "NObeyesdad": "Overweight_Level_I"},
            {"Gender": "Male", "Age": np.nan, "Height": 1.78, "Weight": 89.8, "family_history_with_overweight": "no", "FAVC": "no", "FCVC": 2.0, "NCP": 1.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 0.0, "TUE": 0.0, "CALC": "Sometimes", "MTRANS": "Public_Transportation", "NObeyesdad": "Overweight_Level_II"},
            {"Gender": "Male", "Age": 29.0, "Height": 1.62, "Weight": np.nan, "family_history_with_overweight": "no", "FAVC": "yes", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 0.0, "TUE": 0.0, "CALC": "Sometimes", "MTRANS": "Automobile", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Female", "Age": 23.0, "Height": 1.5, "Weight": 55.0, "family_history_with_overweight": "yes", "FAVC": "yes", "FCVC": 3.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 1.0, "TUE": np.nan, "CALC": "Sometimes", "MTRANS": "Motorbike", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Male", "Age": 22.0, "Height": 1.64, "Weight": 53.0, "family_history_with_overweight": "no", "FAVC": "no", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 3.0, "TUE": 0.0, "CALC": "Sometimes", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Male", "Age": 24.0, "Height": 1.78, "Weight": 64.0, "family_history_with_overweight": "yes", "FAVC": "yes", "FCVC": 3.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 1.0, "TUE": 1.0, "CALC": "Frequently", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Male", "Age": 22.0, "Height": 1.72, "Weight": 68.0, "family_history_with_overweight": "yes", "FAVC": "yes", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 1.0, "TUE": 1.0, "CALC": "no", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"},
            {"Gender": "Female", "Age": 21.0, "Height": 1.62, "Weight": 64.0, "family_history_with_overweight": "yes", "FAVC": "no", "FCVC": 2.0, "NCP": 3.0, "CAEC": "Sometimes", "SMOKE": "no", "CH2O": 2.0, "SCC": "no", "FAF": 0.0, "TUE": 1.0, "CALC": "no", "MTRANS": "Public_Transportation", "NObeyesdad": "Normal_Weight"}, # Duplicate row
        ]


def test_prepare_dataset_success():
    mock_dataset = MockUCIDataSet(data)
    assert isinstance(prepare_dataset(mock_dataset), pd.DataFrame)
    assert prepare_dataset(mock_dataset).shape[1] == mock_dataset.data.features.shape[1] + mock_dataset.data.targets.shape[1]


def test_prepare_dataset_empty():
    mock_dataset = MockUCIDataSet([])
    with pytest.raises(ValueError, match="Data is not available."):
        prepare_dataset(mock_dataset)


def test_prepare_dataset_edge_case():
    mock_dataset = MockUCIDataSet(data)
    assert prepare_dataset(mock_dataset).shape[0] != prepare_dataset(mock_dataset).dropna().shape[0]
    assert prepare_dataset(mock_dataset).shape[0] != prepare_dataset(mock_dataset).drop_duplicates().shape[0]
