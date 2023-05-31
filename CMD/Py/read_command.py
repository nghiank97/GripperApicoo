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

data = client.read_input_registers(1001, 2, unit=86)

print("echo position", data.registers[0]/2)
print("real position", data.registers[1]/2)
      