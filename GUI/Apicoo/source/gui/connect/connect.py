#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import glob
import serial
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from Apicoo.source.gui.style import combobox
from Apicoo.source.device import SimpleDevice
from Apicoo.source.path import path

class SerialStatusForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SerialStatusForm, self).__init__()
        self.id_la = QtWidgets.QLabel(self)
        self.id_la.setAlignment(QtCore.Qt.AlignCenter)
        self.id_la.setStyleSheet("""QLabel{
                font-size: 10pt;
                color: #FF3AFF;}""")
        self.port_la = QtWidgets.QLabel(self)
        self.port_la.setAlignment(QtCore.Qt.AlignCenter)
        self.port_la.setStyleSheet("""QLabel{
                font-size: 10pt;
                color: #FF3AFF;}""")
        self.baudrate_la = QtWidgets.QLabel(self)
        self.baudrate_la.setStyleSheet("""QLabel{
                font-size: 10pt;
                color: #FF3AFF;}""")
        self.baudrate_la.setAlignment(QtCore.Qt.AlignCenter)
        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.id_la)
        box.addWidget(self.port_la)
        box.addWidget(self.baudrate_la)

    def setValue(self, id, port, bd):
        self.id_la.setText("ID: " + str(id))
        self.port_la.setText("PORT: " + str(port))
        self.baudrate_la.setText("BAUD: " + str(bd))

    def clean(self):
        self.id_la.setText("")
        self.port_la.setText("")
        self.baudrate_la.setText("")

class ConnectForm(QtWidgets.QGroupBox):

    def __init__(self, *args, **kwargs):
        super(ConnectForm, self).__init__()
        self.setStyleSheet("font-family: Consolas;"
                           "color: white;"
                           "background-color: #444953;"
                           "border: solid;"
                           "border-radius: 10px;")

        t = """<span style="color:#4DE5FC;">SusGrip</span>
        <span style="color:#4D66C0;">Gripper</span>"""

        self.company_name = QtWidgets.QLabel(text=t)
        self.company_name.setStyleSheet("font-size: 20pt;")

        self.connect_bt = QtWidgets.QPushButton(text='CONNECT')
        self.connect_bt.setFixedSize(140,30)
        self.connect_bt.clicked.connect(self.connect_device_action)
        self.connect_bt.setStyleSheet("font-size: 12pt;background-color: #23252B;border-radius: 4px;")

        self.config_bt = QtWidgets.QPushButton(text='CONFIG')
        self.config_bt.setFixedSize(140,30)
        self.config_bt.clicked.connect(self.configure_device_action)
        self.config_bt.setStyleSheet("font-size: 12pt;background-color: #23252B;border-radius: 4px;")

        self.test_bt = QtWidgets.QPushButton(text='TEST')
        self.test_bt.setFixedSize(140,30)
        self.test_bt.clicked.connect(self.active_timer)
        self.test_bt.setStyleSheet("font-size: 12pt;background-color: #23252B;border-radius: 4px;")
        
        self.status_form = SerialStatusForm()

        box = QtWidgets.QHBoxLayout(self)
        box.addWidget(self.connect_bt)
        box.addWidget(self.config_bt)
        box.addWidget(self.test_bt)
        box.addStretch(1)
        box.addWidget(self.status_form)
        box.addStretch(1)
        box.addWidget(self.company_name)

        self.device = SimpleDevice.getInstance()
        self.device.add_element(self)

    def setEnabled(self, status):
        if status == False:
            self.connect_bt.setText("CONNECT")
            self.config_bt.setEnabled(True)
            self.status_form.clean()
        
    def active_timer(self):
        if self.test_bt.text() == "TEST":
            self.test_bt.setText("STOP")
            self.device.commProvider.load_repeat()
        else:
            self.test_bt.setText("TEST")
            self.device.commProvider.unload_repeat()
            
    def configure_device_action(self):
        config_dialog = ConfigForm()
        result = config_dialog.exec_()
        if result == 0:
            device_config = config_dialog.get_config_value()
            path.set_connect(device_config)
            self.device.configure_connection(device_config)

    def connect_device_action(self):
        if self.device.is_connected == False:
            self.device.connect()
            if self.device.is_connected:
                if self.device.is_connected == True:
                    self.connect_bt.setText("DISCONNECT")
                    self.config_bt.setEnabled(False)
                    self.status_form.setValue(self.device.parameter_connect['id'],self.device.parameter_connect['port'],self.device.parameter_connect['baudrate'])
        else:
            self.device.disconnect()
            if self.device.is_connected == False:
                self.connect_bt.setText("CONNECT")
                self.config_bt.setEnabled(True)
                self.status_form.clean()

class ConfigForm(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__()
        self.setWindowIcon(QtGui.QIcon(path.get_path_img("gear.png")))
        self.setFixedSize(QtCore.QSize(300, 200))
        self.setWindowTitle("CONFIG")
        self.setStyleSheet("background-color: #2E3138;color: white;font-size: 20px;")

        part_id = path.get_device_id()
        _id = [str(i) for i in range(1,255)]
        self.id_cb = combobox.Combobox(text="ID", value=_id)
        self.id_cb.set_head_value(part_id)

        ports = self.get_ports()
        self.port_cb = combobox.Combobox(text="PORT", value=ports)
        part_port = path.get_portname()
        
        if self.check_part_port(part_port, ports):
            self.port_cb.set_head_value(part_port)
        else:
            self.port_cb.set_head_value(ports[-1])

        baud = ['1200', '2400', '4800', '9600',
                '19200', '38400', '57600', '115200', '230400', '250000','256000', '500000','1000000']
        self.baud_cb = combobox.Combobox(text="BAUD", value=baud)
        self.baud_cb.set_edit_able(False)
        part_port = path.get_baudrate()
        self.baud_cb.set_head_value(part_port)

        data_list = ['8', '7', '6', '5']
        self.data_size_cb = combobox.Combobox(text="Data", value=data_list)
        self.data_size_cb.combobox.setEditable(False)

        parity_list = ['None', 'Even', 'Odd']
        self.parity_cb = combobox.Combobox(text="Parity", value=parity_list)
        self.parity_cb.combobox.setEditable(False)

        stop_list = ['1', '1.5', '2']
        self.stop_cb = combobox.Combobox(text="Stop", value=stop_list)
        self.stop_cb.combobox.setEditable(False)

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.id_cb)
        box.addWidget(self.port_cb)
        box.addWidget(self.parity_cb)
        box.addWidget(self.stop_cb)
        box.addWidget(self.baud_cb)
        box.addWidget(self.data_size_cb)
        
        self.device = SimpleDevice.getInstance()

    def check_part_port(self, portname, list_portname):
        for p in list_portname:
            if p == portname:
                return True
        return False

    def get_config_value(self):
        values = {
            'id': self.id_cb.get_value(),
            'port': self.port_cb.get_value(),
            'baudrate': self.baud_cb.get_value(),
            'stop': self.stop_cb.get_value(),
            'size': self.data_size_cb.get_value(),
            'parity':  self.parity_cb.get_value()
        }
        return values

    def get_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result