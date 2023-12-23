import sys, system, sqlite3
from myglobal import *
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
class ProfileForm(QDialog):
    def __init__(self, callback):
        super(ProfileForm, self).__init__()
        self.callback = callback
        self.edit_name = QLineEdit()
        self.setWindowTitle("Профиль")
        self.edit_name.setPlaceholderText("Логин")

        self.edit_password = QLineEdit()
        self.edit_password.setPlaceholderText("Пароль")
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.profile_create = QPushButton("Создать")
        self.profile_create.clicked.connect(self.create_user)
        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.edit_name)
        layout.addWidget(self.edit_password)
        layout.addWidget(self.profile_create)
        layout.addWidget(self.buttonBox)
        # Set dialog layout
        self.setLayout(layout)
    def create_user(self):
        with sqlite3.connect(database) as db:
            try:
                username = self.edit_name.text()
                password = self.edit_password.text()
                cursor = db.cursor()
                query = f"""INSERT INTO user (name, password) VALUES("{username}", "{password}")"""
                if username == "" or password == "":
                    raise Exception("syntax")
                cursor.execute(query)
                id = cursor.lastrowid
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Пользователь создан!")
                msg.setWindowTitle("Успех")
                msg.exec_()
                system.createUserLog(cursor, id)
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
                    msg.setText("Логин занят")
                    msg.setInformativeText('Используйте другое имя для создания профиля')
                    msg.setWindowTitle("Ошибка")
                    msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Неопознанная ошибка")
                    msg.setWindowTitle("Ошибка")
                    msg.exec_()
                    print(e)
    def __del__(self):
        self.callback(self.edit_name.text(), self.edit_password.text())