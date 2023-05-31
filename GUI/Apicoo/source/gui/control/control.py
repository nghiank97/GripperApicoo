#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5 import QtGui, QtWidgets, QtCore
from Apicoo.source.device import SimpleDevice
from Apicoo.source.gui.style import slider
from Apicoo.source.gui.style import switch

class LoadButton(QtWidgets.QWidget):
    def __init__(self,*args,**kwargs):
        super(LoadButton,self).__init__()

        int_value = QtGui.QIntValidator()
        self.value_la = QtWidgets.QLineEdit()
        self.value_la.setValidator(int_value)
        self.value_la.setText(str(kwargs['value']))
        self.value_la.setAlignment(QtCore.Qt.AlignCenter)

        self.bt = QtWidgets.QPushButton(kwargs["text"])
        self.bt.setFixedHeight(30)
        self.bt.setStyleSheet("font-family: Consolas;"
                           "color: white;"
                           "background-color: #2AA1D3;"
                           "border: solid;"
                           "font-size: 20pt;"
                           "border-radius: 5px;"
                           "font-weight: bold")

        vbox = QtWidgets.QVBoxLayout(self)
        # vbox.addWidget(self.value_la)
        vbox.addWidget(self.bt)

    def getValue(self):
        return int(self.value_la.text())

class ControlForm(QtWidgets.QGroupBox):
    def __init__(self,*args,**kwargs):
        super(ControlForm,self).__init__()

        self.switch_mode = switch.ToggleButton()
        self.switch_mode.clicked.connect(self.setmode)

        self.position_slider = slider.Slider(name="DISTANCE",min=0,max=260, type="float")
        self.position_slider.set_value(0)
        self.position_slider.slider.setFixedWidth(120)

        self.speed_slider = slider.Slider(name="SPEED  ",min=1,max=255, type="int")
        self.speed_slider.set_value(1)
        self.speed_slider.slider.setFixedWidth(200)
        
        self.torque_slider = slider.Slider(name="TORQUE ",min=1,max=255, type="int")
        self.torque_slider.set_value(1)
        self.torque_slider.slider.setFixedWidth(200)

        self.send_bt = QtWidgets.QPushButton(" SEND ")
        self.send_bt.setFixedHeight(30)
        self.send_bt.clicked.connect(self.upload_position)
        self.send_bt.setStyleSheet("font-family: Consolas;"
                           "color: white;"
                           "background-color: #2AA1D3;"
                           "border: solid;"
                           "font-size: 15pt;"
                           "border-radius: 5px;"
                           "font-weight: bold")

        self.hold_bt = LoadButton(text="CLOSE",value=20)
        self.hold_bt.bt.clicked.connect(self.close_gripper)
        self.drop_bt = LoadButton(text="OPEN",value=220)
        self.drop_bt.bt.clicked.connect(self.open_gripper)

        control_la = QtWidgets.QVBoxLayout(self)

        control_la.addWidget(self.switch_mode)
        control_la.addStretch(1)

        box = QtWidgets.QHBoxLayout()
        box.addWidget(self.position_slider)
        box.addWidget(self.send_bt)

        control_la.addLayout(box)
        control_la.addWidget(self.speed_slider)
        control_la.addWidget(self.torque_slider)

        reload_la = QtWidgets.QHBoxLayout()
        reload_la.addWidget(self.hold_bt)
        reload_la.addWidget(self.drop_bt)

        control_la.addStretch(1)
        control_la.addLayout(reload_la)
        
        self.setStyleSheet("font-family: Consolas;"
                           "color: white;"
                           "background-color: #23252B;"
                           "border: solid;"
                           "font-size: 12pt;"
                           "font-weight: bold")

        self.device = SimpleDevice.getInstance()
        self.device.add_element(self)
        self.setEnabled(False)

    def upload_position(self):
        position = self.position_slider.get_value()
        if (position <0):
            position = 0xFFFF + 1 + position
        else:
            position = position

        speed = self.speed_slider.get_value()
        torque = self.torque_slider.get_value()
        command = {
            "add": 2001,
            "data": [position,speed,torque]
        }
        self.device.mb_send_command(command)

    def close_gripper(self):
        position = self.hold_bt.getValue()

        if (position <0):
            position = 0xFFFF + 1 + position
        else:
            position = position

        speed = self.speed_slider.get_value()
        torque = self.torque_slider.get_value()
        command = {
            "add": 2001,
            "data": [position,speed,torque]
        }
        self.device.mb_send_command(command)

    def open_gripper(self):
        position = self.drop_bt.getValue()
        if (position <0):
            position = 0xFFFF + 1 + position
        else:
            position = position
        speed = self.speed_slider.get_value()
        torque = self.torque_slider.get_value()
        command = {
            "add": 2001,
            "data": [position,speed,torque]
        }
        self.device.mb_send_command(command)

    def setmode(self, value):
        if (self.device.commProvider.gMode == 1):
            if(value == True):
                command = {
                    "add": 2000,
                    "data": [3]
                }
                self.device.mb_send_command(command)
        else:
            if(value == False):
                command = {
                    "add": 2000,
                    "data": [7]
                }
                self.device.mb_send_command(command)