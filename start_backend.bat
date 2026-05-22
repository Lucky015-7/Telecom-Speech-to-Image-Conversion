@echo off
echo ========================================
echo  SLT Mobitel Voice-to-Image System
echo  Starting Backend API Server
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting FastAPI backend on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
