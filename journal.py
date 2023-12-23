import system, sqlite3
from myglobal import *
from supportClass import *
from datetime import datetime
from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QTextEdit,
    QVBoxLayout, QDialog, QGroupBox, QMainWindow, QRadioButton,
    QFileDialog, QWidget, QDateEdit, QLabel, QGridLayout,
    QDialogButtonBox, QMessageBox, QFrame, QScrollArea
    )


class JournalScroll(QScrollArea):
    def __init__(self, callbackOpen, callbackCreate):
        super(JournalScroll, self).__init__()
        layout = QVBoxLayout()
        self.journal = Journal(callbackOpen, callbackCreate)
        # layout.addWidget(self.journal)
        self.setWidgetResizable(True)
        self.setWidgetResizable(True)
        self.setWidget(self.journal)


class Journal(QWidget):
    def __init__(self, callbackOpen, callbackCreate):
        super(Journal, self).__init__()
        self.newJournalName = ""
        self.callbackOpen = callbackOpen
        self.callbackCreate = callbackCreate
        self.journalLayout = QGridLayout()
        self.journalLayout.addWidget(QLabel("Название"), 0, 0, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Дата Создания"), 0, 1, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Дата Изменения"), 0, 2, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.journalLayout)
        self.journals = []
        self.getUserJournal()
        self.journalUpdate()
    def journalUpdate(self):
        for i in reversed(range(self.journalLayout.count())): 
            self.journalLayout.itemAt(i).widget().setParent(None)
        self.journalLayout.addWidget(QLabel("Название", objectName="table_header"), 0, 0, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Дата Создания", objectName="table_header"), 0, 1, Qt.AlignmentFlag.AlignTop)
        self.journalLayout.addWidget(QLabel("Дата Изменения", objectName="table_header"), 0, 2, Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.journalLayout)
        self.buttons = []
        self.getUserJournal()
        for i, journal in enumerate(self.journals):
            self.buttons.append(fieldButton(self.openJournal, i))
            self.journalLayout.addWidget(QHLine(), (i + 1) * 2, 0, 1, 4, Qt.AlignmentFlag.AlignTop)
            self.journalLayout.addWidget(QLabel(journal[0]), (i + 1) * 2 - 1, 0, Qt.AlignmentFlag.AlignTop)
            self.journalLayout.addWidget(QLabel(str(datetime.fromtimestamp(journal[1]).strftime("%D %H:%M:%S"))), (i + 1) * 2 - 1, 1, Qt.AlignmentFlag.AlignTop)
            self.journalLayout.addWidget(QLabel(str(datetime.fromtimestamp(journal[2]).strftime("%D %H:%M:%S"))), (i + 1) * 2 - 1, 2, Qt.AlignmentFlag.AlignTop)
            self.journalLayout.addWidget(self.buttons[i], (i + 1) * 2 - 1, 3, Qt.AlignmentFlag.AlignTop)
        self.createButton = QPushButton("Создать")
        self.createButton.clicked.connect(self.createJournal)
        self.journalLayout.addWidget(self.createButton, len(self.journals) * 2 + 1, 0)
    def createJournal(self):
        self.callbackCreate()
        self.journalUpdate()
    def openJournal(self, id):
        self.callbackOpen(self.journals[id][3])
        self.journalUpdate()
    def getUserJournal(self):
        with sqlite3.connect(database) as db:
            cursor = db.cursor()
            query = f"""SELECT name, create_date, change_date, id FROM journal"""
            cursor.execute(query)
            self.journals = cursor.fetchall()
            