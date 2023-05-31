#!/usr/bin/env python
# -*- coding: utf-8 -*-
from re import S
import numpy as np
import logging
import pyqtgraph as pg
from PyQt5 import QtWidgets,QtGui,QtCore
from Apicoo.source.device import SimpleDevice
from Apicoo.source.path import path
from Apicoo.source.gui.style import number
from Apicoo.source.gui.style import led

class GraphicWidget(QtWidgets.QGroupBox):
    def __init__(self, *args, **kwargs):
        super(GraphicWidget, self).__init__()

        self.numberOfSamples = 1000
        self.part_value = None

        pg.setConfigOptions(antialias=True)
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle(kwargs['name'], **{'color': '#FFFFFF'})
        self.plotWidget.getAxis('left').setTextPen('#FFFFFF')
        self.plotWidget.showGrid(x = True, y = True)
        self.plotWidget.setBackground((0x2E,0x31,0x38))
        self.plotWidget.setStyleSheet("border-radius: 10px;")
        
        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.plotWidget)
        self.plotWidget.setYRange(kwargs['min'],kwargs['max'])
        self.plotWidget.getPlotItem().hideAxis('bottom')

        self.plotWidget.addLegend()
        self.timeArray = np.arange(-self.numberOfSamples, 0, 1)

        grad = QtGui.QLinearGradient(0, 0, 0, 3)
        grad.setColorAt(0.1, pg.mkColor('#000000'))
        grad.setColorAt(0.9, pg.mkColor('b'))
        brush = QtGui.QBrush(grad)

        self.signalDataArrays = np.zeros(self.numberOfSamples)
        mpen = pg.mkPen(color=(0x8A,0xB6,0x1B), width=1.5)
        self.signalPlots = pg.PlotDataItem([0],[0],pen=mpen, brush=brush)
        self.plotWidget.addItem(self.signalPlots)
        self.setEnabled(False)

    def upDateGraphic(self, data):
        if data == None:
            return
        self.signalDataArrays = np.roll(self.signalDataArrays, -1)
        self.signalDataArrays[-1] = data
        self.signalPlots.setData(self.timeArray, self.signalDataArrays)
        self.signalPlots.updateItems()

class ChartForm(QtWidgets.QGroupBox):
    def __init__(self,*args,**kwargs):
        super(ChartForm,self).__init__()

        self.setStyleSheet("font-family: Consolas;"
                           "color: white;"
                           "background-color: #444953;"
                           "border: solid;"
                           "border-radius: 10px;")

        self.current_graphics = GraphicWidget(name="CURRENT (0.1A)",min=-40, max= 40)
        self.position_graphics = GraphicWidget(name="DISTANCE (mm)",min=0, max= 130)

        self.position_number = number.Number(name=" DISTANCE ")
        self.current_number = number.Number(name=" CURRENT ")
        
        self.temp_a = number.Number(name=" TEMP A ")
        self.temp_b = number.Number(name=" TEMP B ")

        self.pickup = QtWidgets.QLabel()
        self.pixmap_on = QtGui.QPixmap(path.get_path_img("robot_hand_pick.png"))
        self.pixmap_off = QtGui.QPixmap(path.get_path_img("hand_hold_bg.png"))
        self.pickup.setPixmap(self.pixmap_off)
        self.pickup.setAlignment(QtCore.Qt.AlignCenter)

        self.init_led = led.Led(text="INIT ",status = "DEAVTIVE")
        self.goto_led = led.Led(text="GOTO ",status = "STOP")
        self.obj_led = led.Led(text="OBJ  ",status = "NONE")
        self.input_led = led.Led(text="INPUT",status = "OFF")
        self.fault_led = led.Led(text="FAULT",status = "NONE")
        self.mode_led = led.Led(text="MODE ",status = "NORMAL")

        chart_la = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.position_graphics)
        hbox.addWidget(self.current_graphics)

        lex_box = QtWidgets.QVBoxLayout()
        lex_box.addWidget(self.init_led)
        lex_box.addWidget(self.goto_led)
        lex_box.addWidget(self.mode_led)
        lex_box.addWidget(self.obj_led)
        lex_box.addWidget(self.input_led)
        lex_box.addWidget(self.fault_led)
        hbox.addLayout(lex_box)

        number_box = QtWidgets.QHBoxLayout()
        number_box.addWidget(self.position_number)
        number_box.addWidget(self.current_number)
        number_box.addWidget(self.temp_a)
        number_box.addWidget(self.temp_b)
        number_box.addWidget(self.pickup)

        chart_la.addLayout(number_box)
        chart_la.addLayout(hbox)

        self.device = SimpleDevice.getInstance()
        self.device.commProvider.monitor_data.connect(self.update_data)

    def s16(self,value):
        return -(value & 0x8000) | (value & 0x7fff)

    def update_data(self, value):
        if self.device.is_connected == False:
            return
        if value == None and self.part_value == None:
            return
        if len(value) == 0:
            return
        if value == None:
            value = self.part_value

        # a = [self.s16(i) for i in value]
        # print(a)
        position = self.s16(value[2])
        current = self.s16(value[3])
        temp_a =  (value[4]>>8)
        temp_b =  value[4]&0xFF

        self.position_graphics.upDateGraphic(position/2)
        self.current_graphics.upDateGraphic(current)

        self.position_number.set_value(position/2)
        self.current_number.set_value(current)
        self.temp_a.set_value(temp_a)
        self.temp_b.set_value(temp_b)

        self.init_led.set_value((value[0]>>0)&0x01)
        if ((value[0]>>0)&0x01):
            self.init_led.set_status("ACTIVE")
        else:
            self.init_led.set_status("DEACTIVE")

        self.goto_led.set_value((value[0]>>1)&0x01)
        if ((value[0]>>1)&0x01):
            self.goto_led.set_status("GOTO")
        else:
            self.goto_led.set_status("STOP")

        self.mode_led.set_value((value[0]>>2)&0x01)
        if ((value[0]>>2)&0x01):
            self.mode_led.set_status("GPIO")
        else:
            self.mode_led.set_status("NORMAL")

        self.obj_led.set_value((value[0]>>3)&0x03)
        if (value[0]>>3)&0x03 == 0x00:
            self.obj_led.set_status("NONE")
            self.pickup.setPixmap(self.pixmap_off)
        elif (value[0]>>3)&0x03 == 0x01:
            self.obj_led.set_status("OPEN")
            self.pickup.setPixmap(self.pixmap_on)
        elif (value[0]>>3)&0x03 == 0x02:
            self.obj_led.set_status("CLOSE")
            self.pickup.setPixmap(self.pixmap_on)
        elif (value[0]>>3)&0x03 == 0x03:
            self.obj_led.set_status("DROP")
            self.pickup.setPixmap(self.pixmap_on)
            
        self.input_led.set_value((value[0]>>5)&0x01)
        if (value[0]>>5)&0x01 == 0x00:
            self.input_led.set_status("OFF")
        elif (value[0]>>5)&0x01 == 0x01:
            self.input_led.set_status("ON")

        self.fault_led.set_value((value[0]>>8)&0x0F)
        if (value[0]>>8) == 0x00:
            self.fault_led.set_status("NONE")
        elif (value[0]>>8) == 0x01:
            self.fault_led.set_status("nOCWT")
        elif (value[0]>>8) == 0x02:
            self.fault_led.set_status("nFAULT")
        elif (value[0]>>8) == 0x04:
            self.fault_led.set_status("CURRENT OVER")   
        elif (value[0]>>8) == 0x03:
            self.fault_led.set_status("TEMP OVER")    

        self.part_value = value