.PHONY: clean

all: render_report

download_data: 
	python scripts/download_data.py \
		--name=ObesityDataSet_raw_data_sinthetic.csv \
    	--write_to=data/raw

clean_data: download_data
	python scripts/clean_data.py \
		--raw-data='data/raw/ObesityDataSet_raw_data_sinthetic.csv' \
		--name='ObesityDataSet_processed_data.csv' --data-to="data/processed/" \
		--plot-to="results/figures" \
		--html-to="results/htmls"

split_preprocess_data: clean_data
	python scripts/clean_data.py \
		--raw-data='data/raw/ObesityDataSet_raw_data_sinthetic.csv' \
		--name='ObesityDataSet_processed_data.csv' --data-to="data/processed/" \
		--plot-to="results/figures" \
		--html-to="results/htmls"

eda: split_preprocess_data
	python scripts/eda.py \
		--training_data_split=data/processed/obesity_train.csv \
		--plot_path=results/figures/

fit_obesity_classifier:
	python scripts/fit_obesity_classifier.py \
		--encoded-train-data=data/processed/obesity_train_target_encoding.csv \
		--data-to=results/tables --preprocessor=results/models/obesity_preprocessor.pickle \
		--seed=522 --pipeline-to=results/models

evaluate_models: fit_obesity_classifier
	python scripts/evaluate_models.py \
		--test-data=data/processed/obesity_test_target_encoding.csv \
		--pipeline-path=results/models/trained_pipelines.pkl \
		--data-to=results/tables \
		--plot-to=results/figures

render_report: evaluate_models
	quarto render report/obesity_level_predictor_report.qmd --to html

clean:
	rm -f results/isles.dat \
		results/abyss.dat \
		results/last.dat \
		results/sierra.dat
	rm -f results/figure/isles.png \
		results/figure/abyss.png \
		results/figure/last.png \
		results/figure/sierra.png	
	rm -rf report/count_report.html \
		report/count_report_files	