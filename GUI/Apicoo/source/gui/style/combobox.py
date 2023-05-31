

from PyQt5 import QtCore
from PyQt5 import QtWidgets

HORIZONTAL = 0
VERTICAL = 1

class Combobox(QtWidgets.QWidget):

    def __init__(self, type = HORIZONTAL, *args, **kwargs):
        super(Combobox, self).__init__()

        self.lable = QtWidgets.QLabel(kwargs['text'])
        self.lable.setAlignment(QtCore.Qt.AlignLeft)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(kwargs['value'])
        self.set_edit_able(True)

        if (type == HORIZONTAL):
            layout = QtWidgets.QHBoxLayout(self)
        else:
            layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.lable)
        layout.addWidget(self.combobox)

    def set_edit_able(self,status):
        self.combobox.setEditable(status)

    def set_head_value(self,value):
        if type(value) == int:
            str_value = str(value)
        else:
            str_value = value
        self.combobox.setCurrentText(str_value)

    def set_enabled(self, value):
        self.combobox.setEnabled(value)

    def get_value(self):
        value = self.combobox.currentText()
        return value

    