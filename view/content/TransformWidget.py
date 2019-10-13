import re

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QRadioButton, QButtonGroup, QListWidget, QListWidgetItem, QListView, QLineEdit, \
    QPushButton, \
    QTableWidget, QHeaderView, QTableWidgetItem, QTableView, QAbstractItemView, QVBoxLayout, QPlainTextEdit

from util import util
from view.base.BoxLayout import VBoxLayout, HBoxLayout
from view.base.LineTextEdit import LineTextEdit
from view.base.RadioButtonGroup import RadioButtonGroup
from view.base.ScrollArea import ScrollArea
from view.base.TabWidget import TabWidget


class HexConvertWidget(ScrollArea):
    """https://tool.lu/hexconvert"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hexIn = 10
        self.hexInList = [{'value': 2, 'text': '2进制'}, {'value': 8, 'text': '8进制'}, {'value': 10, 'text': '10进制'},
                          {'value': 16, 'text': '16进制'}]
        self.hexOutList = [{'value': 2, 'text': '2进制'}, {'value': 8, 'text': '8进制'}, {'value': 10, 'text': '10进制'},
                           {'value': 16, 'text': '16进制'}]

        self.mainLayout = VBoxLayout(self.frame)
        self.mainLayout.setContentsMargins(20, 10, 0, 0)
        self.mainLayout.setSpacing(10)

        self.inRadioLayout = self.getInRadioLayout()
        self.mainLayout.addLayout(self.inRadioLayout)

        self.inputLayout = HBoxLayout()
        self.inputLayout.setSpacing(10)
        self.input = QLineEdit(self)
        self.input.setMinimumWidth(240)
        self.inputLayout.addWidget(self.input)
        self.transformSubmitButton = QPushButton("转换")
        self.inputLayout.addWidget(self.transformSubmitButton)
        self.inputLayout.addStretch(1)

        self.mainLayout.addLayout(self.inputLayout)

        self.resultTable = self.getResultTable()
        self.mainLayout.addWidget(self.resultTable)

        self.mainLayout.addStretch(1)

        self.transformSubmitButton.clicked.connect(self.transform)

    def getInRadioLayout(self):
        inRadioLayout = HBoxLayout()
        inRadioLayout.setSpacing(10)

        bg1 = QButtonGroup(self)
        for item in self.hexInList:
            rb11 = QRadioButton(item['text'])
            bg1.addButton(rb11, item['value'])
            if self.hexIn == item['value']:
                rb11.setChecked(True)
            inRadioLayout.addWidget(rb11)
        inRadioLayout.addStretch(1)
        """
        buttonClicked(self, QAbstractButton) [signal]
        buttonClicked(self, int) [signal]
        """
        bg1.buttonClicked[int].connect(lambda x: setattr(self, 'hexIn', x))
        # 也能获得选中的值
        # print(bg1.checkedId())

        return inRadioLayout

    def getResultTable(self):
        resultTable = QTableWidget()
        resultTable.setMaximumWidth(600)
        resultTable.setMinimumHeight(200)
        # resultTable.horizontalHeader().setStyleSheet("QHeaderView::section{background:#F3F3F3;}")
        self.setStyleSheet("QTableWidget{border:0 none;//最外层边框}")
        resultTable.verticalHeader().setVisible(False)  # 隐藏行号
        resultTable.setAlternatingRowColors(True)
        resultTable.setColumnCount(2)
        # 注意必须在初始化行列之后进行，否则，没有效果
        resultTable.setHorizontalHeaderLabels(['进制', '结果'])
        # 设置可以自适应宽度
        resultTable.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 设置可以自定义宽度
        resultTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        # QTableWidget的一些配置“https://blog.csdn.net/vah101/article/details/6215066”
        resultTable.setEditTriggers(QTableView.NoEditTriggers)  # 不可编辑
        resultTable.setSelectionMode(QAbstractItemView.NoSelection)  # 设置不能选中
        # resultTable.setSelectionBehavior(QAbstractItemView.SelectItems)  # 设置只能选中单元格
        # resultTable.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只能选中一行
        # resultTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置只有行选中
        resultTable.setColumnWidth(0, 50)

        # 可以设置tableview所有列的默认行高
        resultTable.verticalHeader().setDefaultSectionSize(40)

        resultTable.setRowCount(4)
        for i, data in enumerate(self.hexOutList):
            item = QTableWidgetItem(str(data['value']))
            resultTable.setItem(i, 0, item)
            lineEdit = QLineEdit()
            lineEdit.setContentsMargins(5, 5, 30, 5)
            lineEdit.setObjectName("rst_text_hex{}".format(data['value']))
            resultTable.setCellWidget(i, 1, lineEdit)

        return resultTable

    def transform(self):
        hexIn = self.hexIn
        text = self.input.text()
        num = int(text, hexIn)

        for data in self.hexOutList:
            hexOut = data['value']
            if hexOut == 2:
                rst = bin(num)[2:]
            elif hexOut == 8:
                rst = oct(num)[2:]
            elif hexOut == 10:
                rst = str(num)
            elif hexOut == 16:
                rst = hex(num)[2:]
            else:
                rst = util.hex_convert(num, hexOut)
            self.resultTable.findChild(QLineEdit, "rst_text_hex{}".format(hexOut)).setText(rst)

class RGBConvertWidget(ScrollArea):
    """https://tool.lu/hexconvert"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.convertTypeRadio = RadioButtonGroup(self, datas=[(1, "Hex_to_RGB"), (2, "RGB_to_Hex")], value=1)
        self.inputTextEdit = QPlainTextEdit()
        self.execButton = QPushButton("execute(执行)", maximumWidth=100)
        self.resultTextEdit = LineTextEdit()

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.convertTypeRadio)
        mainLayout.addWidget(self.inputTextEdit, 2)
        mainLayout.addWidget(self.execButton)
        mainLayout.addWidget(self.resultTextEdit, 7)

        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.execButton.clicked.connect(self.execButtonClicked)

    def execButtonClicked(self, *params):
        """rgba(1,2,1,1),rgba(1,1,3,1),rgba(1,1,5,1)"""
        #re.findall(r"\((.+?)\)", """rgba(1,1,1,1),rgba(1,1,1,1),rgba(1,1,1,1)""" )
        convertType = self.convertTypeRadio.value
        text = self.inputTextEdit.toPlainText().strip()

        self.resultTextEdit.clear()
        first = True
        for str in self.getConvertRsts(text, convertType):
            if not first:
                self.resultTextEdit.appendPlainText("\n"+ "#"*10 + "\n")
            else:
                first = False
            self.resultTextEdit.appendPlainText(str)

    def getConvertRsts(self, text, convertType):
        if convertType == 1:#Hex_to_RGB
            datas = [util.Hex_to_RGB(self.extractData(data)) for data in text.split(",") if data.strip()!=""]
            rstText1 = ", ".join( ["\"rgb({},{},{})\"".format(*data) for data in datas] )
            rstText2 = ", ".join(["\"rgba({},{},{},1)\"".format(*data) for data in datas])
            return rstText1,rstText2
        else:
            datas = [util.RGB_to_Hex(data) for data in re.findall(r"\((.+?)\)",text)]
            rstText1 = ", ".join(["\"#{}\"".format(data) for data in datas])
            rstText2 = ", ".join(["\"{}\"".format(data) for data in datas])
            rstText3 = ", ".join(["{}".format(data) for data in datas])
            return rstText1,rstText2,rstText3


    def extractData(self, data):
        data = data.strip()
        if "\"" in data or "'" in data:
            data = data[1:-1]
        return data

class TransformWidget(TabWidget):

    def addTabs(self):
        tab = HexConvertWidget(self.parent)
        self.addTab(tab, QIcon("icon/H1.png"), "进制转换")
        tab = RGBConvertWidget(self.parent)
        self.addTab(tab, QIcon("icon/transform.png"), "颜色转换")

    def initUI(self):
        pass
