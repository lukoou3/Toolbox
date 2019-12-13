import re
from PyQt5.QtWidgets import QPlainTextEdit, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, \
    QWidget, QPushButton, QListView, QTextEdit

from view.base.ComboBox import ComboBox
from view.base.GridLayout import GridLayout, GLItem
from view.base.LineTextEdit import LineTextEdit
from view.base.ScrollArea import ScrollArea

sepList = [{"text": "换行符", "sep": "\n"},
           {"text": "逗号", "sep": ","},
           {"text": ";号", "sep": ";"},
           ]

extractList = [{"text": "两个反引号之间的字符", "extract_re": None, "extract": lambda line: line[line.index("`", 0) + 1:line.index("`", line.index("`", 0) + 1)]},
               {"text": "以=分割成两个字符", "extract_re": None, "extract": lambda line: line.split("=")},
               {"text": "以.分割成两个字符", "extract_re": None, "extract": lambda line: line.split(".")},
               {"text": "以:分割成两个字符", "extract_re": None, "extract": lambda line: line.split(":")},
               {"text": "原字符", "extract_re": None, "extract": lambda line: line}
               ]

formatList = [{"text": "原字符", "format_text": "{0}"},
              {"text": "java case 语句：int -> string", "format_text": """case {0}:
    str = "{1}";
    break;"""},
              {"text": 'key value："{0}":"{1}"', "format_text": '"{0}":"{1}"'}
              ]

joinList = [{"text": "换行符", "sep": "\n"},
            {"text": "逗号：, ", "sep": ","}
            ]


class StrMapReduceWidget(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.inputText = QPlainTextEdit()
        #self.resultText = QPlainTextEdit()
        self.resultText = LineTextEdit()

        mainLayout = QVBoxLayout(self)

        mainLayout.addWidget(self.inputText, 20)

        self.sepCombobox = ComboBox(self, datas=sepList)  # maximumWidth=300, minimumWidth=200
        self.sepCombobox.setView(QListView())
        # self.sepCombobox.setEditable(True)
        # self.sepCombobox.setMaxVisibleItems(6)
        self.udSepCheckBox = QCheckBox('自定义separator：')
        self.udSepInput = QLineEdit(self, minimumWidth=240)
        self.sepCombobox.currentIndexChanged.connect(lambda x: print(x))

        self.trimLineCheckBox = QCheckBox('strip/trim Line', checked=True)
        self.delBlankLineCheckBox = QCheckBox('删除空行')
        self.fmtBlankLineCheckBox = QCheckBox('format空行')

        self.extractCombobox = ComboBox(self, datas=extractList)
        self.extractCombobox.setView(QListView())
        self.udExCheckBox = QCheckBox('自定义extract：')
        self.udExInput = QLineEdit(self, minimumWidth=240)

        self.formatCombobox = ComboBox(self, datas=formatList)
        self.formatCombobox.setView(QListView())
        self.udFmtCheckBox = QCheckBox('自定义format：')
        self.udFmtInput = QLineEdit(self, minimumWidth=240)

        self.joinCombobox = ComboBox(self, datas=joinList)
        self.joinCombobox.setView(QListView())
        self.udJoinCheckBox = QCheckBox('自定义join：')
        self.udJoinInput = QLineEdit(self, minimumWidth=240)

        self.execButton = QPushButton("execute(执行)", maximumWidth=100)

        gridLayout = GridLayout()
        glWidgets = [
            [GLItem(QLabel("separator："), 1, 1), GLItem(self.sepCombobox, 1, 3), GLItem(self.udSepCheckBox, 1, 1),
             GLItem(self.udSepInput, 1, 3), GLItem(QWidget(), 1, 1)],
            [GLItem(QLabel("extract："), 1, 1), GLItem(self.extractCombobox, 1, 3), GLItem(self.udExCheckBox, 1, 1),
             GLItem(self.udExInput, 1, 3), GLItem(QWidget(), 1, 1)],
            [GLItem(QLabel("format："), 1, 1), GLItem(self.formatCombobox, 1, 3), GLItem(self.udFmtCheckBox, 1, 1),
             GLItem(self.udFmtInput, 1, -1)],
            [GLItem(QLabel("join："), 1, 1), GLItem(self.joinCombobox, 1, 3), GLItem(self.udJoinCheckBox, 1, 1),
             GLItem(self.udJoinInput, 1, 3), GLItem(QWidget(), 1, 1)],
            [GLItem(self.trimLineCheckBox, 1, 1), GLItem(self.delBlankLineCheckBox, 1, 1),
             GLItem(self.fmtBlankLineCheckBox, 1, 1), GLItem(QWidget(), 1, -1)],
            [GLItem(self.execButton, 1, 2), GLItem(QWidget(), 1, -1)],
        ]
        gridLayout.addWidgets(glWidgets)
        mainLayout.addLayout(gridLayout)

        mainLayout.addWidget(self.resultText, 60)

        # 注册事件
        self.registerSignalConnect()

        self.setQssStyle()

    def registerSignalConnect(self):
        self.execButton.clicked.connect(self.execButtonClicked)

    def execButtonClicked(self, *params):
        text = self.inputText.toPlainText()
        sepData = self.sepCombobox.getCurrentData()
        extractData = self.extractCombobox.getCurrentData()
        formatData = self.formatCombobox.getCurrentData()
        joinData = self.joinCombobox.getCurrentData()

        if self.udSepCheckBox.isChecked():
            sepData = {"text": "", "sep": self.udSepInput.text()}
        if self.udExCheckBox.isChecked():
            extractData = {"text": "", "extract_re": self.udExInput.text().strip(), "extract": None}
        if self.udFmtCheckBox.isChecked():
            formatData = {"text": "", "format_text": self.udFmtInput.text().strip().replace(r"\s",
                                                                                            " ").replace(r"\n", "\n")}
        if self.udJoinCheckBox.isChecked():
            joinData = {"text": "", "sep": self.udJoinInput.text()}

        result = self.strMapReduce(text, sepData, extractData, formatData, joinData)
        self.resultText.setPlainText(result)

    def strMapReduce(self, text, sepData, extractData, formatData, joinData):
        def getExtractStrs(extractData, line):
            extract = extractData.get("extract")
            if extract:
                extract_strs = extract(line)
            else:
                extract_re = re.compile(extractData.get("extract_re"))
                groups = extract_re.groups
                match = extract_re.search(line)
                if groups is 0:
                    extract_strs = match.group()
                else:
                    extract_strs = match.groups()

            if not isinstance(extract_strs, (list, tuple)):
                extract_strs = (extract_strs, )
            return extract_strs

        def fmtLine(line):
            if line.strip() is "":
                return line if not fmtBlankLine else formatData.get("format_text").format(line)
            else:
                extract_strs = getExtractStrs(extractData, line)
                return formatData.get("format_text").format(*extract_strs)

        trimLine = self.trimLineCheckBox.isChecked()
        delBlankLine = self.delBlankLineCheckBox.isChecked()
        fmtBlankLine = self.fmtBlankLineCheckBox.isChecked()

        lines = [line.strip() if trimLine else line
                 for line in text.split(sepData.get("sep"))
                 if not delBlankLine or line.strip()]
        """
        lines = [(line, ) if line == "" else getExtractStrs(extractData, line)
                 for line in lines]
        lines = [formatData.get("format_text").format(*extract_strs) if extract_strs != ("", ) or fmtBlankLine else extract_strs[0]
                 for extract_strs in lines]
        """
        lines = [fmtLine(line) for line in lines]
        return joinData.get("sep").join(lines)

    def setQssStyle(self):
        self.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #bebebe;
                padding: 1px 18px 1px 3px;
                font: normal normal 16px "Microsoft YaHei";
                color: #555555;
                background: transparent;
            }


            QComboBox:editable{
                background: transparent;
            }

            QComboBox:!editable, QComboBox::drop-down:editable{
                background: transparent;
            }

            QComboBox:!editable:on, QComboBox::drop-down:editable:on{
                background: transparent;
            }


            QComboBox:on{ /* the popup opens */
                color: #555555;
                border-color: #327cc0;
                background: transparent;
            }


            QComboBox::drop-down{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: darkgray;
            }

            QComboBox::down-arrow{
                image:url(icon/arrow.png);
            }

            QComboBox::down-arrow:on {
                image:url(icon/arrow.png);
            }


            QComboBox QAbstractItemView {
                outline: 0; 
                border: 1px solid #327cc0;
                background-color: #F1F3F3;
                font: normal normal 14px "Microsoft YaHei";
            }

            QComboBox QAbstractItemView::item {
                height: 32px;
                color: #555555;
                background-color: transparent;
            }

            QComboBox QAbstractItemView::item:hover {
                color: #FFFFFF;
                background-color: #327cc0;
            }

            QComboBox QAbstractItemView::item:selected {
                color: #FFFFFF;
                background-color: #327cc0;
            }

            QComboBox QAbstractScrollArea QScrollBar:vertical {
                background-color: #d0d2d4;
            }

            QComboBox QAbstractScrollArea QScrollBar::handle:vertical {
                background: rgb(160,160,160);
            }

            QComboBox QAbstractScrollArea QScrollBar::handle:vertical:hover {
                background: rgb(90, 91, 93);
            }
            """
        )
