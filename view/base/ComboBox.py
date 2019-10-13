from PyQt5.QtWidgets import QComboBox

class ComboBox(QComboBox):
    def __init__(self, parent=None, datas=None, textkey="text", **kwargs):
        super().__init__(parent, **kwargs)

        if datas is not None:
            self.datas = datas
        else:
            self.datas = []
        self.textkey = textkey

        self._addDatasToItems(self.datas)

    def getCurrentData(self):
        return self.datas[self.currentIndex()]

    def addDatas(self, datas):
        self.datas.extend(datas)
        self._addDatasToItems(datas)

    def getDataText(self, data):
        if isinstance(data, str):
            return data
        elif isinstance(data, tuple):
            return data[1]
        elif isinstance(data, dict):
            return data.get(self.textkey)
        else:
            return str(data)

    def _addDatasToItems(self, datas):
        if not datas:
            return

        for data in datas:
            self.addItem(self.getDataText(data))


