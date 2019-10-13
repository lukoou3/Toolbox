from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

class SearchLineEdit(QLineEdit):
    searchSignal =  pyqtSignal(str)
    """创建一个可搜索的输入框。"""
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setMinimumSize(218, 20)

        self.button = QPushButton(self)
        self.button.setMaximumSize(16, 16)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton{border-image: url(icons/search.png)}")

        self.setTextMargins(3, 0, 19, 0)

        self.mainLayout = QHBoxLayout()
        # 添加空白区宽150px、高10px，宽度尽可能的缩小、放大
        self.spaceItem = QSpacerItem(150, 10, QSizePolicy.Expanding)
        self.mainLayout.addSpacerItem(self.spaceItem)
        # self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.button)
        self.mainLayout.addSpacing(5)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.button.clicked.connect(self.sendSearchSignal)

    def sendSearchSignal(self):
        self.searchSignal.emit(self.text())