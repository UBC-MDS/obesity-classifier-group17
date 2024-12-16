# split_n_preprocessor.py
# author: Yun Zhou, Sepehr Heydarian
# date: 2024-12-15

import click
import os
import sys
import pickle
import pandas as pd
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.split_clean_dataset import split_clean_dataset

warnings.filterwarnings("ignore")
@click.command()
@click.option('--clean-data', type=str, help="Path to the data after cleaning")
@click.option('--data-to', type=str, help="Path to directory where splitted data will be written to")
@click.option('--preprocessor-to', type=str, help="Path to directory where the preprocessor object will be written to")
@click.option('--seed', type=int, help="seed for random state", default=522)
@click.option('--html-to', type=str, help="Directory to save the correlation check result(html)", required=True)
def main(clean_data, data_to, preprocessor_to, seed, html_to):
    '''This script splits the data after cleaning for training and testing.
    EDA will be performed on training data set.
    The preprocessor will be applied for model training.'''

    # Set random state
    seed_random_state = seed

    # Input data and split using split_clean_dataset function from src folder
    merged_df = pd.read_csv(clean_data)

    train_df, test_df, X, y_train = split_clean_dataset(df=merged_df, target_variable="obesity_level", test_size=0.3, random_state=seed_random_state)

    # 10. No anomalous correlations between target/response variable and features/explanatory variables
    # Code adapted from deepchecks <Feature Label Correlation>
    # https://docs.deepchecks.com/stable/tabular/auto_checks/data_integrity/plot_feature_label_correlation.html
    ds = Dataset(train_df, 
                label='obesity_level', 
                cat_features=['gender',                     
                            'family_history_with_overweight',
                            'frequent_high_calorie_intake',
                            'food_intake_between_meals',
                            'smoker',
                            'monitor_calories',
                            'frequent_alcohol_intake', 
                            'mode_of_transportation'])

    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.9)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset=ds)
    #check_feat_lab_corr_result.show()
    if not check_feat_lab_corr_result.passed_conditions():
        raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")
    # Save the feature-label correlation result as an HTML file
    os.makedirs(html_to, exist_ok=True)
    feature_label_corr_html_path = os.path.join(html_to, "feature_label_correlation.html")
    if os.path.exists(feature_label_corr_html_path):
        os.remove(feature_label_corr_html_path)
    check_feat_lab_corr_result.save_as_html(feature_label_corr_html_path)
    
    # 11. No anomalous correlations between features/explanatory variables1
    # Code adapted from deepchecks <Feature Feature Correlation>
    # https://docs.deepchecks.com/stable/tabular/auto_checks/data_integrity/plot_feature_feature_correlation.html
    check_feat_feat_corr = FeatureFeatureCorrelation(threshold=0.8)
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset=ds)
    #check_feat_feat_corr_result.show()
    if not check_feat_feat_corr_result.passed_conditions():
        raise ValueError("Feature-Feature correlation exceeds the maximum acceptable threshold.")
    os.makedirs(html_to, exist_ok=True)
    feature_feature_corr_html_path = os.path.join(html_to, "feature_feature_correlation.html")
    if os.path.exists(feature_feature_corr_html_path):
        os.remove(feature_feature_corr_html_path)
    check_feat_feat_corr_result.save_as_html(feature_feature_corr_html_path)

    # Store splitted data
    train_df.to_csv(os.path.join(data_to, "obesity_train.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "obesity_test.csv"), index=False)

    # Encode target variable
    label_encoder = LabelEncoder()
    label_encoder.fit(y_train)

    train_df['obesity_level'] = label_encoder.transform(train_df['obesity_level'])
    test_df['obesity_level'] = label_encoder.transform(test_df['obesity_level'])

    train_df.to_csv(os.path.join(data_to, "obesity_train_target_encoding.csv"), index=False)
    test_df.to_csv(os.path.join(data_to, "obesity_test_target_encoding.csv"), index=False)

    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns
    numerical_cols = X.select_dtypes(include=['float64']).columns

    # Preprocessing for numeric and categorical data
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # Create directory if not existing
    if not os.path.isdir(preprocessor_to):
        os.makedirs(preprocessor_to)

    pickle.dump(preprocessor, open(os.path.join(preprocessor_to, "obesity_preprocessor.pickle"), "wb"))

if __name__ == '__main__':
    main()