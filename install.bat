@echo off
cd /d "%~dp0"
chcp 65001 >nul 2>&1

echo ============================================
echo   CATIA Macro Parameterizer - Install
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ============================================
    echo   Python not detected!
    echo ============================================
    echo.
    echo   Two options:
    echo.
    echo   [Option 1] Download exe version (no Python needed):
    echo   https://github.com/Iterate-H/catia-ai-copilot/releases
    echo.
    echo   [Option 2] Install Python first:
    echo   https://www.python.org/downloads/
    echo   IMPORTANT: Check "Add Python to PATH" during install!
    echo.
    echo   After installing Python, run this script again.
    echo ============================================
    echo.
    choice /c 12 /n /m "Open [1] Releases page or [2] Python download? "
    if errorlevel 2 (
        start https://www.python.org/downloads/
    ) else (
        start https://github.com/Iterate-H/catia-ai-copilot/releases
    )
    pause
    exit /b 1
)

echo [1/3] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo [Error] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

echo [2/3] Installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [Error] Failed to install dependencies.
    pause
    exit /b 1
)

echo [3/3] Starting application...
echo.
python app.py

if errorlevel 1 (
    echo.
    echo [Error] Application exited with error.
)
pause
