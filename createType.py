import system, sqlite3
from myglobal import *
from supportClass import *
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QTextEdit,
    QVBoxLayout, QDialog, QGroupBox, QMainWindow, QRadioButton,
    QFileDialog, QWidget, QDateEdit, QLabel, QGridLayout,
    QDialogButtonBox, QMessageBox, QFrame
    )
class TypeForm(QDialog):
    def __init__(self, userId, journalId):
        super(TypeForm, self).__init__()
        self.userId = userId
        self.journalId = journalId
        self.editName = QLineEdit()
        self.setWindowTitle("Создание типа")
        self.editName.setPlaceholderText("Название")
        self.createButton = QPushButton("Создать")
        self.createButton.clicked.connect(self.createLogType)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.editName)
        layout.addWidget(self.createButton)
        # Set dialog layout
        self.setLayout(layout)
    def createLogType(self):
        with sqlite3.connect(database) as db:
                typeName = self.editName.text()
                try:
                    cursor = db.cursor()
                    query = f"""INSERT INTO log_type (journal_id, type) VALUES("{self.journalId}", "{typeName}")"""
                    if typeName == "":
                        raise Exception("syntax")
                    cursor.execute(query)
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Тип события создан!")
                    msg.setWindowTitle("Успех")
                    msg.exec_()
                    system.createTypelLog(cursor, self.userId, self.journalId, typeName)
                    system.setChangeDate(cursor, self.journalId)
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