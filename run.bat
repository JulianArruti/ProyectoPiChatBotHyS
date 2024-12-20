@echo off
REM run.bat (Windows)
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload