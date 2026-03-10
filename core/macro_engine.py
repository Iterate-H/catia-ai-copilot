"""宏引擎 — 宏解析（AI参数提取）、参数注入、CATIA 执行。"""

from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

from core.llm_client import LLMConfig, stream_chat
from core.prompt_builder import build_analysis_prompt, build_user_message


def parse_parameters(config: LLMConfig, macro_code: str) -> list[dict]:
    """调用 AI 分析宏代码，返回可调参数列表。

    Returns:
        [{"name", "label", "type", "default", "unit", "min", "max", "step", "line", "original_code"}, ...]
    """
    system_prompt = build_analysis_prompt()
    user_message = build_user_message(macro_code)
    messages = [{"role": "user", "content": user_message}]

    # 收集完整响应
    full_response = ""
    for chunk in stream_chat(config, messages, system_prompt):
        full_response += chunk

    # 提取 JSON — AI 可能返回带 markdown 围栏的 JSON
    json_str = _extract_json(full_response)
    params = json.loads(json_str)

    # 标准化每个参数
    validated = []
    for p in params:
        validated.append({
            "name": p.get("name", "param"),
            "label": p.get("label", p.get("name", "参数")),
            "type": p.get("type", "float"),
            "default": p.get("default"),
            "unit": p.get("unit", ""),
            "min": p.get("min"),
            "max": p.get("max"),
            "step": p.get("step"),
            "line": p.get("line"),
            "original_code": p.get("original_code", ""),
        })
    return validated


def inject_parameters(macro_code: str, params: list[dict], values: dict) -> str:
    """将用户修改的参数值注入宏代码，返回新的可执行代码。

    Args:
        macro_code: 原始宏代码
        params: AI 提取的参数列表
        values: 用户修改的参数值 {param_name: new_value}
    """
    lines = macro_code.split("\n")

    for param in params:
        name = param["name"]
        if name not in values:
            continue

        new_val = values[name]
        old_val = param["default"]
        original_code = param.get("original_code", "").strip()

        if old_val is None:
            continue

        old_str = _format_value(old_val)
        new_str = _format_value(new_val)

        if old_str == new_str:
            continue

        # 策略1：用 AI 返回的行号定位
        target_idx = None
        line_idx = param.get("line")
        if line_idx is not None:
            idx = line_idx - 1
            if 0 <= idx < len(lines) and old_str in lines[idx]:
                target_idx = idx

        # 策略2：行号不准时，用 original_code 内容匹配
        if target_idx is None and original_code:
            for i, line in enumerate(lines):
                if original_code in line.strip() or line.strip() in original_code:
                    if old_str in line:
                        target_idx = i
                        break

        # 策略3：全文搜索包含旧值的行（仅限赋值语句）
        if target_idx is None:
            for i, line in enumerate(lines):
                stripped = line.strip()
                # 匹配赋值语句中的值（= value 或 , value）
                if old_str in stripped and ("=" in stripped or "," in stripped):
                    target_idx = i
                    break

        if target_idx is not None:
            lines[target_idx] = lines[target_idx].replace(old_str, new_str, 1)

    return "\n".join(lines)


def run_in_catia(macro_code: str, language: str = "vbscript") -> str:
    """启动 CATIA 并执行宏代码（仅 Windows）。

    Args:
        macro_code: 要执行的宏代码
        language: "vbscript" 或 "python"

    Returns:
        执行状态消息
    """
    if sys.platform != "win32":
        return "CATIA 自动执行仅支持 Windows 系统。请使用「导出脚本」功能保存宏文件后手动执行。"

    try:
        import win32com.client  # type: ignore
    except ImportError:
        return "缺少 pywin32 库。请运行: pip install pywin32"

    if language == "python":
        # Python 宏 → 保存为临时文件并执行
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(macro_code)
            tmp_path = f.name
        import subprocess
        result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True)
        Path(tmp_path).unlink(missing_ok=True)
        if result.returncode == 0:
            return "Python 宏执行成功。"
        return f"执行失败:\n{result.stderr}"

    # VBScript 宏 → COM 方式执行
    try:
        catia = win32com.client.Dispatch("CATIA.Application")
        catia.Visible = True
    except Exception:
        return "无法连接 CATIA。请确保 CATIA V5 已安装并启动。"

    # 保存为临时 CATScript 文件并通过 CATIA 执行
    with tempfile.NamedTemporaryFile(mode="w", suffix=".CATScript", delete=False, encoding="utf-8") as f:
        f.write(macro_code)
        tmp_path = f.name

    try:
        catia.SystemService.ExecuteScript(
            "FileSystem", 1, tmp_path, "CATMain", []
        )
        return "宏执行成功。"
    except Exception as e:
        return f"宏执行失败: {e}"
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def detect_language(macro_code: str) -> str:
    """检测宏代码语言类型。"""
    code_lower = macro_code.lower()
    if "sub catmain" in code_lower or "end sub" in code_lower or "dim " in code_lower:
        return "vbscript"
    if "import " in code_lower or "from pycatia" in code_lower or "def " in code_lower:
        return "python"
    return "vbscript"  # 默认


def _extract_json(text: str) -> str:
    """从 AI 响应中提取 JSON 数组。"""
    # 尝试去除 markdown 围栏
    fence_match = re.search(r"```(?:json)?\s*\n?(.*?)```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()

    # 尝试直接找 [ ... ]
    bracket_match = re.search(r"\[.*\]", text, re.DOTALL)
    if bracket_match:
        return bracket_match.group(0)

    return text.strip()


def _format_value(val) -> str:
    """将参数值格式化为代码中可替换的字符串。"""
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, float):
        # 如果是整数值的 float，去掉 .0 以匹配原始代码
        if val == int(val):
            return str(int(val))
        return str(val)
    return str(val)
