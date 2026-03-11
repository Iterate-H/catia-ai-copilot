@echo off
cd /d "%~dp0"

echo ============================================
echo   CATIA Macro Parameterizer
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 goto nopython

echo [1/3] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
)
if not exist ".venv\Scripts\activate.bat" (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/3] Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo [3/3] Starting application...
echo.
python app.py
pause
exit /b 0

:nopython
echo ============================================
echo   Python is not installed!
echo ============================================
echo.
echo   Please install Python 3.9 or later:
echo   https://www.python.org/downloads/
echo.
echo   IMPORTANT: Check "Add Python to PATH"
echo   during installation!
echo.
echo   After installing, run this file again.
echo ============================================
echo.
pause
exit /b 1
