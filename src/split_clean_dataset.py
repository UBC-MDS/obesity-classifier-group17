# Below code attributed to:
#https://docs.python.org/3/library/exceptions.html
#https://docs.python.org/3/tutorial/errors.html

import pandas as pd
from sklearn.model_selection import train_test_split


def split_clean_dataset(df, target_variable, test_size=0.3, random_state=522):
    """
    Uses clean dataset and splits it into train and test sets and returns them as Pandas DataFrames.
    Also return X data frame, which contains all cleaned data except target column.
    y_train is also return as a series.

    Parameters:
    -----------
    df: pandas.DataFrame
        The input containing the wrangled dataset data frame.
    target_variable: str
        Name of the target column in the wrangled dataset.
    test_size: float:
        The size of the test set as a proportion of the wrangled dataset (default = 0.3).
    random_state: int, optional
        Seed for random state used for reproducibility (default=522).

    Returns:
    --------
    train_df: pandas.DataFrame
        The training split including all features and target variable.
    test_df: pandas.DataFrame
        The test split including all features and target variable.
    X: pandas.DataFrame
        The clean dataset with only explanatory features, no target variable.
    y_train: pandas.Series
        The target column of the training set.

    Raises:
    --------
    ValueError
        Raise error if the target column does not exist in the dataset
    Exception
        Raise error for other erroneous cases 
    """

    try:
        # Check if input df is a pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("The input is not a pandas DataFrame.")

        # Check if DataFrame is not empty
        if df.empty:
            raise ValueError("The input DataFrame is empty.")

        #check if target feature exists
        if target_variable not in df.columns:
            raise ValueError(f"'{target_variable}' is not found in the data frame.")
    
        X = df.drop(target_variable, axis=1)
        y = df[target_variable]

        # Split data into X and y train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Combine X and y sets into train and test data frames
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)

        return train_df, test_df, X, y_train
    
    except ValueError:
        raise
    except TypeError:
        raise
    except Exception as error:
        raise Exception(f"Error: {error}")