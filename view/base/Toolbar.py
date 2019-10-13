from PyQt5.QtWidgets import QToolBar, QFrame, QWidget


class Toolbar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

    def action(self, qIcon, text, handler):
        """
        对装饰器的探索，在类里面，自己调自己暂时实现不了
        :param qIcon:QIcon
        :param text:str
        :param handler:PYQT_SLOT
        :return:
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func

        return decorator

    @action(1,"a","b","v")
    def test(self):
        print(3)


    """
    有多种方式关联SLOT，多点点源码，看到函数定义，基本就知道什么意思了：
    1、QAction.triggered.connect
    2、Toolbar.addAction
    3、Toolbar.actionTriggered[QAction].connect
    
    toolBar = QToolBar()
    jsonFmt = QAction(QIcon('icon/json.png'), 'jsonFmt', self)
    #多种方式关联SLOT，多点点源码，看到函数定义，基本就知道什么意思了
    #jsonFmt.triggered.connect(self.jsonFormat)
    toolBar.addAction(QIcon('icon/json.png'), 'jsonFmt', self.jsonFormat)
    xml = QAction(QIcon('icon/xml2.png'), 'xml',self)
    xml.triggered.connect(lambda x: print("xml1:"+str(x)))
    toolBar.addAction(xml)
    copy = QAction(QIcon('icon/copy.png'), 'copy',self)
    toolBar.addAction(copy)
    download = QAction(QIcon('icon/download.png'), 'download', self)
    toolBar.addAction(download)
    clear = QAction(QIcon('icon/clear_delete.png'), 'clear', self)
    toolBar.addAction(clear)
    mainLayout.addWidget(toolBar)

    toolBar.actionTriggered[QAction].connect(lambda x: print(x.text()))
    """