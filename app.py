from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
from main_window import MainWindow
from PySide6.QtWidgets import QMessageBox
import sys

if __name__ == "__main__":
    app = QApplication([])
    shared = QSharedMemory("G00dV1b3s-F33!s")
    if not shared.create(1):
        QMessageBox.warning(None, "Application Status", "The Application is already running.")
        sys.exit(0)
    else:
        main_window = MainWindow()
        main_window.show()
        app.exec()