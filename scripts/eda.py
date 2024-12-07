# eda.py
# author: Sepehr Heydarian
# date: 2024-12-05

import altair as alt
import os
import click
import pandas as pd


@click.command()
@click.option('--training_data_split', type=str, help="The path to the training dataset for exploratory data analysis")
@click.option('--plot_path', type=str, help="Path of directory where plots will be saved")

def main(training_data_split, plot_path):
    '''
    Plot findings from explanatory data analysis in the training dataset and save plot as figures.
    The following plots generated from EDA:
        1) Target variable distribution
        2) Heatmap for correlation between numeric features
        3) Distribution of continuous features for target classes
        4) Relationship of categorical features to target classes
    '''
    
    train_df = pd.read_csv(training_data_split)
    
    # Create directory if not existing
    if os.path.isdir(plot_path) is False:
        os.makedirs(plot_path)

    ## Plot 1: Target variable distribution
    target_distribution = alt.Chart(train_df).mark_bar().encode(
        x=alt.X('obesity_level:N', title='Obesity Level'),
        y=alt.Y('count():Q', title='Count'),
     color=alt.Color('obesity_level')
    ).properties(
     title='Figure 1. Distribution of Target: Obesity Level',
        width=400,
     height=300
    )

    target_distribution.save(os.path.join(plot_path, "target_distribution_plot.png"))

    ## Plot 2: Correlation between numeric features
    
    # Keep numeric features
    numeric_data = train_df.select_dtypes(include=['float64', 'int64'])
    # Calculate the correlation between features
    correlation_data = numeric_data.corr().reset_index().melt('index')

    # Plot heatmap
    correlation_chart = alt.Chart(correlation_data).mark_rect().encode(
        x=alt.X('variable:N', title='Features', axis=alt.Axis(labelAngle=45)),
        y=alt.Y('index:N', title='Features'),
        color=alt.Color(
            'value:Q',
            scale=alt.Scale(
                domain=[0, 1],  
                range=['#E6F7FF', '#0050B3']  
            ),
            title='Correlation'
        ),
     tooltip=['index', 'variable', 'value'] 
    ).properties(
        title='Figure 2. Numeric Feature Correlation Heatmap',
        width=400,
        height=400
    )

    correlation_chart.save(os.path.join(plot_path, "correlation_heatmap_chart.png"))

    ## Plot 3: Relationship between continuous features and target
    alt.data_transformers.enable('vegafusion')

    numeric_features_facet = alt.Chart(
        train_df.melt(id_vars=['obesity_level'], value_vars=numeric_data)
    ).mark_boxplot().encode(
        x=alt.X('obesity_level:N', title='Obesity Level'),
        y=alt.Y(
            'value:Q',
            title='Value',
            scale=alt.Scale(padding=5)  
        ),
        color=alt.Color('obesity_level'),
        facet=alt.Facet('variable:N', title='Features', columns=2)  
    ).properties(
        title='Figure 3. Distribution of Numeric Features by Obesity Level',
        width=200,
        height=200
    ).resolve_scale(
        y='independent'
    )

    numeric_features_facet.save(os.path.join(plot_path, "numeric_feature_distribution.png"))


    ## Plot 4: Relationship between categorical features and target

    # Select binary/categorical features (excluding numeric features)
    categorical_features = train_df.select_dtypes(exclude=['float64', 'int64']).columns.difference(['obesity_level'])

    # Create a list to store individual charts
    charts = []

    # Loop through each categorical feature
    for feature in categorical_features:
        # Create a bar chart for the current feature
        chart = alt.Chart(train_df).mark_bar().encode(
            x=alt.X(f"{feature}:N", title=feature, sort='-y'),  # Sort categories by count (descending)
            y=alt.Y('count():Q', title='Count'),
            color=alt.Color('obesity_level:N', title='Obesity Level'),
            order=alt.Order('count():Q', sort='descending')  # Sort stack order by count, ascending
        ).properties(
            title=f'{feature} by Obesity Level',
            width=200,
            height=200
        )
        charts.append(chart)

    # Arrange charts in rows of 2 columns
    rows = [alt.hconcat(*charts[i:i+2]) for i in range(0, len(charts), 2)]

    # Combine all rows into a vertical concatenation
    combined_chart = alt.vconcat(*rows).properties(
        title="Figure 4. Relationship between Categorical Features and Target"
    ).configure_title(
        fontSize=16,
        anchor='middle',  
        font='Arial'
    )   

    combined_chart.save(os.path.join(plot_path, "categorical_feat_target_relationship.png"))


if __name__ == '__main__':
    main()