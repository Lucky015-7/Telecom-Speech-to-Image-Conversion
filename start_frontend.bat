@echo off
echo ========================================
echo  SLT Mobitel Voice-to-Image System
echo  Starting Frontend Interface
echo ========================================
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Streamlit frontend...
echo The app will open in your browser automatically
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run frontend\app.py
