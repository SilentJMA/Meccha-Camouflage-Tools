#!/usr/bin/env python3
"""Standalone camouflage-only entry point for MecchaCamouflage.exe."""
import sys
import os
import ctypes

# Keep the camouflage-only build consistent with the full application's DPI
# behavior.  These must be set before importing Qt.
os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
os.environ.setdefault("QT_SCALE_FACTOR_ROUNDING_POLICY", "PassThrough")

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

from meccha_chameleon_tools.core import MecchaESP
from meccha_chameleon_tools.config import Config, load_config, save_config
from meccha_chameleon_tools.ui import Menu


def camo_main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except (AttributeError, TypeError):
        pass
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(-4)
    except Exception:
        pass
    app = QApplication(sys.argv)
    font = QFont("Segoe UI")
    font.setPointSizeF(10.0)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)

    config = load_config()
    try:
        esp = MecchaESP()
    except (RuntimeError, Exception) as e:
        QMessageBox.critical(
            None, "Game Not Found",
            f"Could not connect to the game.\n\n"
            f"Make sure the game is running before launching.\n\n"
            f"Error: {e}"
        )
        sys.exit(1)

    menu = Menu(config, esp, tabs=["Camouflage"])
    menu.setWindowTitle("Meccha Camouflage")
    menu.show()
    app.aboutToQuit.connect(lambda: (save_config(config), esp.cleanup()))
    sys.exit(app.exec_())


if __name__ == "__main__":
    camo_main()
