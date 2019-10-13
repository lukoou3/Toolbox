from PyQt5.QtCore import QEvent, QPropertyAnimation
from PyQt5.QtWidgets import QWidget


class FadeWidget(QWidget):
    """支持fade的QWidget"""

    def __init__(self):
        super().__init__()
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QEvent.WindowDeactivate:
            self.halfHide()
        elif event.type() == QEvent.WindowActivate:
            self.recoverHalfHide()
        return super().eventFilter(object, event)

    def halfHide(self):
        if self.windowOpacity() < 0.05:
            return None
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(100)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0.5)
        self.animation.start()

    def recoverHalfHide(self):
        if self.windowOpacity() > 0.95:
            return None
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(100)
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(1)
        self.animation.start()

    def hide(self):
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(200)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(super().hide)
        self.animation.start()

    def show(self):
        super().show()
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()