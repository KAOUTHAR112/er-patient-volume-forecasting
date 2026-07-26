@echo off
python -m venv .venv
call .venv\Scriptsctivate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo Installation completed.
