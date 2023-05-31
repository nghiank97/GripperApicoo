#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
client = ModbusClient(
    method = "RTU",
    port="COM7", baudrate=115200, bytesize=8, parity="N", stopbits=1
)
connection = client.connect()
time.sleep(1)
print(client.is_socket_open())

# [3 , position, velocity, torque]
cmd_open = [3,200,100,100]
client.write_registers(2000, cmd_open, unit=86)
