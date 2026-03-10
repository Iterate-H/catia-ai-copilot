@echo off
chcp 65001 >nul
echo ============================================
echo   CATIA 宏参数化工具 - 一键安装
echo ============================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 创建虚拟环境
if not exist ".venv" (
    echo [1/3] 创建虚拟环境...
    python -m venv .venv
)

:: 激活虚拟环境并安装依赖
echo [2/3] 安装依赖...
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q

:: 启动
echo [3/3] 启动应用...
echo.
python app.py

pause
