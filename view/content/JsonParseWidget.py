import json

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QToolBar, QAction

from util import qtUtil, util
from view.base.BoxLayout import VBoxLayout
from view.base.Line import HLine
from view.base.ScrollArea import ScrollArea


class JsonParseWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.toolBar = QToolBar()
        self.resultText = QPlainTextEdit()

        self.initUI()

    def initUI(self):
        mainLayout = VBoxLayout(self)

        self.initToolBar()
        mainLayout.addWidget(self.toolBar)

        mainLayout.addWidget(HLine())

        mainLayout.addWidget(self.resultText)
        self.resultText.setObjectName('resultText')
        self.resultText.setTextInteractionFlags(Qt.TextSelectableByMouse)#仅能通过鼠标选择
        self.setStyleSheet('''
        #resultText {
        	border-radius: 5px;
        	padding: 7px;
        	color: black;
        	background: #A5D6AD;
        	font-size:18px;
        	font-family: Consolas,楷体;
        }
        QToolBar{
            background: #9DDBB4;
            border-bottom-style:1px red;
        }
        QFrame HLine{
            color: #2177C7;
        }
        ''')

        #text = """{"a":{"uid":"10","g":"3P486JMR@gmail.com","ln":"-52.3","os":"8.0.1","ba":"Sumsung","hw":"640*1136","sr":"K","ar":"MX","l":"es","vn":"1.2.8","nw":"WIFI","t":"1549703161897","md":"sumsung-0","la":"-13.3","sv":"V2.5.9","vc":"5","mid":"10"},"ap":"app","et":[{"ett":"1549653945280","kv":{"news_staytime":"9","category":"99","goodsid":"2","type1":"433","loading_time":"28","entry":"1","action":"4","showtype":"4"},"en":"newsdetail"},{"ett":"1549707695882","kv":{"errorBrief":"at cn.lift.dfdf.web.AbstractBaseController.validInbound(AbstractBaseController.java:72)","errorDetail":"at cn.lift.dfdfdf.control.CommandUtil.getInfo(CommandUtil.java:67)\\n at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)\\n at java.lang.reflect.Method.invoke(Method.java:606)\\n"},"en":"error"},{"ett":"1549662678493","kv":{"content":"命鹅闭杯雇浓猛泪铁焙铁讫湍耳扇厕次","p_comment_id":2,"comment_id":8,"addtime":"1549721327626","reply_count":106,"other_id":1,"userid":9,"praise_count":851},"en":"comment"}]}"""
        #self.resultText.setPlainText(json.dumps(json.loads(text, encoding="utf-8"), ensure_ascii=False, indent=4, separators=(',', ':')))

    def initToolBar(self):
        # 多种方式关联SLOT，多点点源码，看到函数定义，基本就知道什么意思了
        # jsonFmt.triggered.connect(self.jsonFormat)
        self.toolBar.addAction(QIcon('icon/json.png'), 'jsonFmt', self.jsonFormat)
        self.toolBar.addAction(QIcon('icon/xml2.png'), 'xml', self.jsonFormat)
        self.toolBar.addAction(QIcon('icon/copy.png'), 'copy', self.copyToClipboard)
        self.toolBar.addAction(QIcon('icon/download.png'), 'download', self.test)
        self.toolBar.addAction(QIcon('icon/clear_delete.png'), 'clear_delete', self.clearResult)

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

    def jsonFormat(self):
        text = qtUtil.getClipboardText()
        result = util.jsonFormat(text)
        qtUtil.setClipboardText(result)
        self.resultText.setPlainText(result)

    def copyToClipboard(self):
        print(self.resultText.toPlainText())
        qtUtil.setClipboardText(self.resultText.toPlainText())
        """
        plainTextEdit获得、设置文本内容的方法和一般的控件不同。
        获得文本内容：
        # 一般控件获得方式
        self.lineEdit.text()        
        # plainTextEdit获得方式
        self.plainTextEdit_5.toPlainText()

        设置文本内容：
        # 一般控件设置方法
        self.lineEdit.setText("...")    
        # plainTextEdit设置方式
        self.plainTextEdit_5.setPlainText("...")
        self.plainTextEdit_5.appendPlainText("...")   # 在原本内容基础上增加内容
        """

    def clearResult(self):
        self.resultText.clear()

    def test(self):
        text = qtUtil.getClipboardText()

        print(text)
        result = text.encode('utf-8').decode("unicode_escape")
        #text.encode('unicode_escape').decode()
        self.resultText.setPlainText(result)
