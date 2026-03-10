"""参数面板 — 根据AI提取的参数列表，动态生成输入控件。"""

from __future__ import annotations

from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QWidget, QDoubleSpinBox, QSpinBox, QLineEdit, QCheckBox,
    QComboBox, QPushButton, QSizePolicy, QProgressBar,
)


class ParamPanel(QFrame):
    """参数面板 — 动态生成参数输入控件。"""

    params_applied = pyqtSignal(dict)   # {param_name: new_value}
    run_requested = pyqtSignal(dict)    # 运行建模

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self._params: list[dict] = []
        self._widgets: dict[str, QWidget] = {}  # name → input widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 标题
        title = QLabel("参数面板")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # 滚动区域
        self._scroll = QScrollArea()
        self._scroll.setObjectName("paramScroll")
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._container = QWidget()
        self._container.setObjectName("paramContainer")
        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(12, 8, 12, 8)
        self._container_layout.setSpacing(8)

        # 空状态
        self._empty_label = QLabel("上传宏代码后\n点击「分析参数」提取可调参数")
        self._empty_label.setObjectName("emptyState")
        self._empty_label.setAlignment(Qt.AlignCenter)
        self._container_layout.addWidget(self._empty_label)
        self._container_layout.addStretch()

        self._scroll.setWidget(self._container)
        layout.addWidget(self._scroll, 1)

        # 底部按钮区
        self._btn_frame = QFrame()
        btn_layout = QVBoxLayout(self._btn_frame)
        btn_layout.setContentsMargins(12, 8, 12, 12)
        btn_layout.setSpacing(6)

        self._apply_btn = QPushButton("应用参数")
        self._apply_btn.clicked.connect(self._on_apply)
        btn_layout.addWidget(self._apply_btn)

        self._run_btn = QPushButton("运行建模")
        self._run_btn.setObjectName("primaryButton")
        self._run_btn.clicked.connect(self._on_run)
        btn_layout.addWidget(self._run_btn)

        self._btn_frame.setVisible(False)
        layout.addWidget(self._btn_frame)

    def show_loading(self, text: str = "正在分析..."):
        """显示加载状态。"""
        # 清除旧控件
        while self._container_layout.count():
            item = self._container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 加载提示
        loading_widget = QWidget()
        loading_layout = QVBoxLayout(loading_widget)
        loading_layout.setAlignment(Qt.AlignCenter)
        loading_layout.setSpacing(16)

        progress = QProgressBar()
        progress.setRange(0, 0)  # 无限滚动
        progress.setFixedWidth(200)
        progress.setFixedHeight(4)
        progress.setTextVisible(False)
        progress.setStyleSheet("""
            QProgressBar { background: #E8E5E0; border: none; border-radius: 2px; }
            QProgressBar::chunk { background: #D97706; border-radius: 2px; }
        """)
        loading_layout.addWidget(progress, 0, Qt.AlignCenter)

        label = QLabel(text)
        label.setObjectName("emptyState")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 13px; color: #787774; padding: 0;")
        loading_layout.addWidget(label)

        self._container_layout.addStretch()
        self._container_layout.addWidget(loading_widget)
        self._container_layout.addStretch()
        self._btn_frame.setVisible(False)

    def hide_loading(self):
        """隐藏加载状态（set_parameters 会清理）。"""
        pass

    def set_parameters(self, params: list[dict]):
        """根据参数列表生成输入控件。"""
        self._params = params
        self._widgets.clear()

        # 清除旧控件
        while self._container_layout.count():
            item = self._container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not params:
            self._empty_label = QLabel("未提取到可调参数")
            self._empty_label.setObjectName("emptyState")
            self._empty_label.setAlignment(Qt.AlignCenter)
            self._container_layout.addWidget(self._empty_label)
            self._container_layout.addStretch()
            self._btn_frame.setVisible(False)
            return

        for p in params:
            row = self._create_param_row(p)
            self._container_layout.addWidget(row)

        self._container_layout.addStretch()
        self._btn_frame.setVisible(True)

    def _create_param_row(self, param: dict) -> QFrame:
        """创建单个参数输入行。"""
        row = QFrame()
        row.setObjectName("paramRow")
        layout = QVBoxLayout(row)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)

        # 标签行：中文名
        label_layout = QHBoxLayout()
        label_layout.setSpacing(6)

        label = QLabel(param.get("label", param["name"]))
        label.setObjectName("paramLabel")
        label_layout.addWidget(label)

        unit = param.get("unit", "")
        if unit:
            unit_label = QLabel(unit)
            unit_label.setObjectName("paramUnit")
            label_layout.addWidget(unit_label)

        label_layout.addStretch()

        # 重置按钮
        reset_btn = QPushButton("重置")
        reset_btn.setFixedSize(40, 22)
        reset_btn.setStyleSheet("font-size: 11px; padding: 2px 6px; min-height: 20px;")
        label_layout.addWidget(reset_btn)

        layout.addLayout(label_layout)

        # 输入控件
        ptype = param.get("type", "float")
        default = param.get("default")
        widget = self._create_input_widget(param, ptype, default)
        self._widgets[param["name"]] = widget
        layout.addWidget(widget)

        # 重置功能
        reset_btn.clicked.connect(lambda _, w=widget, d=default, t=ptype: self._reset_value(w, d, t))

        return row

    def _create_input_widget(self, param: dict, ptype: str, default) -> QWidget:
        """根据参数类型创建对应输入控件。"""
        if ptype == "float":
            w = QDoubleSpinBox()
            w.setDecimals(3)
            w.setRange(
                param.get("min") if param.get("min") is not None else -99999.0,
                param.get("max") if param.get("max") is not None else 99999.0,
            )
            if param.get("step"):
                w.setSingleStep(param["step"])
            else:
                w.setSingleStep(0.1)
            if default is not None:
                w.setValue(float(default))
            return w

        if ptype == "int":
            w = QSpinBox()
            w.setRange(
                int(param.get("min")) if param.get("min") is not None else -99999,
                int(param.get("max")) if param.get("max") is not None else 99999,
            )
            if param.get("step"):
                w.setSingleStep(int(param["step"]))
            if default is not None:
                w.setValue(int(default))
            return w

        if ptype == "bool":
            w = QCheckBox()
            if default is not None:
                w.setChecked(bool(default))
            return w

        if ptype == "enum" and isinstance(default, list):
            w = QComboBox()
            w.addItems([str(v) for v in default])
            return w

        # string 或其他
        w = QLineEdit()
        if default is not None:
            w.setText(str(default))
        w.setPlaceholderText(f"输入 {param.get('label', param['name'])}")
        return w

    def _reset_value(self, widget: QWidget, default, ptype: str):
        """重置参数到默认值。"""
        if isinstance(widget, QDoubleSpinBox):
            widget.setValue(float(default) if default is not None else 0.0)
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(default) if default is not None else 0)
        elif isinstance(widget, QCheckBox):
            widget.setChecked(bool(default) if default is not None else False)
        elif isinstance(widget, QLineEdit):
            widget.setText(str(default) if default is not None else "")

    def get_values(self) -> dict:
        """获取当前所有参数的值。"""
        values = {}
        for name, widget in self._widgets.items():
            if isinstance(widget, QDoubleSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QSpinBox):
                values[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                values[name] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                values[name] = widget.currentText()
            elif isinstance(widget, QLineEdit):
                values[name] = widget.text()
        return values

    def _on_apply(self):
        self.params_applied.emit(self.get_values())

    def _on_run(self):
        self.run_requested.emit(self.get_values())

