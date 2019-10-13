from PyQt5.QtWidgets import QDialog, QFormLayout, QPushButton, QLineEdit

from view.base.BoxLayout import HBoxLayout

class DbSettingDialog(QDialog):
    def __init__(self, parent=None, width=400, hight=250, host="localhost", port=3306, user="root", passwd="123456", db="test", charset="utf8"):
        super().__init__(parent)
        self.setWindowTitle("db设置")
        self.resize(width, hight)

        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

        self.hostLineEdit = QLineEdit(self.host, maximumWidth=260)
        self.portLineEdit = QLineEdit(str(self.port), maximumWidth=260)
        self.dbLineEdit = QLineEdit(self.db, maximumWidth=260)
        self.userLineEdit = QLineEdit(self.user, maximumWidth=260)
        self.passwdLineEdit = QLineEdit(self.passwd, maximumWidth=260)
        self.charsetLineEdit = QLineEdit(self.charset, maximumWidth=260)
        self.confirmButton = QPushButton("确定", maximumWidth=100)
        self.cancelButton = QPushButton("取消", maximumWidth=100)

        fromlayout = QFormLayout(self)
        fromlayout.addRow("host：", self.hostLineEdit)
        fromlayout.addRow("port：", self.portLineEdit)
        fromlayout.addRow("db：", self.dbLineEdit)
        fromlayout.addRow("user：", self.userLineEdit)
        fromlayout.addRow("passwd：", self.passwdLineEdit)
        fromlayout.addRow("charset：", self.charsetLineEdit)

        submitLayout = HBoxLayout(contentsMargins=(10, 10, 10, 10), spacing=10)
        submitLayout.addStretch(1)
        submitLayout.addWidget(self.confirmButton)
        submitLayout.addSpacing(20)
        submitLayout.addWidget(self.cancelButton)
        submitLayout.addStretch(1)

        fromlayout.addRow(submitLayout)

        self.confirmButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def accept(self):
        self.host = self.hostLineEdit.text().strip()
        self.port = int(self.portLineEdit.text().strip())
        self.db = self.dbLineEdit.text().strip()
        self.user = self.userLineEdit.text().strip()
        self.passwd = self.passwdLineEdit.text().strip()
        self.charset = self.charsetLineEdit.text().strip()
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

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    widget = DbSettingDialog()
    widget.show()
    sys.exit(app.exec_())




