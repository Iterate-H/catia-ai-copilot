@echo off
cd /d "%~dp0"

echo ============================================
echo   CATIA Macro Parameterizer
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 goto nopython

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
    if not exist ".venv\Scripts\python.exe" (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [1/3] Virtual environment exists.
)

echo [2/3] Installing dependencies (may take a minute)...
.venv\Scripts\pip.exe install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Install failed. Check your network connection.
    pause
    exit /b 1
)

echo.
echo [3/3] Starting application...
echo.

:: Find Qt plugins path and set it
for /f "delims=" %%i in ('.venv\Scripts\python.exe -c "import os, PyQt5; print(os.path.join(os.path.dirname(PyQt5.__file__), 'Qt5', 'plugins', 'platforms'))"') do set QT_QPA_PLATFORM_PLUGIN_PATH=%%i

echo Qt plugin path: %QT_QPA_PLATFORM_PLUGIN_PATH%

if not exist "%QT_QPA_PLATFORM_PLUGIN_PATH%\qwindows.dll" (
    echo.
    echo Qt plugin not found, trying alternate path...
    for /f "delims=" %%i in ('.venv\Scripts\python.exe -c "import os, PyQt5; print(os.path.join(os.path.dirname(PyQt5.__file__), 'Qt', 'plugins', 'platforms'))"') do set QT_QPA_PLATFORM_PLUGIN_PATH=%%i
    echo Qt plugin path: %QT_QPA_PLATFORM_PLUGIN_PATH%
)

.venv\Scripts\python.exe app.py
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
