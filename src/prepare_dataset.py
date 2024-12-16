
import pandas as pd


def prepare_dataset(result):
    """
    Prepares a combined dataset by merging features and target variables from
             the uci result object.

    Parameters:
    ----------
    result (object): uci result object.

    Raises:
        ValueError if data object or its attributes are not available.

    Returns:
    ----------
    merged_df: A combined DataFrame containing the feature columns and
                    target variable(s) side by side.
    """

    if not result.data:
        raise ValueError("Data is not available.")

    if result.data.features.empty:
        raise ValueError("Features is not available.")

    if result.data.targets.empty:
        raise ValueError("Targets is not available.")

    features = result.data.features
    target = result.data.targets
    merged_df = pd.concat([features, target], axis=1)
    return merged_df
