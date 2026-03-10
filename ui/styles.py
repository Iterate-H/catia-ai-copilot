"""全局样式表 — Claude/Notion 风格，暖灰配色，工程师友好。"""

# 色板
COLORS = {
    "bg": "#FAF9F7",           # 暖白背景（Claude风格）
    "surface": "#FFFFFF",       # 卡片白
    "surface_alt": "#F5F3F0",   # 次级面板背景
    "border": "#E8E5E0",        # 柔和边框
    "border_focus": "#C4A882",  # 聚焦边框（暖棕）
    "text": "#37352F",          # 主文字（Notion 深棕黑）
    "text_secondary": "#787774",# 次级文字
    "text_muted": "#B4B0AB",   # 占位符
    "accent": "#D97706",        # 强调色（琥珀/工程橙）
    "accent_hover": "#B45309",
    "accent_light": "#FEF3C7",  # 强调色浅底
    "code_bg": "#1E1E1E",       # 代码区深色背景
    "code_text": "#D4D4D4",     # 代码文字
    "success": "#059669",       # 成功绿
    "error": "#DC2626",         # 错误红
    "scrollbar": "#D5D3CE",
    "scrollbar_hover": "#B4B0AB",
}

STYLESHEET = f"""
/* ── 全局 ── */
QMainWindow, QDialog {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: -apple-system, "SF Pro Text", "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 13px;
}}

/* ── 工具栏 ── */
QToolBar {{
    background-color: {COLORS['surface']};
    border-bottom: 1px solid {COLORS['border']};
    padding: 6px 12px;
    spacing: 8px;
}}
QToolBar QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 14px;
    color: {COLORS['text']};
    font-size: 13px;
    font-weight: 500;
}}
QToolBar QToolButton:hover {{
    background-color: {COLORS['surface_alt']};
    border-color: {COLORS['border']};
}}
QToolBar QToolButton#runButton {{
    background-color: {COLORS['accent']};
    color: white;
    font-weight: 600;
    border: none;
}}
QToolBar QToolButton#runButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

/* ── 标题标签 ── */
QLabel#titleLabel {{
    font-size: 14px;
    font-weight: 600;
    color: {COLORS['text']};
    padding: 0 8px;
}}

/* ── 卡片面板 ── */
QFrame#card {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
}}

/* ── 区域标题 ── */
QLabel#sectionTitle {{
    font-size: 12px;
    font-weight: 700;
    color: {COLORS['text_secondary']};
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 12px 16px 6px 16px;
}}

/* ── 代码编辑器 ── */
QPlainTextEdit#codeEditor {{
    background-color: {COLORS['code_bg']};
    color: {COLORS['code_text']};
    border: none;
    border-radius: 0 0 10px 10px;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Consolas", monospace;
    font-size: 13px;
    padding: 12px;
    selection-background-color: #264F78;
}}
QPlainTextEdit#codePreview {{
    background-color: {COLORS['code_bg']};
    color: {COLORS['code_text']};
    border: none;
    border-radius: 0 0 10px 10px;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Consolas", monospace;
    font-size: 13px;
    padding: 12px;
    selection-background-color: #264F78;
}}

/* ── 行号栏 ── */
QWidget#lineNumberArea {{
    background-color: #252526;
    color: #858585;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", "Consolas", monospace;
    font-size: 13px;
}}

/* ── 参数面板 ── */
QScrollArea#paramScroll {{
    background: transparent;
    border: none;
}}
QWidget#paramContainer {{
    background: transparent;
}}

/* ── 参数行 ── */
QFrame#paramRow {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
}}
QFrame#paramRow:hover {{
    border-color: {COLORS['border_focus']};
}}
QLabel#paramLabel {{
    font-size: 13px;
    font-weight: 500;
    color: {COLORS['text']};
    padding-left: 4px;
}}
QLabel#paramUnit {{
    font-size: 12px;
    color: {COLORS['text_secondary']};
    padding-right: 4px;
}}

/* ── 输入控件（统一风格）── */
QSpinBox, QDoubleSpinBox {{
    background-color: {COLORS['surface_alt']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 5px 8px;
    color: {COLORS['text']};
    font-size: 13px;
    min-height: 28px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {COLORS['accent']};
    background-color: {COLORS['surface']};
}}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    width: 20px;
    border: none;
    background: transparent;
}}
QLineEdit {{
    background-color: {COLORS['surface_alt']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 5px 10px;
    color: {COLORS['text']};
    font-size: 13px;
    min-height: 28px;
}}
QLineEdit:focus {{
    border-color: {COLORS['accent']};
    background-color: {COLORS['surface']};
}}
QLineEdit::placeholder {{
    color: {COLORS['text_muted']};
}}
QCheckBox {{
    color: {COLORS['text']};
    font-size: 13px;
    spacing: 6px;
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background: {COLORS['surface']};
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}
QComboBox {{
    background-color: {COLORS['surface_alt']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: 5px 10px;
    color: {COLORS['text']};
    font-size: 13px;
    min-height: 28px;
}}
QComboBox:focus {{
    border-color: {COLORS['accent']};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

/* ── 按钮 ── */
QPushButton {{
    background-color: {COLORS['surface']};
    border: 1px solid {COLORS['border']};
    border-radius: 7px;
    padding: 8px 18px;
    color: {COLORS['text']};
    font-size: 13px;
    font-weight: 500;
    min-height: 32px;
}}
QPushButton:hover {{
    background-color: {COLORS['surface_alt']};
    border-color: {COLORS['border_focus']};
}}
QPushButton:pressed {{
    background-color: {COLORS['border']};
}}
QPushButton#primaryButton {{
    background-color: {COLORS['accent']};
    color: white;
    border: none;
    font-weight: 600;
}}
QPushButton#primaryButton:hover {{
    background-color: {COLORS['accent_hover']};
}}
QPushButton#analyzeButton {{
    background-color: {COLORS['text']};
    color: {COLORS['surface']};
    border: none;
    font-weight: 600;
}}
QPushButton#analyzeButton:hover {{
    background-color: #504E49;
}}

/* ── 滚动条 ── */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {COLORS['scrollbar']};
    border-radius: 4px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{
    background: {COLORS['scrollbar_hover']};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
}}
QScrollBar::handle:horizontal {{
    background: {COLORS['scrollbar']};
    border-radius: 4px;
    min-width: 30px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {COLORS['scrollbar_hover']};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
}}

/* ── Splitter 拖拽条 ── */
QSplitter::handle {{
    background-color: {COLORS['border']};
}}
QSplitter::handle:horizontal {{
    width: 1px;
}}

/* ── 状态栏 ── */
QStatusBar {{
    background-color: {COLORS['surface']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding: 2px 12px;
}}

/* ── 对话框 ── */
QDialog {{
    background-color: {COLORS['bg']};
}}
QGroupBox {{
    font-size: 13px;
    font-weight: 600;
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px 12px 12px 12px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {COLORS['text_secondary']};
}}

/* ── 提示标签 ── */
QLabel#hintLabel {{
    color: {COLORS['text_muted']};
    font-size: 12px;
    padding: 8px 16px;
}}

/* ── 空状态 ── */
QLabel#emptyState {{
    color: {COLORS['text_muted']};
    font-size: 14px;
    padding: 40px;
}}
"""
