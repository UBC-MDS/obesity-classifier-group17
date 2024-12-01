# Obesity Level Predictor

- author: Yun Zhou, Zanan Pech and Sepehr Heydarian

Milestone 2 for DSCI 522 data workflows project

## About

In this project we attempt to build a model to classify different levels of obesity. The obesity levels are categorized as Insufficient Weight, Normal Weight, Overweight Level I, Overweight Level II, Obesity Type I, Obesity Type II, and Obesity Type III. We trained and evaluated three machine learning models - K-Nearest Neighbors (KNN), Support Vector Machine (SVM), and Decision Tree enhanced with AdaBoost. Our evaluation showed that SVM and the Decision Tree with AdaBoost achieved high predictive accuracy of ~97%. Although the accuracy of our KNN model is ~88%. These high scores reflect on the quality of data and analysis. With these promising scores, this model could potentially act as a useful tool in the healthcare industry to better help patients and healthcare professionals. 

The dataset used is obtained from UC Irvine Machine Learning Repository - [Link here](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition). This dataset was used in work by Fabio Mendoza Palechor and  Alexis de la Hoz Manotas (Palechor, F. M., & De La Hoz Manotas, A., 2019). Find work [here](https://doi.org/10.1016/j.dib.2019.104344).The dataset contains 2111 observations with 16 features (and one target - obesity level) from individuals from Mexico, Peru, and Colombia (Estimation of Obesity Levels Based On Eating Habits and Physical Condition, 2019). This dataset contains 24 duplicate rows which were dropped after data validation process. 

## Report

The final report can be found [here](https://github.com/UBC-MDS/obesity-classifier-group17/tree/main/notebooks)

## Usage

Ensure Docker is installed - [Install from here](https://www.docker.com/)

Clone the main branch of this repository: [Repository link](https://github.com/UBC-MDS/obesity-classifier-group17)

```bash
git clone https://github.com/UBC-MDS/obesity-classifier-group17
```

Once in the root directory of repository in local run the following command in terminal to open container. 

```bash
docker compose up
```
From the output of the above command in the terminal find the link to the container. See [image](https://github.com/UBC-MDS/obesity-classifier-group17/blob/main/img/container-weblaunch-url.png) as reference to find the url.

Open URL and once in Jupyter Lab under the "Kernel" menu click "Restart Kernel and Run All Cells...".

For further work on the environment and updating dependencies use `environment.yml` file (found [here](https://github.com/UBC-MDS/obesity-classifier-group17/blob/main/environment.yml). Once file is updated with new dependencies run:
```bash
conda-lock -k explicit --file environment.yml -p linux-64
```
Push changes to main and on Github Actions > Publish Docker Image run the workflow. Find docker tag in new published image and update the `docker-compose.yml`.

## Dependencies

[Docker](https://www.docker.com/)


## License
The Obesity Level Predictor project report is licensed under [Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). For additional information visit license link. Follow guidelines when sharing this report highlighted in the license file when using and sharing this work,

## References

Palechor, F. M., & De La Hoz Manotas, A. (2019). Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico. Data in Brief, 25, 104344. Retrieved from https://doi.org/10.1016/j.dib.2019.104344

Estimation of Obesity Levels Based On Eating Habits and Physical Condition. (2019). UCI Machine Learning Repository. Retrieved from https://doi.org/10.24432/C5H31Z.
