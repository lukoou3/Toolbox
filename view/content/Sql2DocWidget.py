from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QPushButton, QFileDialog, QCheckBox

import os

from util import sqlParse
from view.base.RadioButtonGroup import RadioButtonGroup
from view.base.FileLineEdit import FileOpenFileLineEdit


class Sql2DocWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.labl1 = QLabel("sql文件：")
        self.openPathLineEdit = FileOpenFileLineEdit(filter="sql files (*.sql *.txt)", maximumWidth=300)
        self.openPathLineEdit.setPlaceholderText("输入或者选择路径")

        self.labl2 = QLabel("导出类型：")
        self.exportTypeRadioGroup = RadioButtonGroup(datas=[{"value": 1, "text": "docx"},
                                                {"value": 2, "text": "html"}]
                                         , value=1, maximumWidth=200)

        self.labl3 = QLabel("导出后打开文件：")
        self.explorerFileCheckBox = QCheckBox()
        self.explorerFileCheckBox.setChecked(True)

        self.exportButton = QPushButton("导出", maximumWidth=100)

        mainLayout = QFormLayout(self)
        mainLayout.addRow(self.labl1, self.openPathLineEdit)
        mainLayout.addRow(self.labl2, self.exportTypeRadioGroup)
        mainLayout.addRow(self.labl3, self.explorerFileCheckBox)
        mainLayout.addRow(self.exportButton)

        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.exportButton.clicked.connect(self.exportButtonClicked)

    def exportButtonClicked(self, *params):
        exportType = self.exportTypeRadioGroup.value
        openPath = self.openPathLineEdit.text()
        explorer = self.explorerFileCheckBox.isChecked()

        if not os.path.exists(openPath):
            return

        with open(openPath, encoding="utf-8") as fp:
            sqlText = fp.read()

        if exportType == 1:
            fileName = QFileDialog.getSaveFileName(self, '', "", "doc files (*.docx)")
            if fileName[0]:
                sqlParse.sql_to_docx(sqlText, fileName[0], explorer=explorer)
        elif exportType == 2:
            fileName = QFileDialog.getSaveFileName(self, '', "", "html files (*.html)")
            if fileName[0]:
                sqlParse.sql_to_html(sqlText, fileName[0], explorer=explorer)
