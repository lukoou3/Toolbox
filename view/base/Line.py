from PyQt5.QtWidgets import QFrame

class HLine(QFrame):
    def __init__(self, parent=None, width=2):
        super().__init__(parent)

        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(width)

class VLine(QFrame):
    def __init__(self, parent=None, width=2):
        super().__init__(parent)

        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(width)
