@echo off
echo Starting RecallBuddy...
pip install -r requirements.txt
start http://127.0.0.1:8000
python -m uvicorn server:app --reload
pause