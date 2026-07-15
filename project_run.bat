@echo off
echo ===================================================
echo   Starting Telecom Speech-to-Image Project...
echo ===================================================

echo [STEP 1/3] Checking and installing dependencies...
python -m pip install -r requirements.txt

echo.
echo [STEP 2/3] Launching FastAPI Backend in a new window...
:: අලුත් Window එකක Backend එක Run කරනවා
start cmd /k "echo Running Backend... && python -m uvicorn backend.main:app --reload"

echo.
echo [STEP 3/3] Launching Streamlit Frontend...
:: මේ Window එකේම Frontend එක Run වෙන්න දෙනවා
python -m streamlit run frontend/app.py

pause