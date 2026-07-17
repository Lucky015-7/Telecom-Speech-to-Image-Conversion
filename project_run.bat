@echo off
setlocal

set "ROOT=%~dp0"
set "CACHE_ROOT=%ROOT%.cache"
set "HF_HOME=%CACHE_ROOT%\huggingface"
set "HUGGINGFACE_HUB_CACHE=%HF_HOME%"
set "TRANSFORMERS_CACHE=%CACHE_ROOT%\transformers"
set "XDG_CACHE_HOME=%CACHE_ROOT%"
set "TORCH_HOME=%CACHE_ROOT%\torch"
set "WHISPER_CACHE=%CACHE_ROOT%\whisper"
set "TMP=%CACHE_ROOT%\temp"
set "TEMP=%CACHE_ROOT%\temp"
set "PIP_CACHE_DIR=%CACHE_ROOT%\pip"
set "VENV_DIR=%ROOT%\.venv"
set "VENV_PY=%VENV_DIR%\Scripts\python.exe"

set "PYTHON_CMD=python"
where py >nul 2>nul
if not errorlevel 1 set "PYTHON_CMD=py -3"

mkdir "%CACHE_ROOT%" 2>nul
mkdir "%HF_HOME%" 2>nul
mkdir "%TRANSFORMERS_CACHE%" 2>nul
mkdir "%TORCH_HOME%" 2>nul
mkdir "%WHISPER_CACHE%" 2>nul
mkdir "%TMP%" 2>nul
mkdir "%PIP_CACHE_DIR%" 2>nul

cd /d "%ROOT%"

if not exist "%VENV_PY%" (
    echo [INFO] Creating project virtual environment...
    %PYTHON_CMD% -m venv "%VENV_DIR%"
)

if exist "%VENV_PY%" (
    set "PYTHON_CMD=%VENV_PY%"
    set "PATH=%VENV_DIR%\Scripts;%PATH%"
)

echo ===================================================
echo   Starting Telecom Speech-to-Image Project...
echo ===================================================
echo.
echo [STEP 1/3] Checking and installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt

echo.
echo [STEP 2/3] Launching FastAPI Backend in a new window...
:: Backend will use the project-local cache folders and virtual environment.
start cmd /k "cd /d "%ROOT%" && "%VENV_PY%" -m uvicorn backend.main:app --reload"

echo.
echo [STEP 3/3] Launching Streamlit Frontend...
:: Frontend will run from the project root in the virtual environment.
%VENV_PY% -m streamlit run frontend/app.py

pause