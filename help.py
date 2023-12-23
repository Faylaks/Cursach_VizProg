from supportClass import *
from PySide6.QtCore import Qt, QDate, QUrl
from PySide6.QtWidgets import (QVBoxLayout, QDialog, QWidget, QLabel, QTabWidget, QScrollArea, QPushButton)
from PySide6.QtWebEngineWidgets import QWebEngineView

class helpForm(QDialog):
    def __init__(self):
        super(helpForm, self).__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle("Справка")
        self.browser = QWebEngineView()
        self.browser.load(QUrl(helpfile))
        l = QVBoxLayout()
        l.addWidget(self.browser)
        self.setLayout(l)