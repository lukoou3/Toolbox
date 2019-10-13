from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QToolBar, QListWidget, QListView

from dao import DbSetting
from util.MysqlCursor import MysqlCursor
from view.base.BoxLayout import VBoxLayout
from view.content.DbTableWidget import DbTableWidgetDialog
from view.pop.DbSettingDialog import DbSettingDialog



class DbTablesWidget(QWidget):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        host, port, db, user, passwd, charset = DbSetting.getDbSetting(1)
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

        self.toolBar = QToolBar()
        self.tablesWidget = QListWidget()
        self.tablesWidget.setViewMode(QListView.IconMode)
        self.tablesWidget.itemDoubleClicked.connect(self.tableClicked)
        self.initToolBar()

        mainLayout = VBoxLayout(self)
        mainLayout.addWidget(self.toolBar)
        mainLayout.addWidget(self.tablesWidget)

    def initToolBar(self):
        self.toolBar.addAction(QIcon('icon/setting.png'), 'setting', self.setDbParams)

    def loadData(self):
        self.tablesWidget.clear()
        with MysqlCursor(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset) as cursor:
            cursor.execute("show tables")
            for row in cursor:
                self.tablesWidget.addItem(row[0])

    def tableClicked(self,item):
        table = item.text()
        dialog = DbTableWidgetDialog(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                                 charset=self.charset,tableName=table)
        dialog.tableWidget.loadData()
        dialog.exec_()

    def setDbParams(self):
        exportDialog = DbSettingDialog(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset)
        result = exportDialog.exec_()
        if result > 0:
            self.host = exportDialog.host
            self.port = exportDialog.port
            self.db = exportDialog.db
            self.user = exportDialog.user
            self.passwd = exportDialog.passwd
            self.charset = exportDialog.charset
            DbSetting.setDbSetting(1, self.host, self.port, self.db, self.user, self.passwd, self.charset)
            self.loadData()
