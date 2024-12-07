# obesity_classifier.py
# author: Yun Zhou
# date: 2024-12-6

import click
import os
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import GridSearchCV


@click.command()
@click.option('--encoded-train-data', type=str, help="Path to training data, with encoded target")
@click.option('--data-to', type=str, help="Path to directory where training scores will be written to")
@click.option('--preprocessor', type=str, help="Path to directory where the preprocessor object locates")
@click.option('--seed', type=int, help="seed for random state", default=522)
@click.option('--pipeline-to', type=str, help="Path to directory where the pipeline object will be written to")
def main(encoded_train_data, data_to, preprocessor, seed, pipeline_to):
    '''This script splits the data after cleaning for training and testing.
    EDA will be performed on training data set.
    The preprocessor will be applied for model training.'''

    # Set random state
    seed_random_state = seed
    # Input data
    train_df = pd.read_csv(encoded_train_data)
    with open(preprocessor, 'rb') as f:
        preprocessor_obj = pickle.load(f)
    # Models to evaluate
    models = {
        'KNN': KNeighborsClassifier(),
        'SVM (RBF Kernel)': SVC(kernel='rbf', random_state=seed_random_state),
        'AdaBoost + Decision Tree': AdaBoostClassifier(
            estimator=DecisionTreeClassifier(max_depth=5, random_state=seed_random_state), 
            n_estimators=50,  
            learning_rate=0.5,
            algorithm="SAMME",
            random_state=seed_random_state
        )
    }
    
    # Code adapted from DSCI 571 Lecture 4
# https://pages.github.ubc.ca/MDS-2024-25/DSCI_571_sup-learn-1_students/lectures/notes/04_preprocessing-pipelines-column-transformer.html
    def mean_std_cross_val_scores(model, X_train, y_train, **kwargs):
        """
        Returns mean and std of cross validation
        Parameters
        ----------
        model :
            scikit-learn model
        X_train : numpy array or pandas DataFrame
            X in the training data
        y_train :
            y in the training data
        Returns
        ----------
            pandas Series with mean scores from cross_validation
        """
        scores = cross_validate(model, X_train, y_train, return_train_score=True, **kwargs)
        mean_scores = pd.DataFrame(scores).mean()
        std_scores = pd.DataFrame(scores).std()
        out_col = []
        for i in range(len(mean_scores)):
            out_col.append((f"%0.3f (+/- %0.3f)" % (mean_scores.iloc[i], std_scores.iloc[i])))
        return pd.Series(data=out_col, index=mean_scores.index)
    
    warnings.filterwarnings("ignore", category=UserWarning, module="sklearn.preprocessing")
    # Evaluate models with detailed cross-validation results
    results = {}
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor_obj), ('classifier', model)])
        results[name] = mean_std_cross_val_scores(
            pipeline, 
            train_df.drop('obesity_level', axis=1), 
            train_df['obesity_level'], 
            cv=5, 
            scoring='accuracy'
        )
    # Combine results into a DataFrame for comparison
    cv_results_df = pd.DataFrame(results)
    # Output the results
    if not os.path.isdir(data_to):
        os.makedirs(data_to)
    cv_results_df.to_csv(os.path.join(data_to, "cross_validation_scores.csv"), index=False)

    # Hyper Parameter Optimization
    param_grids = {
        'KNN': {
            'n_neighbors': [3, 5, 7, 9],  
            'weights': ['uniform', 'distance'],  
            'metric': ['euclidean', 'manhattan']  
        },
        'SVM (RBF Kernel)': {
            'C': [0.1, 1, 10, 100],  
            'gamma': ['scale', 'auto', 0.01, 0.1, 1] 
        },
        'AdaBoost + Decision Tree': {
            'n_estimators': [100, 150, 200],  
            'learning_rate': [0.3, 0.5, 0.7],  
            'estimator__max_depth': [5, 6, 7, 8, 9]  
        }
    }
    # To store best params and scores
    best_params = {}
    best_scores = {}
    # Hyper paramaters optimization for each model
    for name, model in models.items():
        pipeline = Pipeline(steps=[('preprocessor', preprocessor_obj), ('classifier', model)])
        param_grid = {f'classifier__{key}': value for key, value in param_grids[name].items()}
        
        grid_search = GridSearchCV(
            pipeline,
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            n_jobs=-1
        )
        grid_search.fit(
            train_df.drop('obesity_level', axis=1), 
            train_df['obesity_level']
        )
        best_params[name] = grid_search.best_params_
        best_scores[name] = grid_search.best_score_
    # Print result
    hy_results_df = pd.DataFrame({
        'Best Params': best_params,
        'Best CV Accuracy': best_scores
    })
    # Output the results
    if not os.path.isdir(data_to):
        os.makedirs(data_to)
    hy_results_df.to_csv(os.path.join(data_to, "best_hyper_parameters.csv"), index=False)

    # Auto generating parameters
    auto_best_params = {}
    for name, params in hy_results_df['Best Params'].items():
        if name == 'AdaBoost + Decision Tree':
            # Capture DecisionTreeClassifier Parameters
            base_estimator_params = {
                key.split('__')[2]: value for key, value in params.items() if key.startswith('classifier__estimator__')
            }
            # Capture AdaBoostClassifier parameters
            ada_params = {
                key.split('__')[1]: value for key, value in params.items() if not key.startswith('classifier__estimator__')
            }
            # Create nested model parameters
            auto_best_params[name] = {
                **ada_params,
                'estimator': DecisionTreeClassifier(**base_estimator_params)
            }
        else:
            # For other models
            auto_best_params[name] = {
                key.split('__')[1]: value for key, value in params.items()
            }

    # Fit model by optimized parameters
    trained_pipelines = {}      
    for name, model in models.items():
        params = auto_best_params[name]
        # Dynamic Set AdaBoost + Decision Tree
        if name == 'AdaBoost + Decision Tree':
            model.set_params(**{k: v for k, v in params.items() if k != 'estimator'})
            model.estimator = params['estimator']
        else:
            model.set_params(**params)
        pipeline = Pipeline(steps=[('preprocessor', preprocessor_obj), ('classifier', model)])
        pipeline.fit(
            train_df.drop('obesity_level', axis=1), 
            train_df['obesity_level']
        )
        # Save trained_pipeline to a dict
        trained_pipelines[name] = pipeline

    os.makedirs(pipeline_to, exist_ok=True)
    trained_pipelines_path = os.path.join(pipeline_to, 'trained_pipelines.pkl')
    with open(trained_pipelines_path, 'wb') as f:
        pickle.dump(trained_pipelines, f)

if __name__ == '__main__':
    main()