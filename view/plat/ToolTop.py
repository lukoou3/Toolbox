import math
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QListView, QListWidgetItem, QGraphicsDropShadowEffect
from config import configuration


class ToolTop(QListWidget):
    def __init__(self):
        super().__init__()
        self.menus = configuration.menus
        self.initUI()

    def initUI(self):
        self.setViewMode(QListView.IconMode)
        for item in self.menus:
            widgetItem = QListWidgetItem(self)
            widgetItem.metadata = item
            widgetItem.setText(item['title'])
            widgetItem.setToolTip(item.get('description',''))
            widgetItem.setIcon(QIcon(item['icon']))
            self.addItem(widgetItem)

        self.setCurrentRow(0)
        self.setIconSize(QSize(32, 32))
        self.setMovement(QListView.Static)
        self.setUniformItemSizes(True)

        # self.setSize()
        self.setStyleSheet("""QListWidget::Item {
	padding-left: 10px;
	padding-right: 10px;
	padding-bottom: 5px;
}""")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(Qt.black)
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)

        #self.itemClicked.connect(lambda x:print(x.metadata))

    def setSize(self):
        itemNum = len(self.menus)
        rows = math.ceil(itemNum / 10)
        cols = itemNum if rows == 1 else 10
        self.setMaximumSize(40 + cols * 75, rows * 80)
        self.setMinimumSize(40 + cols * 75, rows * 80)

