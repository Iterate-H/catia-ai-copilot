"""宏代码编辑器 — 带行号、语法高亮、拖拽上传的代码编辑区。"""

from __future__ import annotations

import re

from PyQt5.QtCore import Qt, QRect, QMimeData, pyqtSignal
from PyQt5.QtGui import (
    QColor, QFont, QFontMetrics, QPainter, QSyntaxHighlighter,
    QTextCharFormat, QTextDocument, QPalette,
)
from PyQt5.QtWidgets import (
    QWidget, QPlainTextEdit, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QFrame,
)


class VBScriptHighlighter(QSyntaxHighlighter):
    """VBScript / CATScript 语法高亮。"""

    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self._rules: list[tuple[re.Pattern, QTextCharFormat]] = []

        # 关键字
        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor("#569CD6"))
        kw_fmt.setFontWeight(QFont.Bold)
        keywords = (
            r"\b(Sub|End Sub|Function|End Function|Dim|Set|If|Then|Else|ElseIf|"
            r"End If|For|To|Step|Next|Do|While|Loop|Until|Exit|Select|Case|"
            r"As|New|Nothing|True|False|And|Or|Not|Mod|Is|Call|ReDim|"
            r"On Error|Resume|GoTo|With|End With|Each|In|Let|Const|"
            r"Public|Private|ByVal|ByRef|Optional|Static|Type|Enum)\b"
        )
        self._rules.append((re.compile(keywords, re.IGNORECASE), kw_fmt))

        # 字符串
        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#CE9178"))
        self._rules.append((re.compile(r'"[^"]*"'), str_fmt))

        # 数字
        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#B5CEA8"))
        self._rules.append((re.compile(r"\b\d+\.?\d*\b"), num_fmt))

        # 注释
        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor("#6A9955"))
        comment_fmt.setFontItalic(True)
        self._rules.append((re.compile(r"'.*$", re.MULTILINE), comment_fmt))

        # CATIA 对象
        catia_fmt = QTextCharFormat()
        catia_fmt.setForeground(QColor("#4EC9B0"))
        self._rules.append((re.compile(
            r"\b(CATIA|Part|Body|Sketch|ShapeFactory|HybridShapeFactory|"
            r"Factory2D|Pad|Pocket|Hole|EdgeFillet|Chamfer|Selection|"
            r"Document|Product|Parameters|Reference)\b"
        ), catia_fmt))

    def highlightBlock(self, text: str):
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


class PythonHighlighter(QSyntaxHighlighter):
    """Python 语法高亮。"""

    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self._rules: list[tuple[re.Pattern, QTextCharFormat]] = []

        kw_fmt = QTextCharFormat()
        kw_fmt.setForeground(QColor("#569CD6"))
        kw_fmt.setFontWeight(QFont.Bold)
        keywords = (
            r"\b(def|class|if|elif|else|for|while|return|import|from|as|"
            r"with|try|except|finally|raise|pass|break|continue|and|or|"
            r"not|in|is|None|True|False|lambda|yield|global|nonlocal)\b"
        )
        self._rules.append((re.compile(keywords), kw_fmt))

        str_fmt = QTextCharFormat()
        str_fmt.setForeground(QColor("#CE9178"))
        self._rules.append((re.compile(r'(?:"[^"]*"|\'[^\']*\')'), str_fmt))

        num_fmt = QTextCharFormat()
        num_fmt.setForeground(QColor("#B5CEA8"))
        self._rules.append((re.compile(r"\b\d+\.?\d*\b"), num_fmt))

        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor("#6A9955"))
        comment_fmt.setFontItalic(True)
        self._rules.append((re.compile(r"#.*$", re.MULTILINE), comment_fmt))

        func_fmt = QTextCharFormat()
        func_fmt.setForeground(QColor("#DCDCAA"))
        self._rules.append((re.compile(r"\b\w+(?=\()"), func_fmt))

    def highlightBlock(self, text: str):
        for pattern, fmt in self._rules:
            for m in pattern.finditer(text):
                self.setFormat(m.start(), m.end() - m.start(), fmt)


class LineNumberArea(QWidget):
    """行号侧边栏。"""

    def __init__(self, editor: CodeEditor):
        super().__init__(editor)
        self._editor = editor
        self.setObjectName("lineNumberArea")

    def sizeHint(self):
        return self._editor.line_number_area_size()

    def paintEvent(self, event):
        self._editor.paint_line_numbers(event)


class CodeEditor(QPlainTextEdit):
    """带行号的代码编辑器。"""

    file_dropped = pyqtSignal(str)  # 拖入文件时发射文件路径

    def __init__(self, parent=None, read_only=False):
        super().__init__(parent)
        self._line_area = LineNumberArea(self)
        self._read_only = read_only

        self.blockCountChanged.connect(self._update_line_area_width)
        self.updateRequest.connect(self._update_line_area)

        self._update_line_area_width()

        if read_only:
            self.setReadOnly(True)
            self.setObjectName("codePreview")
        else:
            self.setObjectName("codeEditor")
            self.setAcceptDrops(True)

        self.setTabStopDistance(QFontMetrics(self.font()).horizontalAdvance(" ") * 4)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

    def dragEnterEvent(self, event):
        if not self._read_only and event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if not self._read_only and event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        """拦截文件拖拽，读取文件内容而非插入路径。"""
        mime = event.mimeData()
        if not self._read_only and mime.hasUrls():
            path = mime.urls()[0].toLocalFile()
            if path:
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        self.setPlainText(f.read())
                    self.file_dropped.emit(path)
                except OSError:
                    pass
                event.acceptProposedAction()
                return
        super().dropEvent(event)

    def line_number_area_size(self):
        digits = max(1, len(str(self.blockCount())))
        return QFontMetrics(self.font()).horizontalAdvance("9") * (digits + 2) + 12

    def _update_line_area_width(self):
        self.setViewportMargins(self.line_number_area_size(), 0, 0, 0)

    def _update_line_area(self, rect, dy):
        if dy:
            self._line_area.scroll(0, dy)
        else:
            self._line_area.update(0, rect.y(), self._line_area.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._update_line_area_width()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self._line_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_size(), cr.height())
        )

    def paint_line_numbers(self, event):
        painter = QPainter(self._line_area)
        painter.fillRect(event.rect(), QColor("#252526"))

        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QColor("#858585"))
                painter.drawText(
                    0, top, self._line_area.width() - 8,
                    self.fontMetrics().height(),
                    Qt.AlignRight | Qt.AlignVCenter,
                    str(block_num + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_num += 1

        painter.end()


class MacroEditorPanel(QFrame):
    """宏代码编辑面板 — 包含标题、编辑器、操作按钮。"""

    analyze_requested = pyqtSignal(str)  # 发射宏代码文本

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._highlighter = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题栏
        header = QHBoxLayout()
        header.setContentsMargins(16, 12, 16, 8)

        title = QLabel("宏代码")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        open_btn = QPushButton("打开文件")
        open_btn.setFixedHeight(28)
        open_btn.clicked.connect(self._open_file)
        header.addWidget(open_btn)

        layout.addLayout(header)

        # 代码编辑器
        self._editor = CodeEditor(self)
        self._editor.setPlaceholderText("在此粘贴 CATIA 宏代码，或拖拽文件到此处...")
        self._editor.file_dropped.connect(self._on_file_dropped)
        layout.addWidget(self._editor, 1)

        # 底部按钮区
        footer = QHBoxLayout()
        footer.setContentsMargins(12, 8, 12, 12)

        hint = QLabel("支持 .CATScript / .py 文件")
        hint.setObjectName("hintLabel")
        footer.addWidget(hint)
        footer.addStretch()

        analyze_btn = QPushButton("分析参数")
        analyze_btn.setObjectName("analyzeButton")
        analyze_btn.setFixedHeight(34)
        analyze_btn.clicked.connect(self._on_analyze)
        footer.addWidget(analyze_btn)

        layout.addLayout(footer)

        # 拖拽支持
        self.setAcceptDrops(True)

    def get_code(self) -> str:
        return self._editor.toPlainText()

    def set_code(self, code: str):
        self._editor.setPlainText(code)
        self._update_highlighter(code)

    def _update_highlighter(self, code: str):
        """根据代码内容自动切换语法高亮。"""
        from core.macro_engine import detect_language
        lang = detect_language(code)
        if self._highlighter:
            self._highlighter.setDocument(None)
        if lang == "python":
            self._highlighter = PythonHighlighter(self._editor.document())
        else:
            self._highlighter = VBScriptHighlighter(self._editor.document())

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "打开宏文件", "",
            "CATIA宏 (*.CATScript *.catvbs);;Python (*.py);;所有文件 (*)"
        )
        if path:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                self.set_code(f.read())

    def _on_analyze(self):
        code = self.get_code().strip()
        if code:
            self.analyze_requested.emit(code)

    def _on_file_dropped(self, path: str):
        """文件拖入后更新语法高亮。"""
        self._update_highlighter(self._editor.toPlainText())
