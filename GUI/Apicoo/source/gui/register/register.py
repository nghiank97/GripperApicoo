#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import serial
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from Apicoo.source.gui.style import display
from Apicoo.source.device import SimpleDevice
from Apicoo.source.path import path

class RegisterForm(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__()
        self.resize(700, 400)
        self.setWindowIcon(QtGui.QIcon(path.get_path_img('logo.png')))

        self.output_form = display.OutputForm()
        self.input_form = display.InputForm()

        self.save_bt = QtWidgets.QPushButton(text='SAVE CONFIG')
        self.save_bt.setStyleSheet(
            """
            color: #F7B515;
            font-size: 16pt;
            background-color: #444953;
            border-radius: 4px;"""
        )
        self.save_bt.clicked.connect(self.save_config_handle)

        vbox = QtWidgets.QVBoxLayout(self)

        box_register = QtWidgets.QHBoxLayout()
        box_register.addWidget(self.output_form)
        box_register.addWidget(self.input_form)

        box_bt = QtWidgets.QHBoxLayout()
        box_bt.addWidget(self.save_bt)
        
        vbox.addLayout(box_register)
        vbox.addLayout(box_bt)

        self.setStyleSheet(
            """QGroupBox{
                font-family: Consolas;
                color: white;
                background-color: #23252B;
                border: 0;
        }""")

        self.device = SimpleDevice.getInstance()
        self.device.commProvider.monitor_data.connect(self.show_input_data)
        self.device.add_element(self)

    def show_input_data(self,value):
        self.input_form.show_data(value)

    def save_config_handle(self):
        value = self.output_form.getListValue()
        command = {
            "add": 2000,
            "data": value
        }
        self.device.mb_send_command(command)