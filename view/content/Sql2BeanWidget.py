from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QPushButton, QVBoxLayout

from util import sqlParse
from view.base.LineTextEdit import LineTextEdit
from view.base.RadioButtonGroup import RadioButtonGroup


class Sql2BeanWidget(QWidget):
    TOJAVABEAN = 1
    TOSCALACASE = 2
    TOSCALABEAN = 3
    TOPYSQLALCHEMY = 4

    def __init__(self, parent=None):
        super().__init__(parent)

        convertTypeList = [(self.TOJAVABEAN, "sql转java bean"),(self.TOSCALACASE, "sql转scala case"),
                           (self.TOSCALABEAN, "sql转scala bean"),(self.TOPYSQLALCHEMY, "sql转python sqlalchemy")
                           ]
        self.convertTypeRadio = RadioButtonGroup(self, datas=convertTypeList, value=1)
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
        convertType = self.convertTypeRadio.value
        text = self.inputTextEdit.toPlainText().strip()

        if convertType == self.TOJAVABEAN:
             javaList = sqlParse.sql_to_javabean(text)
             result = ("\n"*2+"#"*10+"\n"*2).join(classText for className, classText in javaList)
        elif convertType == self.TOPYSQLALCHEMY:
             rstList = sqlParse.sql_to_sqlalchemy(text)
             result = ("\n" * 2 + "#" * 10 + "\n" * 2).join(classText for className, classText in rstList)
        elif convertType == self.TOSCALACASE:
             rstList = sqlParse.sql_to_scalacase(text)
             result = ("\n" * 2 + "#" * 10 + "\n" * 2).join(classText for className, classText in rstList)
        elif convertType == self.TOSCALABEAN:
             rstList = sqlParse.sql_to_scalabean(text)
             result = ("\n" * 2 + "#" * 10 + "\n" * 2).join(classText for className, classText in rstList)

        self.resultTextEdit.setPlainText(result)
