#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5 import QtGui,QtCore
from Apicoo.source.gui.control import control
from Apicoo.source.gui.connect import connect
from Apicoo.source.gui.graphics import chart
from Apicoo.source.gui.register import register
from Apicoo.source.path import path

class WidgetWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(WidgetWindow,self).__init__()

        # self.setFixedSize(1000, 620)
        self.setWindowTitle('Apicoo Robotics')
        
        self.setWindowIcon(QtGui.QIcon(path.get_path_img('logo.png')))
        self.setStyleSheet("background-color: #2E3138;font-weight: bold")

        self.logo = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(path.get_path_img("big_logo.png"))
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)

        self.connect_form = connect.ConnectForm()
        self.graphic_form = chart.ChartForm()

        # Initialize tab screen
        self.mode_tabs = QtWidgets.QTabWidget()
        self.mode_tabs.setStyleSheet(
            """QTabBar{
                color: white;
                font-size: 12px;
            }
            QTabWidget::pane{
                border: 2px solid #23252B;
                border-radius: 5px;
            }
            QTabBar::tab:top:selected {
                background-color: #2AA1D3;
                border-radius: 2px;
            }
            QTabBar::tab:top {
                background-color: #2E3138;
            }
            """)
        self.control_form = control.ControlForm()
        self.mb_register_form = register.RegisterForm()
        self.mode_tabs.addTab(self.control_form,"   CONTROL   ")
        self.mode_tabs.addTab(self.mb_register_form,"   REGISTER   ")

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.connect_form)
        hbox = QtWidgets.QHBoxLayout()
        init_la = QtWidgets.QVBoxLayout()
        init_la.addWidget(self.mode_tabs)
        init_la.addWidget(self.logo)

        hbox.addLayout(init_la)
        hbox.addWidget(self.graphic_form)
        box.addLayout(hbox)

    def resizeEvent(self, event):
        _,_,w,h = self.rect().getRect()
        desktop = QtWidgets.QApplication.desktop()
        screenRect = desktop.screenGeometry()
        h_win = screenRect.height()
        w_win = screenRect.width()
        self.move(int((w_win - w)/2), int((h_win - h)/2))       