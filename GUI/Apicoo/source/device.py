#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import threading
import serial
from serial import win32
from collections import deque

from PyQt5 import QtCore, QtWidgets, QtGui
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException
from pymodbus.exceptions import ConnectionException
from pymodbus.exceptions import ModbusIOException
from Apicoo.source.path import path

class SimpleDevice:
    __instance = None
    @staticmethod
    def getInstance():
        if SimpleDevice.__instance == None:
            SimpleDevice()
        return SimpleDevice.__instance

    def __init__(self):
        if SimpleDevice.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.mbrtu_master = None
            self.is_connected = False
            self.id = ""
            self.parameter_connect = {}

            self.element_list = []
            self.commProvider = ModbusRtuMasterHandler()
            SimpleDevice.__instance = self

    def add_element(self, listener):
        self.element_list.append(listener)

    def configure_connection(self, config_dict):
        self.parameter_connect = {
            "id": config_dict["id"],
            "method": 'rtu',
            "port" : config_dict["port"],
            "baudrate" : int(config_dict["baudrate"]),
            "bytesize" : 8,
            "parity" : 'N',
            "stopbits" : 1,
            "timeout" : 1
        }
        self.id = int(config_dict["id"])

    def init_communications(self):
        self.mbrtu_master = ModbusClient(
            method = self.parameter_connect['method']
            ,port= self.parameter_connect['port']
            ,baudrate= self.parameter_connect['baudrate']
            ,parity = self.parameter_connect['parity']
            ,timeout= self.parameter_connect['timeout']
        )
        connection = self.mbrtu_master.connect()

        if connection == True:
            for i in range(5):
                registers  = self.mbrtu_master.read_input_registers(1000,1,unit= self.id, timeout = 1)
            if registers != None and registers.isError() == False:
                self.is_connected = True
                self.start_theading()
                return True
            else:
                raise "Don\'t response"
        return False

    def start_theading(self):
        self.commProvider.id = self.id
        self.commProvider.is_connect = True
        self.commProvider.master_rtu = self.mbrtu_master
        self.commProvider.error.connect(self.disconnect)
        self.commProvider.start()
   
    def connect(self):
        try:
            self.init_communications()
            if self.is_connected == True:
                for listener in self.element_list:
                    listener.setEnabled(True)
                self.show_problem(title="Gripper",text="Connect !")
            else:
                raise "Don\'t response"
        except serial.SerialException as serEx:
            logging.warning('Is not possible to open serial port')
            self.show_problem(title="Gripper",text="Error while trying to open serial port",status=0)
            return False
        except BaseException as serEx:
            logging.warning("Don\'t response")
            self.show_problem(title="Gripper",text="Don\'t response",status=0)
            return False

    def close_communication(self):
        self.is_connected = False
        self.mbrtu_master.close()
        self.commProvider.master_rtu.close()

    def disconnect(self,text = "Disconnect !"): 
        self.close_communication()
        for listener in self.element_list:
            listener.setEnabled(False)
        self.show_problem(title="Gripper",text=text,status=0)

    def show_problem(self,text,status = 1,title = "ConfigTool"):
        msgBox = QtWidgets.QMessageBox()
        if status == 1:
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
        else:
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setWindowIcon(QtGui.QIcon(path.get_path_img("comments.png")));
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()

    def mb_send_command(self, command, mode="NORMAL_MODE"):
        if mode == "SWITCH_MODE":
            if self.is_connected == True:
                if self.commProvider.repeat == False:
                    self.commProvider.load_registers(command)
                    self.show_problem("Finish" ,1,title = "SetMode")
        elif mode == "NORMAL_MODE":
            if self.commProvider.gMode == 1:
                self.show_problem("Can't control by software" ,0,title = "GPIO MODE")
            if self.is_connected == True:
                if self.commProvider.repeat == False:
                     self.commProvider.load_registers(command)

class ModbusRtuMasterHandler(QtCore.QThread):
    monitor_data = QtCore.pyqtSignal(list)
    error = QtCore.pyqtSignal(str)

    def __init__(self, master=None, *args,**kwargs):
        super(ModbusRtuMasterHandler, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.master_rtu = master
        self.id = 1
        self.is_connect = True
        self.timeout = 10
        self.tx_enable = False

        self.register = []
        self.gGTO = 0
        self.gOBJ = 0
        self.gMode = 0
        self.distace = 0

        self.stack_data = deque()

        self.test_list = [0, 256]
        self.test_flag = 0
        self.repeat = False

    def load_repeat(self):
        self.repeat = True

    def unload_repeat(self):
        self.repeat = False

    def load_registers(self,command):
        self.stack_data.append(command)
        self.tx_enable = True

    def run(self):
        try:
            while not self.stopped():
                if (self.is_connect == True):
                    if (self.master_rtu.is_socket_open() == True):
                        if self.repeat == True:
                            if (self.distace != self.test_list[self.test_flag]):
                                data = [3,self.test_list[self.test_flag],150,150]
                                self.master_rtu.write_registers(2000, data, unit=self.id)
                            if (abs(self.test_list[self.test_flag] - self.register[2]) <= 2):
                                self.test_flag += 1
                                if (self.test_flag == 2):
                                    self.test_flag = 0

                            if self.test_list[self.test_flag] < self.register[2] \
                                and self.gOBJ == 2:    
                                self.test_flag += 1
                                if (self.test_flag == 2):
                                    self.test_flag = 0
                            time.sleep(0.01)

                        if (self.tx_enable == True):
                            raw = self.stack_data.pop()
                            address = raw["add"]
                            data = raw["data"]
                            self.master_rtu.write_registers(address, data, unit=self.id)
                            if len(self.stack_data) == 0:
                                self.tx_enable = False
                            time.sleep(0.01)
                            continue
                        else:
                            registers  = self.master_rtu.read_input_registers(1000,6,unit =self.id,timeout = 0.02)
                            if registers != None and registers.isError() == False:
                                self.timeout =  10
                                self.register = registers.registers
                                print(self.register)
                                self.distace = self.register[1]
                                self.gGTO = (self.register[0]>>1)&0x01
                                self.gOBJ = (self.register[0]>>3)&0x03
                                self.gMode = (self.register[0]>>2)&0x01
                                self.monitor_data.emit(registers.registers)
                            else:
                                self.timeout-=1
                                print("timeout: {}".format(self.timeout))
                                if (self.timeout == 0):
                                    print("error: {}".format(registers))
                                    self.error.emit("Timeout")
                                    self.is_connect = False
                self.master_rtu.connect()
                time.sleep(0.02)
        except ModbusIOException as error:
            logging.error(error, exc_info=True)
            self.error.emit(error)

        except ConnectionException as error:
            logging.error(error, exc_info=True)
            self.error.emit(error)

        except serial.SerialException as serialException:
            logging.error(serialException, exc_info=True)
            self.error.emit(error)

        except ModbusException as error:
            logging.error(error, exc_info=True)
            self.error.emit(error)

        finally:
            self.is_connect = False

    def stop(self):
        self.is_connect = False
        time.sleep(1)
        self._stop_event.set()
        if(self.master_rtu.is_socket_open()):
            self.master_rtu.close()


    def stopped(self):
        return self._stop_event.is_set()