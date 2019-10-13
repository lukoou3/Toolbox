from PyQt5.QtWidgets import QTabWidget

from view.base.BoxLayout import VBoxLayout
from view.base.ScrollArea import ScrollArea


class TabWidget(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TransformWidget")

        self.tabWidget = QTabWidget()
        self.tabWidget.setObjectName("tabWidget")

        self.mainLayout = VBoxLayout()
        self.mainLayout.addWidget(self.tabWidget)

        self.frame.setLayout(self.mainLayout)

        self.addTabs()
        self.initUI()

    def initUI(self):
        """子类实现"""
        pass

    def addTabs(self):
        """子类实现"""
        pass


    def addTab(self, widget, * args):
        """
        addTab(self, QWidget, str) -> int
        addTab(self, QWidget, QIcon, str) -> int
        """
        self.tabWidget.addTab(widget, * args)