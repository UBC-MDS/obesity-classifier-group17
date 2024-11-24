# Obesity Level Predictor

- author: Yun Zhou, Zanan Pech and Sepehr Heydarian

Milestone 1 for DSCI 522 data workflows project

## About

In this project we attempt to build a model to classify different levels of obesity. We trained and evaluated three machine learning models - K-Nearest Neighbors (KNN), Support Vector Machine (SVM), and Decision Tree enhanced with AdaBoost. Our evaluation showed that SVM and the Decision Tree with AdaBoost achieved high predictive accuracy of ~97%.

This dataset include data for the estimation of obesity levels in individuals from the countries of Mexico, Peru and Colombia, based on their eating habits and physical condition. The data contains 17 attributes and 2111 records, the records are labeled with the class variable NObesity (Obesity Level), that allows classification of the data using the values of Insufficient Weight, Normal Weight, Overweight Level I, Overweight Level II, Obesity Type I, Obesity Type II and Obesity Type III. 77% of the data was generated synthetically using the Weka tool and the SMOTE filter, 23% of the data was collected directly from users through a web platform.

## Report

The final report can be found [here] (https://github.com/UBC-MDS/obesity-classifier-group17/tree/main/notebooks)

## Usage

Run the following for initial contribution to the project (environment found in root repository):

```bash
conda-lock install --name obesity_classifier_group17 conda-lock.yml
```

Run the following for analysis:

```bash
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

The Obesity Classification Project report contained herein is licensed under the Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0) license. See the license file for more information. If re-using or sharing this report, please provide attribution and link to this repository. The software code contained within this repository is licensed under the MIT license. See the license file for more information.

## References

Dua, Dheeru, and Casey Graff. 2017. “UCI Machine Learning Repository.” University of California, Irvine, School of Information; Computer Sciences. http://archive.ics.uci.edu/ml.

Estimation of Obesity Levels Based On Eating Habits and Physical Condition [Dataset]. (2019). UCI Machine Learning Repository. https://doi.org/10.24432/C5H31Z.
