from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QToolButton, QListWidget, QListWidgetItem

from config import configuration
from view.base.ScrollArea import ScrollArea

class ToolLeft(ScrollArea):
    def __init__(self, parent=None):
        super().__init__()

        self.setObjectName('ToolLeft')
        self.parent = parent
        self.setMaximumWidth(120)

        self.mainLayout = QVBoxLayout(self.frame)
        #self.mainLayout.addSpacing(5)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.menuList = QListWidget()
        self.menuList.setObjectName("menuList")
        self.mainLayout.addWidget(self.menuList)

        #菜单初始化
        self.reloadMenus(configuration.menus[0]['submenus'])

        #self.mainLayout.addStretch(3)
        #self.menuList.itemChanged()

    def reloadMenus(self, menus):
        self.menuList.clear()

        for menu in menus:
            listItem = QListWidgetItem(QIcon(menu['icon']), menu['title'])
            # 可以通过setData(self, int, Any)储存数据,通过data(self, int) -> Any获取数据
            # 经过测试发现前几个索引返回的都是对象的内部属性，改用.属性直接赋值的方式储存数据
            # listItem.setData(0, item)
            listItem.metadata = menu
            self.menuList.addItem(listItem)

        self.menuList.setCurrentRow(0)


class ToolLeft2(ScrollArea):
    def __init__(self, parent=None):
        super().__init__()

        self.setObjectName('ToolLeft')
        self.parent = parent
        self.setMaximumWidth(60)

        self.mainLayout = QVBoxLayout(self.frame)
        self.mainLayout.addSpacing(5)

        #self.mainLayout.addStretch(1)

        for item in configuration.menus:
            toolButton = QToolButton()
            #toolButton.setText(item['title'])
            toolButton.setIcon(QIcon(item['icon']))
            toolButton.setIconSize(QSize(24, 24))
            toolButton.setAutoRaise(True)
            toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            self.mainLayout.addWidget(toolButton)

        self.mainLayout.addStretch(3)