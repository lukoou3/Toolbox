# coding=utf-8
import logging

from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from view.base.FadeWidget import FadeWidget
from view.base.FramelessWindow import FramelessWindow
from view.plat.Content import Content
from view.plat.Header import Header
from view.plat.ToolLeft import ToolLeft
from view.plat.ToolTop import ToolTop

class MainWindow(FramelessWindow,FadeWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName('MainWindow')
        self.parent = parent
        self.initUI()

    def initUI(self):
        #self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏边框
        #self.setWindowFlags(Qt.CustomizeWindowHint)

        self.setWindowIcon(QIcon('icon/app_logo1.png'))#Windows任务栏图标不会变

        # mainLayout = QVBoxLayout()
        # mainLayout.setSpacing(0)
        # #这个必须设置，不设置的话，四周会多出来边框
        # mainLayout.setContentsMargins(6, 6, 6, 6)

        mainLayout = self.layout()
        self.setLayout(mainLayout)

        self.header = Header(self)
        #事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式
        self.header.installEventFilter(self)
        mainLayout.addWidget(self.header)

        self.toolTop = ToolTop()
        self.toolTop.setMaximumHeight(80)
        self.toolTop.installEventFilter(self)
        mainLayout.addWidget(self.toolTop)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)

        self.toolLeft = ToolLeft();
        self.toolLeft.installEventFilter(self)
        contentLayout.addWidget(self.toolLeft)
        self.content = Content()
        self.content.installEventFilter(self)
        contentLayout.addWidget(self.content)

        mainLayout.addLayout(contentLayout)

        #注册事件
        self.registerSignalConnect()

    def registerSignalConnect(self):
        # 注册最小化事件
        self.header.minButton.clicked.connect(self.showMinimized)
        # 注册最大化事件
        self.header.maxButton.clicked.connect(self.showMaxiOrRevert)
        #注册关闭事件
        self.header.closeButton.clicked.connect(self.close)

        #top菜单切换
        self.toolTop.currentItemChanged.connect(self.toolTopItemChanged)
        #left菜单切换
        self.toolLeft.menuList.currentItemChanged.connect(self.toolTopLeftChanged)

    def toolTopItemChanged(self, item, before = None):
        #print(item.metadata.get("submenus"))
        self.toolLeft.reloadMenus(item.metadata.get("submenus"))

    def toolTopLeftChanged(self, item, before = None):
        #清空QListWidget时也会触发这个信号
        if not item:
            return
        self.content.setCurrentWidgetByMenu(item.metadata)
        #logging.getLogger().info("点击左菜单{0}".format(item.metadata))

    def showMaxiOrRevert(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


