from PyQt5.QtGui import QIcon

from view.base.TabWidget import TabWidget
from view.content.Sql2BeanWidget import Sql2BeanWidget
from view.content.Sql2DocWidget import Sql2DocWidget
from view.content.SqlJavaCodeWidget import SqlJavaCodeWidget


class SqlParseWidget(TabWidget):

    def addTabs(self):
        tab = Sql2BeanWidget(self.parent)
        self.addTab(tab, QIcon("icon/sql.png"), "sql转bean")
        tab = Sql2DocWidget(self.parent)
        self.addTab(tab, QIcon("icon/sql.png"), "sql转doc")
        tab = SqlJavaCodeWidget(self.parent)
        self.addTab(tab, QIcon("icon/java.png"), "java")


    def initUI(self):
        pass