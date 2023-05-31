#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

class Led(QtWidgets.QWidget):
    color_on  = """
        QLabel {
            border:solid #F7B515;
            background-color: #F7B515
            }
        """

    color_off  = """
        QLabel {
            border:solid gray;
            background-color: gray;
            }
        """
    def __init__(self, *args, **kwargs):
        super(Led, self).__init__()

        content_la = QtWidgets.QLabel(kwargs['text'])
        content_la.setStyleSheet("font-size: 10pt;")

        self.led = QtWidgets.QLabel()
        self.led.setFixedSize(20, 20)
        self.led.setStyleSheet(self.color_off)

        self.status = QtWidgets.QLabel(kwargs['status'])
        self.status.setStyleSheet("color: #F7B515; font-size: 10pt;")

        led_layout = QtWidgets.QHBoxLayout(self)
        led_layout.addWidget(self.led)
        led_layout.addWidget(content_la)
        led_layout.addWidget(self.status)
        led_layout.setContentsMargins(0,0,0,0)

    def set_value(self, value):
        if value != 0:
            self.led.setStyleSheet(self.color_on)
        else:
            self.led.setStyleSheet(self.color_off)
    
    def set_status(self, status):
        self.status.setText(status)

