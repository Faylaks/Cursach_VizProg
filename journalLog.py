import journalLogForm, system, sqlite3
from myglobal import *
from datetime import datetime
import re
from tabulate import tabulate
from supportClass import *
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout, QDialog, QWidget, QLabel, 
    QGridLayout, QMessageBox, QScrollArea, QFileDialog
    )
class JournalLogDialog(QDialog):
    def __init__(self, userId, journalId):
        super(JournalLogDialog, self).__init__()
        #Параметры окна
        self.setWindowTitle("События")
        self.setFixedSize(600, 400)
        #Отрисовка Содержимого
        layout = QVBoxLayout()
        self.journalScroll = JournalLogScroll(userId, journalId, self.accept)
        layout.addWidget(self.journalScroll)
        self.setLayout(layout)
class JournalLogScroll(QScrollArea):
    def __init__(self, userId, journalId, closeCallback):
        super(JournalLogScroll, self).__init__()
        self.journal = JournalLog(userId, journalId, closeCallback)
        self.setWidgetResizable(True)
        self.setWidgetResizable(True)
        self.setWidget(self.journal)
class JournalLog(QWidget):
    def __init__(self, userId, journalId, closeCallback):
        super(JournalLog, self).__init__()
        self.closeCallback = closeCallback
        self.newJournalName = ""
        self.userId = userId
        self.journalId = journalId
        self.journalLayout = QGridLayout()
        self.journalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.journalLayout)
        self.logs = []
        self.getUserJournalLog()
        self.journalUpdate(self.userId, self.journalId)
    def journalUpdate(self, userId, journalId):
        isSystem = 1 if self.journalId == systemJournalId else 0
        self.userId = userId
        self.journalId = journalId
        for i in reversed(range(self.journalLayout.count())): 
            self.journalLayout.itemAt(i).widget().setParent(None)
        self.journalLayout.addWidget(QLabel("Пользователь", objectName="table_header"), 0, 0, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Тип", objectName="table_header"), 0, 1, Qt.AlignmentFlag.AlignTop)
        if isSystem:
            self.journalLayout.addWidget(QLabel("Дополнительно", objectName="table_header"), 0, 2, Qt.AlignmentFlag.AlignTop)
        else:
            self.journalLayout.addWidget(QLabel("", objectName="table_header"), 0, 3, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Дата", objectName="table_header"), 0, 2 + isSystem, Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.journalLayout)

        self.buttons = []
        self.getUserJournalLog()
        for i, log in enumerate(self.logs):
            self.buttons.append(fieldButton(self.deleteLog, i, "Удалить"))
            self.journalLayout.addWidget(QHLine(), (i + 1) * 2, 0, 1, 4, Qt.AlignmentFlag.AlignTop)
            for j in range(2 + isSystem):
                self.journalLayout.addWidget(QLabel(log[j] if log[j] else "---"), (i + 1) * 2 - 1, j, Qt.AlignmentFlag.AlignTop)
            self.journalLayout.addWidget(QLabel(str(datetime.fromtimestamp(log[3]).strftime("%D %H:%M:%S"))), (i + 1) * 2 - 1, 2 + isSystem, Qt.AlignmentFlag.AlignTop)
            if self.journalId != systemJournalId:
                self.journalLayout.addWidget(self.buttons[i], (i + 1) * 2 - 1, 3 + isSystem, Qt.AlignmentFlag.AlignTop)
        self.createButton = QPushButton("Создать")
        self.createButton.clicked.connect(self.createLog)
        self.clearButton = QPushButton("Очистить")
        self.clearButton.clicked.connect(self.clearLog)
        self.deleeteJournalButton = QPushButton("Удалить журнал")
        self.deleeteJournalButton.clicked.connect(self.deleteJournal)
        if self.logs:
            self.outputButton = QPushButton("Выгрузить")
            self.outputButton.clicked.connect(self.output)
            self.journalLayout.addWidget(self.outputButton, len(self.logs) * 2 + 1, 3)
        elif isSystem == 0:
            self.outputButton = QPushButton("Загрузить")
            self.outputButton.clicked.connect(self.input)
            self.journalLayout.addWidget(self.outputButton, len(self.logs) * 2 + 1, 3)
        if isSystem == 0:
            self.journalLayout.addWidget(self.createButton, len(self.logs) * 2 + 1, 0)
            self.journalLayout.addWidget(self.deleeteJournalButton, len(self.logs) * 2 + 1, 2)
            self.journalLayout.addWidget(self.clearButton, len(self.logs) * 2 + 1, 1)
        else:
            self.journalLayout.addWidget(self.clearButton, len(self.logs) * 2 + 1, 0)
    def input(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open File", ".", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, "r") as file:
                all = file.readlines()[2:]
                all = [list(filter(None, a.split("  "))) for a in all]
                for a in all:
                    a[1] = a[1].strip()
                    a[2] = a[2].replace("\n", "").strip()
        
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            for a in all:
                typeName = a[1]
                query = f"""SELECT id FROM log_type WHERE (journal_id = "{self.journalId}" AND type = "{typeName}")"""
                cursor.execute(query)
                aaa = cursor.fetchone()
                if  aaa is not None:
                    typeId = aaa[0]
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Отсутвуют типы!")
                    msg.setWindowTitle("Ошибка")
                    msg.exec_()
                    return
                query = f"""INSERT INTO log (user_id, journal_id, type_id, date) VALUES({self.userId}, {self.journalId}, {typeId}, {int(datetime.timestamp(datetime.now()))})"""
                cursor.execute(query)
                system.createEventlLog(cursor, self.userId, self.journalId, typeName)
                system.setChangeDate(cursor, self.journalId)
        self.journalUpdate(self.userId, self.journalId)
    def output(self):
        table = tabulate([[log[0], log[1], str(datetime.fromtimestamp(log[3]).strftime("%D %H:%M:%S"))] for log in self.logs], ["Пользователь", "Тип", "Дата"])      
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, "w") as file:
                file.write(table)

    def deleteJournal(self):
        ret = QMessageBox.question(self, 'Внимание', "При удалении журнала исчезнут все события! Продолжить?", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.No:
            return
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            system.deleteJournalLog(cursor, self.userId, self.journalId)
            query = f"""DELETE FROM journal WHERE id = "{self.journalId}" """
            cursor.execute(query)
        self.closeCallback()
    def clearLog(self):
        if not(self.logs):
            return
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            query = f"""DELETE FROM log WHERE journal_id = {self.journalId}"""
            cursor.execute(query)
            if self.journalId != systemJournalId:
                system.clearEventLog(cursor, self.userId, self.journalId) # Добавление системный журнал
        self.logs = []
        self.journalUpdate(self.userId, self.journalId)
    def deleteLog(self, eventId):
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            query = f"""DELETE FROM log WHERE id = {self.logs[eventId][4]}"""
            cursor.execute(query)
            if self.journalId != systemJournalId:
                system.deleteEventLog(cursor, self.userId, self.journalId, self.logs[eventId][1]) # Добавление системный журнал
            system.setChangeDate(cursor, self.journalId)
        self.logs = []
        self.journalUpdate(self.userId, self.journalId)
    def createLog(self):
        dlg = journalLogForm.EventForm(self.userId, self.journalId)
        dlg.exec()
        self.journalUpdate(self.userId, self.journalId)
    def getUserJournalLog(self):
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            query = f"""SELECT user.name, log_type.type, external, date, log.id FROM log
                        LEFT JOIN user, log_type ON log.user_id = user.id AND log.type_id = log_type.id WHERE log.journal_id = {self.journalId}"""
            cursor.execute(query)
            self.logs = cursor.fetchall()            