"""LLM多后端抽象层 — 支持DeepSeek / OpenAI / Claude，统一流式输出接口。"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Generator

import openai
import anthropic


@dataclass
class LLMConfig:
    provider: str  # "deepseek" | "openai" | "claude"
    api_key: str
    model: str | None = None
    temperature: float = 0.3
    max_tokens: int = 4096

    @property
    def resolved_model(self) -> str:
        if self.model:
            return self.model
        defaults = {
            "deepseek": "deepseek-chat",
            "openai": "gpt-4o",
            "claude": "claude-sonnet-4-20250514",
        }
        return defaults[self.provider]


# ── provider → base_url 映射 ──
_BASE_URLS = {
    "deepseek": "https://api.deepseek.com",
    "openai": "https://api.openai.com/v1",
}


def stream_chat(
    config: LLMConfig,
    messages: list[dict],
    system_prompt: str,
) -> Generator[str, None, None]:
    """统一流式接口：yield 文本 chunk。"""
    if config.provider in ("deepseek", "openai"):
        yield from _stream_openai_compat(config, messages, system_prompt)
    elif config.provider == "claude":
        yield from _stream_claude(config, messages, system_prompt)
    else:
        raise ValueError(f"不支持的 provider: {config.provider}")


# ── OpenAI 兼容（DeepSeek / OpenAI）──
def _stream_openai_compat(
    config: LLMConfig,
    messages: list[dict],
    system_prompt: str,
) -> Generator[str, None, None]:
    client = openai.OpenAI(
        api_key=config.api_key,
        base_url=_BASE_URLS[config.provider],
    )
    full_messages = [{"role": "system", "content": system_prompt}] + messages
    stream = client.chat.completions.create(
        model=config.resolved_model,
        messages=full_messages,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content


# ── Anthropic Claude ──
def _stream_claude(
    config: LLMConfig,
    messages: list[dict],
    system_prompt: str,
) -> Generator[str, None, None]:
    client = anthropic.Anthropic(api_key=config.api_key)
    with client.messages.stream(
        model=config.resolved_model,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        system=system_prompt,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
