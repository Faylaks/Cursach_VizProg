import sys
from mystyle import style
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog, QMainWindow, QDialogButtonBox, QMessageBox)
from myapp import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec())