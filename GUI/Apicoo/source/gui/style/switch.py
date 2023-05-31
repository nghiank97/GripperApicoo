#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ToggleButtonBase(QFrame):
    clicked = pyqtSignal(bool)
    def __init__(self, width = 120, height = 60):
        super().__init__()
        self.width = width
        self.height = height
        if self.width < self.height * 2 -20:
            self.width = self.height * 2 -20
        self.setFixedSize(self.width, self.height)
        self.toggle_on = False
        self.initUI()

    def initUI(self):
        self.button_1 = QPushButton()
        self.button_1.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.button_2 = QPushButton()
        self.button_3 = QPushButton()
        self.button_2.setFixedSize(self.height - 30, self.height - 30)
        self.button_3.setFixedSize(self.height - 30, self.height - 30)
        self.button_1.setStyleSheet(
            "border-radius : %d; border : 2px solid #2E3138; background-color: #FFFFFF"%((self.height - 20)//2))
        self.button_2.setStyleSheet(
            "border-radius : %d; background-color: #F7B515"%((self.height - 30)//2))
        self.button_3.setStyleSheet(
            "border-radius : %d; background-color: #F7B515"%((self.height - 30)//2))
        self.button_3.setVisible(False)
        self.button_1.clicked.connect(self.pushToggle)
        self.button_2.clicked.connect(self.pushToggle)
        self.button_3.clicked.connect(self.pushToggle)

        layout = QGridLayout()
        layout.addWidget(self.button_1, 0, 0, 1, 2)
        layout.addWidget(self.button_2, 0, 0, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.button_3, 0, 1, 1, 1, alignment = Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def pushToggle(self):
        self.toggle_on = not self.toggle_on
        self.clicked.emit(self.toggle_on)
    
    def changeState(self, state):
        if state == True:
            self.button_1.setStyleSheet("border-radius : %s; border : 2px solid #2E3138; background-color: rgb(60, 156, 253)"%((self.height - 20)//2))
            self.button_2.setVisible(False)
            self.button_3.setVisible(True)
        elif state == False:
            self.button_1.setStyleSheet("border-radius : %s; border : 2px solid #2E3138; background-color: #FFFFFF"%((self.height - 20)//2))
            self.button_2.setVisible(True)
            self.button_3.setVisible(False)

class ToggleButton(QWidget):
    clicked = pyqtSignal(bool)
    def __init__(self):
        super().__init__()

        font = QFont()
        font.setPointSize(80)
        font.setBold(True)
                    
        self.on_off_label = QLabel('GPIO')
        self.on_off_label.setFont(font)

        self.toggle_button = ToggleButtonBase()
        self.toggle_button.clicked.connect(self.handle_clicked)
        
        mainFrame = QHBoxLayout()
        mainFrame.addWidget(self.toggle_button)
        mainFrame.addWidget(self.on_off_label)
        
        self.setLayout(mainFrame)

    @pyqtSlot(bool)
    def handle_clicked(self, on_off):
        if on_off ==True:
            status = self.show_message("Change to\r\nNORMAL MODE")
            if status == True:
                self.on_off_label.setText('NORMAL')
                self.toggle_button.changeState(True)
                self.clicked.emit(True)
        elif on_off ==False:
            status = self.show_message("Change to\r\nGPIO MODE")
            if status == True:
                self.on_off_label.setText('GPIO')
                self.toggle_button.changeState(False)
                self.clicked.emit(False)
 
    def show_message(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setWindowTitle("MODE")
        msg.setIcon(QMessageBox.Question)
        msg.setStyleSheet("background-color: white;color: black;font-size:20px;")
        msg.setStandardButtons(QMessageBox.Yes|QMessageBox.Cancel)
        msg.exec_()

        button = msg.clickedButton()
        result = msg.standardButton(button)
        if result == QMessageBox.Yes:
            return True
        else:
            return False
