@echo off
echo ========================================
echo  SLT Mobitel Voice-to-Image System
echo  Complete System Launcher
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Backend API Server...
start "Voice-to-Image Backend" cmd /k "call .venv\Scripts\activate.bat && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

echo.
echo Starting Frontend Interface...
start "Voice-to-Image Frontend" cmd /k "call .venv\Scripts\activate.bat && streamlit run frontend\app.py"

echo.
echo ========================================
echo  System Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:8501
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit this window...
echo (Backend and Frontend will continue running)
pause > nul
