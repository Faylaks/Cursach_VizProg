import createJournal, journalLog, help, journal, myprofile, system, sqlite3, webbrowser
from myglobal import *
from PySide6.QtCore import Qt, QDate, QTimer, QSettings
from PySide6.QtGui import QAction
from datetime import datetime
from PySide6.QtWidgets import (
    QLineEdit, QPushButton, QApplication, QTextEdit,
    QVBoxLayout, QDialog, QGroupBox, QMainWindow, QRadioButton,
    QFileDialog, QWidget, QDateEdit, QLabel, QGridLayout,
    QDialogButtonBox, QMessageBox, QTabWidget, QScrollArea
    )

def getCriticalMsg(text):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle("Ошибка")
    msg.exec_()
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # Инициализация переменных
        self.paren = parent
        self.shopData = []
        self.journalId = 0
        self.userName = "Гость"
        self.userPassword = ""
        self.userId = 1
        self.userSemen = []
        self.enter = True
        self.darkTheme = True
        #Наследование от родительского класса QMainWindow
        super().__init__()
        layout = QGridLayout()
        #Создание меню
        mainMenu = self.menuBar()
        #Добавдение кнопок меню для смены пользователя 
        self.profileButton  = QAction(self.userName, mainMenu)
        mainMenu.addAction(self.profileButton)
        self.profileButton.triggered.connect(self.openProfile)
        self.logout = QAction('Выход', mainMenu)
        mainMenu.addAction(self.logout)
        #Добавдение кнопок меню
        self.logout.setVisible(False)
        self.logout.triggered.connect(lambda: self.changeUser('Гость', 'Гость', True))
        #Добавдение кнопок справки
        helpMenu = QAction("Справка", mainMenu)
        helpMenu.setToolTip("Справка")
        helpMenu.triggered.connect(self.openHelp)
        mainMenu.addAction(helpMenu)
        #Параметры окна
        self.setWindowTitle("Журнал Событий")
        self.setFixedSize(600, 400)
        #Создание Вкладок
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        #Создание таймера
        self.currTimeLabel = QLabel(datetime.now().strftime("%D %H:%M:%S"))
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeUpdate)
        self.timer.start(1000)
        self.changeUser('Гость', 'Гость')

        self.journalScroll = journal.JournalScroll(self.openJournal, self.createJournal)
        self.tabs.addTab(self.journalScroll, "Журналы")
        # Отрисовка вкладок
        layout.addWidget(self.tabs, 2, 0,  1, 4)
        #Отрисовка кнопок
        layout.addWidget(self.currTimeLabel, 3, 3)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        #Создание QSettings, Загрузка настроек
        self.settings = QSettings('EventLogger', "OlegBoikoCorp", self)
        self.loadSettings()
    def openHelp(self): #Открытие диалогового окно справки
        dlg = help.helpForm() # Вариант 1
        dlg.exec() # Вариант 1
    def timeUpdate(self): #Обновление часов
        self.currTimeLabel.setText(datetime.now().strftime("%D %H:%M:%S"))
    def saveSettings(self): #Сохраняет настройки в реестре
        self.settings.setValue('user', self.userId)
    def loadSettings(self): #Загружает настройки из реестра
        id = self.settings.value('user', 1, type=int)
        self.enter = True
        self.changeUser('Гость', 'Гость', False, id)
        self.enter = False
    def openProfile(self): 
        dlg = myprofile.ProfileForm(self.changeUser)
        if dlg.exec(): #Открытие окна профиля
            self.enter = True
        else:
            self.enter = False
        del(dlg)
    def openJournal(self, journalId):
        dlg = journalLog.JournalLogDialog(self.userId, journalId)
        dlg.exec()
    def createJournal(self):
        dlg = createJournal.JournalForm(self.userId)
        dlg.exec()
    def changeUser(self, username, password, logout=False, id=1): #Смена пользователя
        if not self.enter and not logout:
            return
        self.enter = False
        with sqlite3.connect(database) as db: #Запрос к БД c представленным логином и паролем
            cursor = db.cursor()
            query = f"""SELECT id, name, password FROM user WHERE name = '{username}' AND password = '{password}'"""
            if id != 1:
                query = f"""SELECT id, name, password FROM user WHERE id = '{id}'"""
            cursor.execute(query)
            result = cursor.fetchone()
            if result: #Обновление данных при успешном входе
                self.userId = result[0]
                self.userName = result[1]
                self.userPassword = result[2]
                self.profileButton.setText(str(self.userName) if self.userName != 'Гость' else 'Регистрация')
            else: #Сообщение об ошибке
                getCriticalMsg("Неверный логин/пароль!")
        # self.allUpdate()
        self.logout.setVisible(self.userName != 'Гость')
    def closeEvent(self, event): #При закрытии приложения сохраняются настройки
        self.saveSettings()
        event.accept()