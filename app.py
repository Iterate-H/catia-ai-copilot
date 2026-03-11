"""CATIA 宏参数化工具 — PyQt5 桌面应用入口。"""

import os
import sys

# Fix: Qt platform plugin not found on Windows
if sys.platform == "win32":
    import pathlib
    venv_qt = pathlib.Path(sys.prefix) / "Lib" / "site-packages" / "PyQt5" / "Qt5" / "plugins"
    if venv_qt.exists():
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = str(venv_qt / "platforms")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow
from ui.styles import STYLESHEET


def main():
    # macOS 高 DPI 支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setApplicationName("CATIA 宏参数化工具")
    app.setStyleSheet(STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
