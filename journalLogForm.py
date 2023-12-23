import createType, system, sqlite3
from myglobal import *
from datetime import datetime
from supportClass import *
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QTextEdit,
    QVBoxLayout, QDialog, QGroupBox, QMainWindow, QRadioButton,
    QFileDialog, QWidget, QDateEdit, QLabel, QGridLayout,
    QDialogButtonBox, QMessageBox, QFrame, QComboBox
    )
class EventForm(QDialog):
    def __init__(self, userId, journalId):
        super(EventForm, self).__init__()
        self.userId = userId
        self.journalId = journalId
        self.types = []
        self.editType = QComboBox()
        self.editType.setPlaceholderText("Тип")
        self.getTypes()
        self.setWindowTitle("Типы и события")
        self.deleteButton = QPushButton("Удалить тип")
        self.editType.currentIndexChanged.connect(lambda: self.deleteButton.setEnabled(True))
        self.deleteButton.setEnabled(False)
        self.deleteButton.clicked.connect(self.deleteType)
        self.createButton = QPushButton("Добавить тип")
        self.createButton.clicked.connect(self.createType)
        self.createLogButton = QPushButton("Создать")
        self.createLogButton.clicked.connect(self.createLog)
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.editType)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.createButton)
        layout.addWidget(self.createLogButton)
        # Set dialog layout
        self.setLayout(layout)
    # def comboBoxChanged(self, value):
        
    def deleteType(self):
        if self.editType.currentText() == "":
            self.deleteButton.setEnabled(False)
            return
        ret = QMessageBox.question(self,'Внимание', "При удалении типа исчезнут все события! Продолжить?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            return
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            query = f"""DELETE FROM log_type WHERE type = "{self.editType.currentText()}" """
            cursor.execute(query)
            system.deleteTypeLog(cursor, self.userId, self.journalId, self.editType.currentText())
        self.getTypes()
    def getTypes(self):
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            query = f"""SELECT type FROM log_type WHERE journal_id = {self.journalId}"""
            cursor.execute(query)
            self.types = list(map(''.join, cursor.fetchall()))
        self.editType.clear()
        self.editType.addItems(self.types)
    def createLog(self):
        typeName = self.editType.currentText()
        if typeName == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Укажите тип!")
            msg.setWindowTitle("Ошибка")
            msg.exec_()
            return
        with sqlite3.connect(database) as db:
                cursor = db.cursor()
                query = f"""SELECT id FROM log_type WHERE (journal_id = "{self.journalId}" AND type = "{typeName}")"""
                cursor.execute(query)
                typeId = cursor.fetchone()[0]
                query = f"""INSERT INTO log (user_id, journal_id, type_id, date) VALUES({self.userId}, {self.journalId}, {typeId}, {int(datetime.timestamp(datetime.now()))})"""
                cursor.execute(query)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Событие создано!")
                msg.setWindowTitle("Успех")
                msg.exec_()
                system.createEventlLog(cursor, self.userId, self.journalId, typeName)
                system.setChangeDate(cursor, self.journalId)
    def createType(self):
        dlg = createType.TypeForm(self.userId, self.journalId)
        dlg.exec()
        self.getTypes()
