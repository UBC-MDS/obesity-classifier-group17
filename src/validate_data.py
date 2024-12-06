# Code below is adapted from
# https://ubc-dsci.github.io/reproducible-and-trustworthy-workflows-for-data-science/lectures/130-data-validation.html
# validate_data.py
# author: Zanan Pech & Sepehr Heydarian
# date: 2024-12-06

import pandera as pa


def validate_data(obesity_df):

    """
    Validates the data from the raw obesity dataset by using pandera library to 
    create schemas.
    Following validations are performed:

    Check missingness not beyond expected threshold with "nullable"
    Check correct data types in each column with "first parameter in pa.Column"
    Check the outlier or anomalous values with "pa.Check.between"
    Check category levels with "pa.Check.isin"
    Check for duplicated observations 
    Check for empty observations 

    Parameters
    ----------
    obesity_df : pandas.DataFrame
        The raw data frame containing obesity levels data.

    Returns
    ----------
    pandas.DataFrame
        A validated data frame is returned with the necessary changes such as dropping duplicate rows.
        These changes do not pertain to the inputted data frame.
    
    Raises
    ----------
    pandera.errors.SchemaError
        Error is raised if one of the checks is failed.
    """
    
    schema = pa.DataFrameSchema({
        "gender": pa.Column(str, pa.Check.isin(["Female", "Male"])),
        "age": pa.Column(float, pa.Check.between(10, 99), nullable=True),
        "height": pa.Column(float, pa.Check.between(1.0, 2.5), nullable=True),
        "weight": pa.Column(float, pa.Check.between(30, 200), nullable=True),
        "family_history_with_overweight": pa.Column(str, pa.Check.isin(["yes", "no"])),
        "frequent_high_calorie_intake": pa.Column(str, pa.Check.isin(["yes", "no"])),
        "vegetable_intake_in_meals": pa.Column(float, pa.Check.between(1.0, 3.0), nullable=True),
        "meals_per_day": pa.Column(float, pa.Check.between(0.0, 10.0), nullable=True),
        "food_intake_between_meals": pa.Column(str, pa.Check.isin(['Sometimes', 'Frequently', 'Always', 'no'])),
        "smoker": pa.Column(str, pa.Check.isin(['no', 'yes'])),
        "daily_water_intake": pa.Column(float, pa.Check.between(0.0, 5.0), nullable=True),
        "monitor_calories": pa.Column(str, pa.Check.isin(["yes", "no"])),
        "days_per_week_with_physical_activity": pa.Column(float, pa.Check.between(0.0, 7.0), nullable=True),
        "daily_screen_time": pa.Column(float, pa.Check.between(0.0, 24.0), nullable=True),
        "frequent_alcohol_intake": pa.Column(str, pa.Check.isin(['no', 'Sometimes', 'Frequently', 'Always'])),
        "mode_of_transportation": pa.Column(str, pa.Check.isin(['Public_Transportation', 'Walking', 'Automobile', 'Motorbike',
        'Bike'])),
        "obesity_level": pa.Column(str, pa.Check.isin(['Normal_Weight', 'Overweight_Level_I', 'Overweight_Level_II',
        'Obesity_Type_I', 'Insufficient_Weight', 'Obesity_Type_II','Obesity_Type_III'])), 
        },
                   
        checks=[
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ],

        drop_invalid_rows=True
    )

    schema.validate(obesity_df, lazy=True).drop_duplicates().dropna(how="all")