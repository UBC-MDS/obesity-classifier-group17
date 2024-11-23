# Obesity Level Predictor

  - author: Yun Zhou, Zanan Pech and Sepehr Heydarian

  Milestone 1 for DSCI 522 data workflows project


## About

In this project we attempt to build a model to classify different levels of obesity. We trained and evaluated three machine learning models - K-Nearest Neighbors (KNN), Support Vector Machine (SVM), and Decision Tree enhanced with AdaBoost. Our evaluation showed that SVM and the Decision Tree with AdaBoost achieved high predictive accuracy of ~97%.  

## Report

The final report can be found [here] (https://github.com/UBC-MDS/obesity-classifier-group17/tree/main/notebooks)

## Usage

Run the following for initial contribution to the project (environment found in root repository):

``` bash
conda-lock install --name obesity_classifier_group17 conda-lock.yml
```

Run the following for analysis:

``` bash
jupyter lab 
```

Open `notebooks/obesity_level_predictor_report.ipynb` in Jupyter Lab
and under Switch/Select Kernel choose 
"Python [conda env:obesity_classifier_group17]".

Next, under the "Kernel" menu click "Restart Kernel and Run All Cells...".

## Dependencies

  - `jupyterlab` >=3.5
  - `matplotlib`=3.9.2
  - `pandas`=2.1.2
  - `altair`=5.1.2
  - `ipykernel`=6.26.0
  - `notebook`=6.5.4
  - `pandas`=2.1.2
  - `python`=3.11
  - `requests`=2.31.0
  - `scikit-learn`=1.5.1
  - `conda-lock`
  - `numpy`=1.26.0
  - `pip`>=24.2
  - `vegafusion-python-embed`=1.4.3
  - `vegafusion`=1.4.3
  - `vl-convert-python`=1.0.1
  - Python and packages listed in [`environment.yml`](environment.yml)

  ## License

  ## References

