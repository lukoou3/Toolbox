from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QFileDialog, QApplication



class FileSaveLineEdit(QLineEdit):
    """创建一个可选择文件保存路径的输入框。"""
    def __init__(self, parent=None, directory = "",filter='', **kwargs):
        super().__init__( **kwargs)
        self.parent = parent
        self.directory = directory
        self.filter = filter

        self.button = QPushButton(self)
        self.button.setMaximumSize(16, 16)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton{border-image: url(icon/ellipsis.png)}")

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

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.button.clicked.connect(self.saveFileSelect)

    def saveFileSelect(self):
        fileName = QFileDialog.getSaveFileName(self, '', self.directory,self.filter)
        if fileName[0]:
            self.setText(fileName[0])

class FileOpenDirLineEdit(QLineEdit):
    """创建一个可选择文件打开目录的输入框。"""
    def __init__(self, parent=None, caption='', directory = "", **kwargs):
        super().__init__( **kwargs)
        self.parent = parent
        self.caption = caption
        self.directory = directory

        self.button = QPushButton(self)
        self.button.setMaximumSize(16, 16)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton{border-image: url(icon/ellipsis.png)}")

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

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.button.clicked.connect(self.openFileSelect)

    def openFileSelect(self):
        #如果点取消，会返回空字符串
        filePath = QFileDialog.getExistingDirectory(self, caption='', directory='')
        if filePath:
            self.setText(filePath)

class FileOpenFileLineEdit(QLineEdit):
    """创建一个可选择文件打开文件的输入框。"""
    def __init__(self, parent=None, caption='', directory = "", filter='', **kwargs):
        super().__init__( **kwargs)
        self.parent = parent
        self.caption = caption
        self.directory = directory
        self.filter = filter

        self.button = QPushButton(self)
        self.button.setMaximumSize(16, 16)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet("QPushButton{border-image: url(icon/ellipsis.png)}")

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

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.button.clicked.connect(self.openFileSelect)

    def openFileSelect(self):
        fileName = QFileDialog.getOpenFileName(self, self.caption, self.directory, self.filter)
        if fileName[0]:
            self.setText(fileName[0])


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = FileOpenDirLineEdit()
    ex.show()
    sys.exit(app.exec_())