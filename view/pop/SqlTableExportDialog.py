from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QPushButton

from view.base.BoxLayout import VBoxLayout, HBoxLayout
from view.base.ComboBox import ComboBox
from view.base.FileLineEdit import FileSaveLineEdit


class SqlTableExportDialog(QDialog):
    def __init__(self, parent=None, width=500, hight=300):
        super().__init__(parent)
        self.setWindowTitle("导出")
        self.resize(width, hight)

        self.labl1 = QLabel("文件类型：")
        self.fileTypeComboBox = ComboBox(datas=[{"id":1,"text":"csv"},
                                    {"id":2,"text":"excel"}]
                                    , maximumWidth=200)
        self.labl2 = QLabel("文件保存路径：")
        self.pathLineEdit = FileSaveLineEdit(filter="Text files (*.csv)", maximumWidth=300)
        self.pathLineEdit.setPlaceholderText("输入或者选择路径")

        self.confirmButton = QPushButton("确定", maximumWidth=100)
        self.cancelButton = QPushButton("取消", maximumWidth=100)


        mainLayout = VBoxLayout(self, contentsMargins=(10,10,10,10),spacing=10)

        fromlayout = QFormLayout()
        fromlayout.addRow(self.labl1, self.fileTypeComboBox)
        fromlayout.addRow(self.labl2, self.pathLineEdit)

        submitLayout = HBoxLayout(contentsMargins=(10, 10, 10, 10), spacing=10)
        submitLayout.addStretch(1)
        submitLayout.addWidget(self.confirmButton)
        submitLayout.addSpacing(20)
        submitLayout.addWidget(self.cancelButton)
        submitLayout.addStretch(1)

        fromlayout.setLayout(2, QFormLayout.SpanningRole, submitLayout)

        mainLayout.addLayout(fromlayout)

        self.fileTypeComboBox.currentIndexChanged.connect(self.fileTypeChanged)
        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def accept(self):
        """
        点击确认后
        """
        #super().accept()
        self.done(1) # 结束对话框返回1:QDialog.Accepted

    def reject(self):
        """
        点击取消后
        """
        self.done(0)# 结束对话框返回0:QDialog.Rejected

    def fileTypeChanged(self):
        self.pathLineEdit.filter = "Text files (*.csv)" if self.fileTypeComboBox.getCurrentData()['id'] == 1 else "Excel 文件(*.xlsx)"

    @property
    def exportParams(self):
        fileType = self.fileTypeComboBox.getCurrentData().get("id",1)
        filePath = self.pathLineEdit.text()
        return fileType,filePath

    @staticmethod
    def getExportParams(parent=None, width=500, hight=300):
        dialog = SqlTableExportDialog(parent=parent, width=width, hight=hight)
        result = dialog.exec_()
        return (result == QDialog.Accepted, dialog.exportParams)