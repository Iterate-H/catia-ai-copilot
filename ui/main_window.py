"""主窗口 — 三栏布局：宏编辑器 | 参数面板 | 代码预览。"""

from __future__ import annotations

import json

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QSplitter, QLabel, QToolBar, QToolButton, QStatusBar,
    QFileDialog, QFrame, QAction, QApplication,
    QProgressBar, QPushButton, QDialog, QDialogButtonBox,
)

from core.llm_client import LLMConfig
from core.macro_engine import parse_parameters, inject_parameters, run_in_catia, detect_language
from ui.macro_editor import MacroEditorPanel, CodeEditor
from ui.param_panel import ParamPanel
from ui.settings_dialog import SettingsDialog, load_settings
from ui.styles import STYLESHEET


class AnalysisWorker(QThread):
    """后台线程执行AI宏分析。"""
    finished = pyqtSignal(list)   # 参数列表
    error = pyqtSignal(str)       # 错误信息

    def __init__(self, config: LLMConfig, macro_code: str):
        super().__init__()
        self._config = config
        self._macro_code = macro_code

    def run(self):
        try:
            params = parse_parameters(self._config, self._macro_code)
            self.finished.emit(params)
        except json.JSONDecodeError as e:
            self.error.emit(f"AI 返回格式错误，无法解析参数: {e}")
        except Exception as e:
            self.error.emit(str(e))


class CatiaRunWorker(QThread):
    """后台线程执行CATIA宏。"""
    finished = pyqtSignal(str)

    def __init__(self, code: str, language: str):
        super().__init__()
        self._code = code
        self._language = language

    def run(self):
        result = run_in_catia(self._code, self._language)
        self.finished.emit(result)


def _show_msg(parent, title: str, text: str, level: str = "info"):
    """自定义消息对话框，避免 macOS 暗色模式下文字不可见。"""
    dlg = QDialog(parent)
    dlg.setWindowTitle(title)
    dlg.setMinimumWidth(360)
    layout = QVBoxLayout(dlg)
    layout.setContentsMargins(24, 20, 24, 20)
    layout.setSpacing(16)

    label = QLabel(text)
    label.setWordWrap(True)
    label.setStyleSheet("font-size: 14px; color: #37352F; line-height: 1.6;")
    layout.addWidget(label)

    btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
    btn_box.accepted.connect(dlg.accept)
    ok_btn = btn_box.button(QDialogButtonBox.Ok)
    if level == "error":
        ok_btn.setStyleSheet("background:#DC2626; color:white; border:none; border-radius:6px; padding:6px 20px; font-weight:600;")
    else:
        ok_btn.setObjectName("primaryButton")
    layout.addWidget(btn_box, alignment=Qt.AlignRight)

    dlg.exec_()


class MainWindow(QMainWindow):
    """CATIA 宏参数化工具主窗口。"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CATIA 宏参数化工具")
        self.resize(1280, 780)

        self._params: list[dict] = []
        self._macro_code: str = ""
        self._worker: AnalysisWorker | None = None
        self._run_worker: CatiaRunWorker | None = None

        self._setup_toolbar()
        self._setup_central()
        self._setup_statusbar()
        self._connect_signals()

    def _setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)

        # 左侧标题
        title = QLabel("CATIA 宏参数化工具")
        title.setObjectName("titleLabel")
        toolbar.addWidget(title)

        spacer = QWidget()
        spacer.setSizePolicy(
            spacer.sizePolicy().horizontalPolicy(),
            spacer.sizePolicy().verticalPolicy(),
        )
        from PyQt5.QtWidgets import QSizePolicy
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # 设置
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self._open_settings)
        toolbar.addAction(settings_action)

        toolbar.addSeparator()

        # 运行按钮（突出）
        run_btn = QToolButton()
        run_btn.setText("  运行  ")
        run_btn.setObjectName("runButton")
        run_btn.clicked.connect(self._on_run)
        toolbar.addWidget(run_btn)

        self.addToolBar(toolbar)

    def _setup_central(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(12)
        splitter.setChildrenCollapsible(False)

        # 左栏：宏代码编辑器
        self._macro_editor = MacroEditorPanel()
        splitter.addWidget(self._macro_editor)

        # 中栏：参数面板
        self._param_panel = ParamPanel()
        splitter.addWidget(self._param_panel)

        # 右栏：生成代码预览
        right_panel = QFrame()
        right_panel.setObjectName("card")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        preview_title = QLabel("生成代码")
        preview_title.setObjectName("sectionTitle")
        right_layout.addWidget(preview_title)

        self._code_preview = CodeEditor(read_only=True)
        self._code_preview.setPlaceholderText("参数化后的代码将显示在这里...")
        right_layout.addWidget(self._code_preview, 1)

        # 预览底部按钮
        preview_footer = QHBoxLayout()
        preview_footer.setContentsMargins(12, 8, 12, 12)
        preview_footer.addStretch()

        copy_btn = QPushButton("复制代码")
        copy_btn.clicked.connect(self._copy_code)
        preview_footer.addWidget(copy_btn)

        export_file_btn = QPushButton("导出文件")
        export_file_btn.clicked.connect(lambda: self._export_script(self._param_panel.get_values()))
        preview_footer.addWidget(export_file_btn)

        right_layout.addLayout(preview_footer)
        splitter.addWidget(right_panel)

        # 比例 35:25:40
        splitter.setSizes([420, 310, 480])

        layout.addWidget(splitter)

    def _setup_statusbar(self):
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._statusbar.showMessage("就绪")

    def _connect_signals(self):
        self._macro_editor.analyze_requested.connect(self._analyze_macro)
        self._param_panel.params_applied.connect(self._apply_params)
        self._param_panel.run_requested.connect(self._on_run_with_params)

    # ── 工具栏操作 ──

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "打开宏文件", "",
            "CATIA宏 (*.CATScript *.catvbs);;Python (*.py);;所有文件 (*)"
        )
        if path:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                self._macro_editor.set_code(f.read())

    def _open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    # ── AI 分析 ──

    def _analyze_macro(self, code: str):
        settings = load_settings()
        api_key = settings.get("api_key", "")
        if not api_key:
            _show_msg(self, "未配置", "请先在「设置」中配置 API Key。")
            self._open_settings()
            return

        self._macro_code = code
        self._statusbar.showMessage("正在分析宏参数...")
        self._set_analyzing(True)

        config = LLMConfig(
            provider=settings.get("provider", "deepseek"),
            api_key=api_key,
            model=settings.get("model") or None,
        )

        self._worker = AnalysisWorker(config, code)
        self._worker.finished.connect(self._on_analysis_done)
        self._worker.error.connect(self._on_analysis_error)
        self._worker.start()

    def _on_analysis_done(self, params: list[dict]):
        self._params = params
        self._param_panel.set_parameters(params)
        self._statusbar.showMessage(f"提取到 {len(params)} 个可调参数")
        self._set_analyzing(False)

        # 立即用默认值生成预览
        values = self._param_panel.get_values()
        self._update_preview(values)

    def _on_analysis_error(self, error: str):
        self._statusbar.showMessage(f"分析失败: {error}")
        self._set_analyzing(False)
        _show_msg(self, "分析失败", f"AI 参数分析出错:\n\n{error}", "error")

    def _set_analyzing(self, analyzing: bool):
        """分析中禁用按钮、显示加载提示。"""
        self._macro_editor.setEnabled(not analyzing)
        if analyzing:
            self._param_panel.show_loading("正在分析参数，请稍候...")
        else:
            self._param_panel.hide_loading()

    # ── 参数操作 ──

    def _apply_params(self, values: dict):
        self._update_preview(values)
        self._statusbar.showMessage("参数已应用，代码已更新")

    def _update_preview(self, values: dict):
        if not self._macro_code or not self._params:
            return
        new_code = inject_parameters(self._macro_code, self._params, values)
        self._code_preview.setPlainText(new_code)

        # 同步语法高亮
        from ui.macro_editor import VBScriptHighlighter, PythonHighlighter
        lang = detect_language(new_code)
        if lang == "python":
            PythonHighlighter(self._code_preview.document())
        else:
            VBScriptHighlighter(self._code_preview.document())

    # ── 运行 ──

    def _on_run(self):
        values = self._param_panel.get_values()
        self._on_run_with_params(values)

    def _on_run_with_params(self, values: dict):
        # 优先用右栏预览代码，没有则取编辑器原始代码
        code = self._code_preview.toPlainText().strip()
        if not code:
            code = self._macro_editor.get_code().strip()
        if not code:
            _show_msg(self, "提示", "请先上传或粘贴 CATIA 宏代码。")
            return

        if not self._params:
            _show_msg(self, "提示", "请先点击「分析参数」提取可调参数，\n再修改参数后运行。")
            return

        self._apply_params(values)
        code = self._code_preview.toPlainText()
        language = detect_language(code)

        self._statusbar.showMessage("正在执行宏...")
        self._run_worker = CatiaRunWorker(code, language)
        self._run_worker.finished.connect(self._on_run_done)
        self._run_worker.start()

    def _on_run_done(self, result: str):
        self._statusbar.showMessage(result)
        level = "error" if ("失败" in result or "缺少" in result) else "info"
        _show_msg(self, "执行结果", result, level)

    # ── 导出 ──

    def _export_script(self, values: dict):
        if not self._macro_code:
            _show_msg(self, "提示", "请先上传宏代码并分析参数。")
            return

        self._apply_params(values)
        code = self._code_preview.toPlainText()
        language = detect_language(code)

        if language == "python":
            ext_filter = "Python (*.py)"
            default_name = "catia_macro.py"
        else:
            ext_filter = "CATScript (*.CATScript)"
            default_name = "catia_macro.CATScript"

        path, _ = QFileDialog.getSaveFileName(
            self, "导出脚本", default_name, ext_filter
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)
            self._statusbar.showMessage(f"已导出: {path}")

    # ── 复制 ──

    def _copy_code(self):
        code = self._code_preview.toPlainText()
        if code:
            QApplication.clipboard().setText(code)
            self._statusbar.showMessage("代码已复制到剪贴板")
