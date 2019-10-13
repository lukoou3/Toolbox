from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QSpacerItem, QWidget, QLayout, QLabel


class BoxLayout():
    Widget = 0
    Layout = 1
    Spacing = 2
    Stretch = 3

class LayWidget():
    def __init__(self, widget, stretch=0):
        self.widget = widget
        self.stretch = stretch

class LayLayout():
    def __init__(self, layout, stretch=0):
        self.layout = layout
        self.stretch = stretch

class LaySpacing():
    def __init__(self, spacing = 20):
        self.spacing = spacing

class LayStretch():
    def __init__(self, stretch=1):
        self.stretch = stretch

def layoutAddWidgets(layout, widgets):
    for item in widgets:
        if isinstance(item, LayWidget):
            layout.addWidget(item.widget, item.stretch)
        elif isinstance(item, LayLayout):
            layout.addLayout(item.layout, item.stretch)
        elif isinstance(item, LaySpacing):
            layout.addSpacing(item.spacing)
        elif isinstance(item, LayStretch):
            layout.addStretch(item.stretch)


# 去除了margin和spacing的布局框。
class VBoxLayout(QVBoxLayout):


    def __init__(self, *args, contentsMargins=(0, 0, 0, 0), spacing=0, widgets=None):
        super().__init__(*args)

        self.setContentsMargins(*contentsMargins)
        self.setSpacing(spacing)

        if widgets:
            self.addWidgets(widgets)

    def addWidgets(self, widgets):
        #isinstance() 会认为子类是一种父类类型，考虑继承关系
        for item in widgets:
            if isinstance(item, QWidget):
                self.addWidget(item)
            elif isinstance(item, LayWidget):
                self.addWidget(item.widget, item.stretch)
            elif isinstance(item, LayLayout):
                self.addLayout(item.layout, item.stretch)
            elif isinstance(item, LaySpacing):
                self.addSpacing(item.spacing)
            elif isinstance(item, LayStretch):
                self.addStretch(item.stretch)

class HBoxLayout(QHBoxLayout):

    def __init__(self, *args, contentsMargins=(0, 0, 0, 0), spacing=0, widgets=None):
        super().__init__(*args)

        self.setContentsMargins(*contentsMargins)
        self.setSpacing(spacing)

        if widgets:
            self.addWidgets(widgets)

    def addText(self, text):
        self.addWidget(QLabel(text))

    def addWidgets(self, widgets):
        for item in widgets:
            if isinstance(item, QWidget):
                self.addWidget(item)
            elif isinstance(item, QLayout):
                self.addLayout(item)
            elif isinstance(item, LayWidget):
                self.addWidget(item.widget, item.stretch)
            elif isinstance(item, LayLayout):
                self.addLayout(item.layout, item.stretch)
            elif isinstance(item, LaySpacing):
                self.addSpacing(item.spacing)
            elif isinstance(item, LayStretch):
                self.addStretch(item.stretch)
            else:
                self.addWidget(QLabel(str(item)))