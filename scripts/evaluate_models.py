# evaluate_models.py
# Author: Yun Zhou
# Date: 2024-12-6

import os
import pickle
import pandas as pd
import altair as alt
from sklearn.metrics import accuracy_score, precision_score, recall_score
import click

@click.command()
@click.option('--test-data', type=str, help="Path to testing data", required=True)
@click.option('--pipeline-path', type=str, help="Path to the trained pipeline pickle file", required=True)
@click.option('--data-to', type=str, help="Directory to save the evaluation results", required=True)
@click.option('--plot-to', type=str, help="Directory to save the evaluation viz", required=True)
def main(test_data, pipeline_path, data_to, plot_to):
    """
    This script evaluates trained models using a test dataset and visualizes the performance of each model.
    """
    # Load test data
    test_df = pd.read_csv(test_data)
    # Load trained pipelines
    with open(pipeline_path, 'rb') as f:
        trained_pipelines = pickle.load(f)
    # Evaluate models on the test set
    test_results = []
    for name, pipeline in trained_pipelines.items():
        y_pred = pipeline.predict(test_df.drop('obesity_level', axis=1))
        # Evaluate performance
        accuracy = accuracy_score(test_df['obesity_level'], y_pred)
        precision = precision_score(test_df['obesity_level'], y_pred, average=None)  # Per class
        recall = recall_score(test_df['obesity_level'], y_pred, average=None)  # Per class
        # Calculate average Precision and Recall
        avg_precision = precision.mean()
        avg_recall = recall.mean()
        # Save the metrics
        test_results.append({
            "Model": name,
            "Accuracy": accuracy,
            "Average Level Precision": avg_precision,
            "Average Level Recall": avg_recall
        })
    
    # Convert test_results to a DataFrame
    test_results_df = pd.DataFrame(test_results)

    # Save results to CSV
    os.makedirs(data_to, exist_ok=True)
    results_csv_path = os.path.join(data_to, "test_results.csv")
    test_results_df.to_csv(results_csv_path, index=False)

    # Visualization of model performance (optional)
    results_data = pd.DataFrame({
        'Model': test_results_df['Model'],
        'Accuracy': test_results_df['Accuracy']
    })
    # Create bar chart for comparison
    bar_chart = alt.Chart(results_data).mark_bar().encode(
        x=alt.X('Model:N', title='Model', sort=None, axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Accuracy:Q', title='Accuracy', scale=alt.Scale(domain=[0, 1])),
        tooltip=['Model', 'Accuracy']
    )
    # Add text labels
    text = bar_chart.mark_text(
        align='center',
        baseline='middle',
        dy=-10,  
        fontSize=12
    ).encode(
        text=alt.Text('Accuracy:Q', format='.2f')  
    )
    # Combine the bar chart with the text labels
    final_chart_with_text = (bar_chart + text).properties(
        title='Figure 5. Model Performance Comparison',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16
    ).configure_mark(
        color='skyblue'
    )

    # Save chart as png
    os.makedirs(plot_to, exist_ok=True)
    final_chart_with_text.save(os.path.join(plot_to, "Obesity_test.png"), scale_factor=1.5)

if __name__ == "__main__":
    main()