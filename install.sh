#!/bin/bash
echo "============================================"
echo "  CATIA 宏参数化工具 - 一键安装"
echo "============================================"
echo

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.9+"
    exit 1
fi

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "[1/3] 创建虚拟环境..."
    python3 -m venv .venv
fi

# 安装依赖
echo "[2/3] 安装依赖..."
source .venv/bin/activate
pip install -r requirements.txt -q

# 启动
echo "[3/3] 启动应用..."
echo
python3 app.py
