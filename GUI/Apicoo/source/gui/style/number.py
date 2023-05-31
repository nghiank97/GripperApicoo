#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

class Number(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Number, self).__init__()
        content_la = QtWidgets.QLabel(kwargs['name'])
        content_la.setStyleSheet("""QLabel{
                                    background: #045E94;
                                    color: white;
                                    font-size: 20px;
                                    border-top-left-radius : 10px;
                                    border-top-right-radius : 10px;
                                    border-bottom-left-radius : 0px;
                                    border-bottom-right-radius : 0px;
                                    }
                                    """)
        content_la.setAlignment(QtCore.Qt.AlignCenter)
                            
        self.show_value = QtWidgets.QLabel()
        self.show_value.setStyleSheet("""QLabel{
                                    background: #23252B;
                                    color: #2AA1D3;
                                    font-size: 20px;
                                    border-top-left-radius :0px;
                                    border-top-right-radius : 0px;
                                    border-bottom-left-radius : 10px;
                                    border-bottom-right-radius : 10px;
                                    }
                                    """)
        self.show_value.setAlignment(QtCore.Qt.AlignCenter)
        self.set_value(0)

        grip = QtWidgets.QGridLayout(self)

        grip.addWidget(content_la)
        grip.addWidget(self.show_value)
        grip.setVerticalSpacing(0)
        self.setLayout(grip)

    def set_value(self, value):
        self.show_value.setText(str(value))
