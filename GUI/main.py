#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from PyQt5 import QtWidgets
from Apicoo.source.gui.window import WidgetWindow

if __name__ == '__main__':
    try:
        logging.basicConfig(filename='Apicoo.log', filemode='w',
                            format='%(name)s - %(levelname)s - %(message)s')
        app = QtWidgets.QApplication(sys.argv)
        app.setStyle('Fusion')
        mainwindow = WidgetWindow()
        mainwindow.show()
        sys.exit(app.exec_())

    except Exception as exception:
        logging.error(exception, exc_info=True)
        