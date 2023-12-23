from myglobal import *
from PySide6.QtWidgets import (QLineEdit, QPushButton, QFrame)
class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Raised)
class fieldButton(QPushButton):
    def __init__(self, f, i, text = "Открыть"):
        super(fieldButton, self).__init__()
        self.setText(text)
        self.clicked.connect(lambda: f(i))
def createLineEdit(f, i, price):
    t = QLineEdit()
    t.setText("0")
    t.textChanged.connect(lambda: f(i, t.text(), price))
    return t