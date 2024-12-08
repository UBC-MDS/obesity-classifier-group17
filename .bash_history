python scripts/download_data.py --write_to="data/raw" --name="ObesityDataSet_raw_data_sinthetic.csv"
python scripts/clean_data.py --raw-data='data/raw/ObesityDataSet_raw_data_sinthetic.csv' --name='ObesityDataSet_processed_data.csv' --data-to="data/processed/" --plot-to="results/figures" --html-to="results/htmls
python scripts/eda.py --training_data_split=data/processed/obesity_train.csv --plot_path=results/figures/
python scripts/split_n_preprocess.py --clean-data=data/processed/ObesityDataSet_processed_data.csv --data-to=data/processed --preprocessor-to=results/models --seed=522
python scripts/fit_obesity_classifier.py --encoded-train-data=data/processed/obesity_train_target_encoding.csv --data-to=results/tables --preprocessor=results/models/obesity_preprocessor.pickle --seed=522 --pipeline-to=results/models
python scripts/evaluate_models.py --test-data=data/processed/obesity_test_target_encoding.csv --pipeline-path=results/models/trained_pipelines.pkl --data-to=results/tables --plot-to=results/figures

python scripts/download_data.py --write_to="data/raw" --name="ObesityDataSet_raw_data_sinthetic.csv"
python scripts/clean_data.py --raw-data='data/raw/ObesityDataSet_raw_data_sinthetic.csv' --name='ObesityDataSet_processed_data.csv' --data-to="data/processed/" --plot-to="results/figures" --html-to="results/htmls

python scripts/eda.py --training_data_split=data/processed/obesity_train.csv --plot_path=results/figures/

python scripts/split_n_preprocess.py --clean-data=data/processed/ObesityDataSet_processed_data.csv --data-to=data/processed --preprocessor-to=results/models --seed=522

python scripts/fit_obesity_classifier.py --encoded-train-data=data/processed/obesity_train_target_encoding.csv --data-to=results/tables --preprocessor=results/models/obesity_preprocessor.pickle --seed=522 --pipeline-to=results/models

python scripts/evaluate_models.py --test-data=data/processed/obesity_test_target_encoding.csv --pipeline-path=results/models/trained_pipelines.pkl --data-to=results/tables --plot-to=results/figures
