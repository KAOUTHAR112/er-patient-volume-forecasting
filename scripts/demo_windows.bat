@echo off
call .venv\Scriptsctivate
python scripts\generate_demo_data.py
python run_experiment.py --data data\demo\daily_er_volume_demo.csv --fast --output results\demo --figures figures\demo
