#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

class Slider(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Slider, self).__init__()

        content_la = QtWidgets.QLabel(kwargs['name'])
        self.show_value = QtWidgets.QLabel()
        self.type = kwargs['type']
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(kwargs['min'], kwargs['max'])
        self.slider.valueChanged.connect(self.value_slider_changed)
        self.slider.setStyleSheet("""QSlider::groove:horizontal {
                                    background: #434852;
                                    height: 8px;
                                    border-radius: 4px;
                                    }
                                    QSlider::handle:horizontal {
                                    background: #FFFFFF;
                                    width: 20px;
                                    height: 20px;
                                    margin-top: -2px;
                                    margin-bottom: -2px;
                                    border-radius: 5px;
                                    }
                                    QSlider::sub-page:horizontal {
                                    background: #F7B515;
                                    height: 8px;
                                    border-radius: 4px;
                                    }
                                    """)

        self.set_value(0)
        slider_layout = QtWidgets.QVBoxLayout(self)
        slider_layout.setContentsMargins(0,0,0,0)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(content_la)
        hbox.addStretch(1)
        hbox.addWidget(self.show_value)
        hbox.addStretch(1)
    
        slider_layout.addLayout(hbox)
        slider_layout.addWidget(self.slider)

    def value_slider_changed(self, value):
        self.set_value(value)

    def get_value(self):
        return self.slider.value()

    def set_value(self, value):
        if (self.type == "int"):
            self.show_value.setText('{:3d}'.format(value))
        else:
            self.show_value.setText('{:.1f}'.format(value/2))
        self.slider.setValue(value)
