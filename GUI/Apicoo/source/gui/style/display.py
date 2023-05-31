#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from Apicoo.source.device import SimpleDevice

class ParameterForm(QtWidgets.QWidget):
    def __init__(self,value =0,*args, **kwargs):
        super(ParameterForm, self).__init__()

        label = QtWidgets.QLabel(self,text=kwargs['text'])
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("color: white;font-size: 12px;background-color: #23252B;")
        self.linedit = QtWidgets.QLineEdit(self,text=str(value))
        self.linedit.setStyleSheet("color: #2AA1D3;font-size: 12px")
        self.linedit.setAlignment(QtCore.Qt.AlignRight)

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(label)
        box.addWidget(self.linedit)
        box.setContentsMargins(0,0,0,0)

    def getValue(self):
        return int(self.linedit.text())

    def setValue(self,value):
        value = -(value & 0x8000) | (value & 0x7fff)
        self.linedit.setText(str(value))
    
    def setText(self,text):
        self.linedit.setText(text)
     
class OutputForm(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(OutputForm, self).__init__()
        self.setStyleSheet(
            """QGroupBox{
                font-family: Consolas;
                color: white;
                background-color: #23252B;
                border: solid;
                border-radius: 12px;
            }""")
                           
        command_register_la = QtWidgets.QLabel(self,text="COMMAND")
        command_register_la.setStyleSheet("color: white;font-size: 12px;background-color: #23252B;")
        self.action_form = ParameterForm(text="2000", value = 7)
        self.position_form = ParameterForm(text="2001", value = 0)
        self.velocity_form = ParameterForm(text="2002", value = 200)
        self.current_form = ParameterForm(text="2003", value = 100)
        self.position_min_form = ParameterForm(text="2004", value = 20)
        self.position_max_form = ParameterForm(text="2005", value = 200)

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(command_register_la,0,QtCore.Qt.AlignCenter)
        box.addWidget(self.action_form)
        box.addWidget(self.position_form)
        box.addWidget(self.velocity_form)
        box.addWidget(self.current_form)
        box.addWidget(self.position_min_form)
        box.addWidget(self.position_max_form)

    def getListValue(self):
        value = []
        value.append(self.action_form.getValue())
        value.append(self.position_form.getValue())
        value.append(self.velocity_form.getValue())

        value.append(self.current_form.getValue())
        value.append(self.position_min_form.getValue())
        value.append(self.position_max_form.getValue())
        return value

class InputForm(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__()
        self.setStyleSheet(
            """QGroupBox{
                font-family: Consolas;
                color: white;
                background-color: #23252B;
                border: solid;
                border-radius: 12px;
            }""")
        status_register_la = QtWidgets.QLabel(self,text="STATUS")
        status_register_la.setStyleSheet("color: white;font-size: 12px;background-color: #23252B;")

        self.status_input = ParameterForm(text="1000")
        self.position_echo_input = ParameterForm(text="1001")
        self.position_input = ParameterForm(text="1002")
        self.current_input = ParameterForm(text="1003")
        self.temp_input = ParameterForm(text="1004")
        self.reverse = ParameterForm(text="1005")

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(status_register_la,0,QtCore.Qt.AlignCenter)
        box.addWidget(self.status_input)
        box.addWidget(self.position_echo_input)
        box.addWidget(self.position_input)
        box.addWidget(self.current_input)
        box.addWidget(self.temp_input)
        box.addWidget(self.reverse)
        self.setEnabled(False)

    def show_data(self,value):
        self.status_input.setValue(value[0])
        self.position_echo_input.setValue(value[1])
        self.position_input.setValue(value[2])
        self.current_input.setValue(value[3])
        self.temp_input.setText("{} {}".format((value[4]&0xFF00)>>8, value[4]%256))
        self.reverse.setValue(value[5])