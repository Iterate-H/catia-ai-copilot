@echo off
:: 切换到脚本所在目录
cd /d "%~dp0"

:: 尝试设置UTF-8，失败也继续
chcp 65001 >nul 2>&1

echo ============================================
echo   CATIA Macro Parameterizer - Install
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Error] Python not found. Please install Python 3.9+
    echo Download: https://www.python.org/downloads/
    echo.
    echo NOTE: Check "Add Python to PATH" during installation!
    echo.
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
