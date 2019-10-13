from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QButtonGroup, QRadioButton

from view.base.BoxLayout import HBoxLayout


class RadioButtonGroup(QWidget):
    """创建QButtonGroup，要求传入dict或者tuple"""
    valueChanged = pyqtSignal(int, int)

    def __init__(self, parent=None, datas=None, value=0, textkey="text", valuekey="value", **kwargs):
        super().__init__(parent, **kwargs)
        if datas is not None:
            self.datas = datas
        else:
            self.datas = []
        self.value = value
        self.textkey = textkey
        self.valuekey = valuekey

        self.bg = QButtonGroup(self)
        self.mainLayout = HBoxLayout(self)

        self.bg.buttonClicked[int].connect(self.buttonClicked)

        self._addRadioButtons(self.datas)

    def buttonClicked(self, value):
        oldvalue = self.value
        self.value = value  # self.bg.checkedId()也可以获得value
        if oldvalue != value:
            self.valueChanged.emit(value, oldvalue)

    def _getDataText(self, data):
        if isinstance(data, tuple):
            return data[1]
        elif isinstance(data, dict):
            return data.get(self.textkey)
        else:
            raise Exception("need dict or tuple")

    def _getDataValue(self, data):
        if isinstance(data, tuple):
            return data[0]
        elif isinstance(data, dict):
            return data.get(self.valuekey)
        else:
            raise Exception("need dict or tuple")

    def _addRadioButtons(self, datas):
        if not datas:
            return

        for data in datas:
            text = self._getDataText(data)
            value = self._getDataValue(data)
            rb = QRadioButton(text)
            self.bg.addButton(rb, value)
            if self.value == value:
                rb.setChecked(True)
            self.mainLayout.addWidget(rb)
        self.mainLayout.addStretch(1)