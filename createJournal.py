import sys, system, sqlite3
from myglobal import *
from datetime import datetime
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QTextEdit,
    QVBoxLayout, QDialog, QGroupBox, QMainWindow, QRadioButton,
    QFileDialog, QWidget, QDateEdit, QLabel, QGridLayout,
    QDialogButtonBox, QMessageBox, QFrame
    )
def createLineEdit(f, i, price):
    t = QLineEdit()
    t.setText("0")
    t.textChanged.connect(lambda: f(i, t.text(), price))
    return t
class JournalForm(QDialog):
    def __init__(self, userId):
        super(JournalForm, self).__init__()
        self.userId = userId
        self.editName = QLineEdit()
        self.setWindowTitle("Создание журнала")
        self.editName.setPlaceholderText("Название")
        self.createButton = QPushButton("Создать")
        self.createButton.clicked.connect(self.createJournal)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.editName)
        layout.addWidget(self.createButton)
        # Set dialog layout
        self.setLayout(layout)
    def createJournal(self):
        with sqlite3.connect(database) as db:
                journalName = self.editName.text()
                try:
                    cursor = db.cursor()
                    query = f"""INSERT INTO journal (user_id, name, create_date, change_date) VALUES("{self.userId}", "{journalName}", {int(datetime.timestamp(datetime.now()))}, {int(datetime.timestamp(datetime.now()))})"""
                    if journalName == "":
                        raise Exception("syntax")
                    cursor.execute(query)

                    # query = f"""INSERT INTO field (user_id, dung) VALUES({id}, 0)"""
                    # cursor.execute(query)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Журнал создан!")
                    msg.setWindowTitle("Успех")
                    msg.exec_()
                    system.createJournalLog(cursor, self.userId, cursor.lastrowid)
                except Exception as e:
                    ms = str(e)
                    if "syntax" in ms:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Обнаружены пустые поля!")
                        msg.setInformativeText('Заполните все представленные поля')
                        msg.setWindowTitle("Ошибка")
                        msg.exec_()
                    elif "UNIQUE" in ms:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Название занято")
                        msg.setInformativeText('Используйте другое имя для создания')
                        msg.setWindowTitle("Ошибка")
                        msg.exec_()
                    else:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("Неопознанная ошибка")
                        msg.setWindowTitle("Ошибка")
                        msg.exec_()
                        print(e)