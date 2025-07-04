from PySide6.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication([])
    print("Good Vibes - The Feels Salon Application")
    main_window = MainWindow()
    main_window.show()
    app.exec()