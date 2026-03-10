"""组装宏分析提示词 — 将知识库模块拼接为完整的 system prompt。"""

from knowledge.system_prompt import SYSTEM_PROMPT
from knowledge.catia_api_reference import CATIA_API_REFERENCE


def build_analysis_prompt() -> str:
    """组装宏参数分析的系统提示词。"""
    return "\n\n".join([
        SYSTEM_PROMPT,
        "# CATIA API 参考（辅助你理解宏代码中的对象和方法）",
        CATIA_API_REFERENCE,
    ])


def build_user_message(macro_code: str) -> str:
    """构建用户消息：包含待分析的宏代码。"""
    return f"请分析以下 CATIA 宏代码，提取所有可调参数并返回 JSON 数组：\n\n```\n{macro_code}\n```"
