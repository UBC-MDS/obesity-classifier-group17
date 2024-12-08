# Obesity Level Predictor

- author: Yun Zhou, Zanan Pech and Sepehr Heydarian

Milestone 3 for DSCI 522 data workflows project

## About

In this project we attempt to build a model to classify different levels of obesity. From the dataset we utilized, the target variable is categorized as Insufficient Weight, Normal Weight, Overweight Level I, Overweight Level II, Obesity Type I, Obesity Type II, and Obesity Type III. We trained and evaluated three machine learning models - K-Nearest Neighbors (KNN), Support Vector Machine (SVM), and Decision Tree enhanced with AdaBoost. Our evaluation showed that SVM and the Decision Tree with AdaBoost achieved high predictive accuracy of 97.1% and 97.9% respectively. Although the accuracy of our KNN model was relatively lower at 88.0%. These scores were calcualted from evaluating unseen test data that were splitted prior to models being created. These high scores reflect on the quality of features within the dataset and the models ability to generalize well. With these promising scores, this model could potentially act as a useful tool in the healthcare industry to better help patients and healthcare professionals. 

The dataset used is obtained from UC Irvine Machine Learning Repository - [Link here](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition). This dataset was used in work by Fabio Mendoza Palechor and Alexis de la Hoz Manotas (Palechor, F. M., & De La Hoz Manotas, A., 2019). Find work [here](https://doi.org/10.1016/j.dib.2019.104344). The dataset contains 2111 observations with 16 features (and one target - obesity level) from individuals from Mexico, Peru, and Colombia (Estimation of Obesity Levels Based On Eating Habits and Physical Condition, 2019). This dataset contains 24 duplicate rows which were dropped after data validation process. Despite its limitations, this dataset was chosen as it offers a rich set of features which are relevant to obesity. However, its important to note that the data comes from only three countries, limiting its diversity to capture global trends, and a significant portion of the data was synthesized which may introduce some bias.

## Report

The final report can be found [here](https://github.com/UBC-MDS/obesity-classifier-group17/tree/main/report)

## Usage

Ensure Docker is installed and running - [Install from here](https://www.docker.com/)

Clone the main branch of this repository: [Repository link](https://github.com/UBC-MDS/obesity-classifier-group17)

```bash
git clone https://github.com/UBC-MDS/obesity-classifier-group17
```

Once in the root directory of repository in local run the following command in terminal to open container.

```bash
docker compose up
```

From the output of the above command in the terminal find the link to the container. See [image](https://github.com/UBC-MDS/obesity-classifier-group17/blob/main/img/container-weblaunch-url.png) as reference to find the url.

For further work on the environment and updating dependencies use `environment.yml` file (found [here](https://github.com/UBC-MDS/obesity-classifier-group17/blob/main/environment.yml).) Once file is updated with new dependencies run:

```bash
conda-lock -k explicit --file environment.yml -p linux-64
```

Push changes to main and on Github Actions > Publish Docker Image and run the workflow. Find docker tag in new published image and update the `docker-compose.yml`.

## Running the analysis using scripts

1. Open Terminal and set working directory to the root of the repository and run the following commands.

2. Download dataset

```
python scripts/download_data.py --write_to="data/raw" --name="ObesityDataSet_raw_data_sinthetic.csv"
```

3. Clean data and do validation

```
python scripts/clean_data.py --raw-data='data/raw/ObesityDataSet_raw_data_sinthetic.csv' --name='ObesityDataSet_processed_data.csv' --data-to="data/processed/" --plot-to="results/figures" --html-to="results/htmls"
```

4. Split and preprocess data

```
python scripts/split_n_preprocess.py --clean-data=data/processed/ObesityDataSet_processed_data.csv --data-to=data/processed --preprocessor-to=results/models --seed=522
```
5. Explanatory Data Analysis

```
python scripts/eda.py --training_data_split=data/processed/obesity_train.csv --plot_path=results/figures/
```

6. Fit the models

```
python scripts/fit_obesity_classifier.py --encoded-train-data=data/processed/obesity_train_target_encoding.csv --data-to=results/tables --preprocessor=results/models/obesity_preprocessor.pickle --seed=522 --pipeline-to=results/models
```

7. Evaluate the models

```
python scripts/evaluate_models.py --test-data=data/processed/obesity_test_target_encoding.csv --pipeline-path=results/models/trained_pipelines.pkl --data-to=results/tables --plot-to=results/figures
```

8. Render report files

```
quarto render report/obesity_level_predictor_report.qmd --to html
```

## Dependencies

[Docker](https://www.docker.com/)

## License

The Obesity Level Predictor project report is licensed under [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). For additional information visit license link. Follow guidelines highlighted in the license file when using and sharing this work.

## References

Palechor, F. M., & De La Hoz Manotas, A. (2019). Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico. Data in Brief, 25, 104344. Retrieved from https://doi.org/10.1016/j.dib.2019.104344

Estimation of Obesity Levels Based On Eating Habits and Physical Condition. (2019). UCI Machine Learning Repository. Retrieved from https://doi.org/10.24432/C5H31Z.
