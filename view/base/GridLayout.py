from PyQt5.QtWidgets import QGridLayout, QWidget


class GLItem():
    def __init__(self, widget, rowspan=None, colspan=None):
        """widget可以使QWidget或者QLayoutItem"""
        self.widget = widget
        self.rowspan = rowspan
        self.colspan = colspan

    """
    addWidget(self, QWidget)
    addWidget(self, QWidget, int, int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
    addWidget(self, QWidget, int, int, int, int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
    
    addItem(self, QLayoutItem, int, int, rowSpan: int = 1, columnSpan: int = 1, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment())
    addItem(self, QLayoutItem)
    """

class GridLayout(QGridLayout):

    def __init__(self, *args, contentsMargins=None, spacing=None, widgets=None):
        super().__init__(*args)

        if contentsMargins is not None:
            self.setContentsMargins(*contentsMargins)
        if spacing is not None:
            self.setSpacing(spacing)

        if widgets is not None:
            self.addWidget(widgets)

    def addWidgets(self, widgets):
        for row,row_widget in enumerate(widgets):
            col = 0
            for item in row_widget:
                if not item:
                    continue
                if not isinstance(item, GLItem):
                    raise Exception("nedd GridLayoutItem")

                if item.rowspan is None or item.colspan is None:
                    if isinstance(item.widget, QWidget):
                        self.addWidget(item.widget, row, col)
                    else:
                        # 这个函数虽然没提示，但是是有的
                        self.addLayout(item.widget, row, col)
                    col = col + 1
                else:
                    # 第row行，第col列开始，占rowspan行colspan列
                    if isinstance(item.widget, QWidget):
                        self.addWidget(item.widget, row, col, item.rowspan, item.colspan)
                    else:
                        #这个函数虽然没提示，但是是有的
                        self.addLayout(item.widget, row, col, item.rowspan, item.colspan)
                    col = col + item.colspan


