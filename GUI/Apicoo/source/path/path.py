#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

def get_path_img(icon_name):
    source_path = os.path.abspath(os.getcwd())
    icon_path = source_path+"/Apicoo/img/"+ icon_name
    return icon_path

def get_base_path():
    path= os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    return os.path.join(path,"setting.json")

def get_data():
    basePath = get_base_path()
    file_setting = open(basePath,'r')
    data = json.load(file_setting) 
    file_setting.close()
    return data

def get_portname():
    data = get_data()
    return data['port']['value']

def get_baudrate():
    data = get_data()
    return data['baudrate']['value']

def get_device_id():
    data = get_data()
    return data['id']['value']

def get_connect():
    return {
        "port": get_portname(),
        "id": get_device_id(),
        "baudrate": get_baudrate()
    }

def set_portname(port_name):
    path = get_base_path()
    f = open(path, "r")
    data = json.load(f)
    data['port']['value'] = port_name
    f.close()
    f = open(path, "w")
    json.dump(data,f,ensure_ascii=False, indent=4)
    f.close()

def set_device_id(id_name):
    path = get_base_path()
    f = open(path, "r")
    data = json.load(f)
    data['id']['value'] = id_name
    f.close()
    f = open(path, "w")
    json.dump(data,f,ensure_ascii=False, indent=4)
    f.close()

def set_baudrate(bd):
    path = get_base_path()
    f = open(path, "r")
    data = json.load(f)
    data['baudrate']['value'] = bd
    f.close()
    f = open(path, "w")
    json.dump(data,f,ensure_ascii=False, indent=4)
    f.close()

def set_connect(value):
    set_portname(value['port'])
    set_device_id(value['id'])
    set_baudrate(value['baudrate'])
