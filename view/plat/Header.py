from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QFrame, QLabel, QPushButton


class Header(QFrame):
    def __init__(self, parent=None):
        """头部区域，包括图标/最大/小化/关闭。"""
        super().__init__()

        self.setObjectName('Header')
        self.parent = parent

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setSpacing(5)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.addSpacing(5)

        self.logoLabel = QLabel()
        self.logoLabel.setMaximumSize(24, 24)
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QPixmap("icon/tool_logo.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setObjectName("logoLabel")
        self.mainLayout.addWidget(self.logoLabel)


        self.titleLabel = QLabel()
        self.titleLabel.setText("<b>Toolbox</b>")
        self.mainLayout.addWidget(self.titleLabel)

        self.mainLayout.addStretch(1)

        self.minButton = QPushButton('—')
        self.minButton.setObjectName("minButton")
        self.minButton.setMinimumSize(20, 20)
        self.minButton.setMaximumSize(20, 20)
        self.mainLayout.addWidget(self.minButton)

        self.maxButton = QPushButton("□")
        self.maxButton.setObjectName("maxButton")
        self.maxButton.setMinimumSize(20, 20)
        self.maxButton.setMaximumSize(20, 20)
        self.mainLayout.addWidget(self.maxButton)

        self.closeButton = QPushButton("×")
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setMinimumSize(20, 20)
        self.closeButton.setMaximumSize(20, 20)
        self.mainLayout.addWidget(self.closeButton)

        self.mainLayout.addSpacing(5)
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setStyleSheet("QPushButton{text-align : center center;} #Header{background: #A5D6AD;}")

    # 事件。
    """重写鼠标事件，实现窗口拖动。"""
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.m_drag = True
            self.parent.m_DragPosition = event.globalPos() - self.parent.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() and Qt.LeftButton:
                self.parent.move(event.globalPos() - self.parent.m_DragPosition)
                event.accept()
        except AttributeError:
            pass

    def mouseReleaseEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.m_drag = False