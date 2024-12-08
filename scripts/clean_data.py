# Code template below is adapted from work by Tiffany A. Timbers in breast-cancer-predictor repository
# https://github.com/ttimbers/breast-cancer-predictor/blob/main/scripts/split_n_preprocess.py
# download_data.py
# author: Zanan Pech, Yun Zhou
# date: 2024-12-04

import click
import os
import sys
import numpy as np
import pandas as pd
import warnings
import altair as alt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_data import validate_data
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import FeatureLabelCorrelation
from deepchecks.tabular.checks.data_integrity import FeatureFeatureCorrelation

warnings.filterwarnings("ignore")

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--name', type=str, help="name of processed the file")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--plot-to', type=str, help="Directory to save the data validation plot", required=True)
@click.option('--html-to', type=str, help="Directory to save the correlation check result(html)", required=True)
def main(raw_data, name, data_to, plot_to, html_to):

    '''This script checks the number of rows and columns of the data frame against the documentation.
    It checks whether type is Panda data frame and that the column names match the documentation.
    Additionally the column names are changes to a more interpretable name.
    Then it validates the data based on the function from validate_data.py file, 
    drop duplicates/invalid rows and check.
    Afterwards, it checks target distributions, target feature correlation, feature feature correlation.
    The cleaned data is saved in a directory path.
    '''
    
    merged_df = pd.read_csv(raw_data, index_col=0)
    # 1. Check correct data file format
    # The number of instances and features are retrieved from the dataset information in the documentation linked below
    # https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition
    # Check if number of instances are the same as documentation 
    assert merged_df.shape[0] == 2111, "merged_df does not have number of instances mentioned in the documentation"
    # check if number of features are the same as documentation (17 including the target)
    assert merged_df.shape[1] == 17, "merged_df does not have number of features mentioned in the documentation"
    # check if DataFrame is correct type
    assert isinstance(merged_df, pd.DataFrame), "merged_df is not a pandas DataFrame" 
    # Create variable with features listed in the documentation cited in cell above 
    original_column_names = ['Gender', 'Age', 'Height', 'Weight', 'family_history_with_overweight',
        'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE',
        'CALC', 'MTRANS', 'NObeyesdad']
    # 2. Check columns names (Data Validation)
    assert sorted(original_column_names) == sorted(merged_df.columns), "merged_df does not have the same column names as original_column_names"
    # Rename columns into meaningful names
    rename_dict = {
        'Gender': 'gender',
        'Age': 'age',
        'Height': 'height',
        'Weight': 'weight',
        'FAVC': 'frequent_high_calorie_intake',
        'FCVC': 'vegetable_intake_in_meals',
        'NCP': 'meals_per_day',
        'CAEC': 'food_intake_between_meals',
        'SMOKE': 'smoker',
        'CH2O': 'daily_water_intake',
        'SCC': 'monitor_calories',
        'FAF': 'days_per_week_with_physical_activity',
        'TUE': 'daily_screen_time',
        'CALC': 'frequent_alcohol_intake',
        'MTRANS': 'mode_of_transportation',
        'NObeyesdad': 'obesity_level'
    }
    merged_df = merged_df.rename(columns = rename_dict) 
    # validate_data() is imported from validate_data.py in src folder
    validate_data(merged_df)
    # Check Dimensions after dropping dulicates
    merged_df = merged_df.drop_duplicates().dropna(how="all")
    merged_df.shape
    assert merged_df.shape[0] == 2087, "merged_df does not have correct number of instances after dropping the duplicates"
    assert merged_df.shape[1] == 17, "merged_df does not have correct number of features after dropping the duplicates"

    # 9. Target/response variable follows expected distribution
    # Use Altair for visualization
    actual_counts = merged_df['obesity_level'].value_counts().reset_index()
    actual_counts.columns = ['obesity_level', 'count']
    expect_counts = merged_df.shape[0] / merged_df['obesity_level'].nunique()
    actual_counts['expected'] = expect_counts
    # Add threshold +/-60
    actual_counts['expected_lower'] = actual_counts['expected'] - 60
    actual_counts['expected_upper'] = actual_counts['expected'] + 60
    actual_dist = alt.Chart(actual_counts).mark_bar(color='steelblue', opacity=0.6).encode(
        x=alt.X('obesity_level:N', title='Obesity Level'),
        y=alt.Y('count:Q', title='Count'),
        tooltip=['obesity_level', 'count']
    )
    expected_dist = alt.Chart(actual_counts).mark_bar(color='orange', opacity=0.3).encode(
        x=alt.X('obesity_level:N', title='Obesity Level'),
        y=alt.Y('expected:Q'),
        tooltip=['obesity_level', 'expected']
    )
    error_bar = alt.Chart(actual_counts).mark_errorbar(color='black').encode(
        x=alt.X('obesity_level:N'),
        y=alt.Y('expected_lower:Q', title='Error Bar'),
        y2='expected_upper:Q'
    )
    ticks = alt.Chart(actual_counts).mark_tick(
        color='black',
        thickness=2,
        size=20  
    ).encode(
        x=alt.X('obesity_level:N'),
        y=alt.Y('expected_lower:Q')  
    ) + alt.Chart(actual_counts).mark_tick(
        color='black',
        thickness=2,
        size=20  
    ).encode(
        x=alt.X('obesity_level:N'),
        y=alt.Y('expected_upper:Q')  
    )
    target_dist = alt.layer(
        expected_dist, actual_dist, error_bar, ticks
    ).properties(
        title='Target Variable vs Expected Distribution',
        width=400,
        height=300
    )
    legend_data = pd.DataFrame({
        'Category': ['Actual', 'Expected'],
        'Color': ['steelblue', 'orange']
    })
    manual_legend = alt.Chart(legend_data).mark_rect().encode(
        y=alt.Y('Category:N', axis=alt.Axis(title='Legend')),
        color=alt.Color('Color:N', scale=None)
    ).properties(
        width=20,
        height=100
    ) + alt.Chart(legend_data).mark_text(align='left', dx=25).encode(
        y=alt.Y('Category:N')
    )
    final_dist = alt.hconcat(target_dist, manual_legend).resolve_legend(color="independent")
    os.makedirs(plot_to, exist_ok=True)
    final_dist.save(os.path.join(plot_to, "Data_vali_targ_varib_dist.png"), scale_factor=1.5)

    #warnings.filterwarnings("ignore", category=FutureWarning)
    # 10. No anomalous correlations between target/response variable and features/explanatory variables
    # Code adapted from deepchecks <Feature Label Correlation>
    # https://docs.deepchecks.com/stable/tabular/auto_checks/data_integrity/plot_feature_label_correlation.html
    ds = Dataset(merged_df, 
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
    
    merged_df_cleaned = merged_df.drop_duplicates().dropna(how="all")
    # Check if the directory exists, else create one.
    os.makedirs(data_to, exist_ok=True)
    merged_df_cleaned.to_csv(f'{data_to}/{name}')

if __name__ == '__main__':
    main()
