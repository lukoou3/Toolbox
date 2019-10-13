from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QPushButton

from util import markdownUtil
from view.base.ComboBox import ComboBox
from view.base.LineTextEdit import LineTextEdit
from view.base.ScrollArea import ScrollArea


markdownHandlers = [{"text": "url or html，转换页面上所有table到markdown table", "handler": markdownUtil.html_tables_to_markdown},
                    {"text": "html ul 转换成markdown形式的无序列表","handler": markdownUtil.html_ul_to_markdown},
                    {"text": "纯文本 转换成markdown形式的无序列表","handler": markdownUtil.text_to_markdown_ul},
                    {"text": "文本前面添加序号","handler": markdownUtil.text_addnum},
                    ]

class MarkdownWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.inputText = QPlainTextEdit()
        self.handlerCombobox = ComboBox(self, datas=markdownHandlers)
        self.execButton = QPushButton("execute(执行)", maximumWidth=100)
        self.resultText = LineTextEdit()

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(self.inputText, 20)
        mainLayout.addWidget(self.handlerCombobox)
        mainLayout.addWidget(self.execButton)
        mainLayout.addWidget(self.resultText, 70)

        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.execButton.clicked.connect(self.execButtonClicked)

    def execButtonClicked(self, *params):
        text = self.inputText.toPlainText().strip()

        try:
            markdownHandler = self.handlerCombobox.getCurrentData()
            result = markdownHandler.get("handler")(text)
        except Exception as e:
            result = str(type(e)) + '\n' + str(e)

        self.resultText.setPlainText(result)