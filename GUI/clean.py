#!/usr/bin/python
import os
import sys
import shutil

if __name__ == '__main__':

    name_path = [
        "\\Apicoo\\source\\__pycache__\\",
        "\\Apicoo\\source\\gui\\__pycache__\\",
        "\\Apicoo\\source\\gui\\control\\__pycache__\\",
        "\\Apicoo\\source\\gui\\connect\\__pycache__\\",
        "\\Apicoo\\source\\gui\\graphics\\__pycache__\\",
        "\\Apicoo\\source\\gui\\register\\__pycache__\\",
        "\\Apicoo\\source\\gui\\style\\__pycache__\\",
        "\\Apicoo\\source\\path\\__pycache__\\",
    ]

    origin_path = os.path.abspath(os.getcwd())

    print("clean ........")
    try:
        for p in name_path:
            path = origin_path + p
            shutil.rmtree(path)

        print("finish ........")

    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

