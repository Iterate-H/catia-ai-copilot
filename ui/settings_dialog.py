"""设置对话框 — API Key 配置、AI 提供商选择。"""

from __future__ import annotations

import json
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QGroupBox, QFormLayout,
)

CONFIG_PATH = Path.home() / ".catia_copilot.json"

DEFAULT_MODELS = {
    "deepseek": "deepseek-chat",
    "openai": "gpt-4o",
    "claude": "claude-sonnet-4-20250514",
}


def load_settings() -> dict:
    """从配置文件加载设置。"""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"provider": "deepseek", "api_key": "", "model": ""}


def save_settings(settings: dict):
    """保存设置到配置文件。"""
    CONFIG_PATH.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")


class SettingsDialog(QDialog):
    """API Key 和 AI 提供商设置对话框。"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(480, 380)
        self.setModal(True)
        self._settings = load_settings()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # AI 配置组
        group = QGroupBox("AI 配置")
        group.setStyleSheet("""
            QGroupBox { color: #37352F; }
            QGroupBox::title { color: #787774; }
        """)
        form = QFormLayout(group)
        form.setSpacing(20)
        form.setContentsMargins(20, 32, 20, 20)
        form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        label_style = "font-size: 13px; font-weight: 500; color: #37352F;"

        # 提供商
        lbl_provider = QLabel("AI 提供商")
        lbl_provider.setStyleSheet(label_style)
        self._provider = QComboBox()
        self._provider.addItems(["deepseek", "openai", "claude"])
        self._provider.setCurrentText(self._settings.get("provider", "deepseek"))
        self._provider.currentTextChanged.connect(self._on_provider_changed)
        form.addRow(lbl_provider, self._provider)

        # API Key
        lbl_key = QLabel("API Key")
        lbl_key.setStyleSheet(label_style)
        self._api_key = QLineEdit()
        self._api_key.setEchoMode(QLineEdit.Password)
        self._api_key.setPlaceholderText("输入 API Key...")
        self._api_key.setText(self._settings.get("api_key", ""))
        form.addRow(lbl_key, self._api_key)

        # 模型
        lbl_model = QLabel("模型名称")
        lbl_model.setStyleSheet(label_style)
        self._model = QLineEdit()
        self._model.setPlaceholderText(self._get_default_model_hint())
        self._model.setText(self._settings.get("model", ""))
        form.addRow(lbl_model, self._model)

        layout.addWidget(group)

        # 提示
        hint = QLabel("配置保存在 ~/.catia_copilot.json")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("font-size: 12px; color: #B4B0AB;")
        layout.addWidget(hint)

        layout.addStretch()

        # 按钮
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("保存")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _get_default_model_hint(self) -> str:
        provider = self._provider.currentText()
        return f"留空使用默认: {DEFAULT_MODELS.get(provider, '')}"

    def _on_provider_changed(self, provider: str):
        self._model.setPlaceholderText(self._get_default_model_hint())

    def _on_save(self):
        self._settings = {
            "provider": self._provider.currentText(),
            "api_key": self._api_key.text().strip(),
            "model": self._model.text().strip(),
        }
        save_settings(self._settings)
        self.accept()

    def get_settings(self) -> dict:
        return self._settings
