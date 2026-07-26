@echo off
call .venv\Scriptsctivate
python run_experiment.py --data data\processed\daily_er_volume.csv
