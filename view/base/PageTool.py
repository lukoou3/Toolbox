import math
from itertools import zip_longest

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton,  QLineEdit, QLabel

from view.base.BoxLayout import HBoxLayout
from view.base.ComboBox import ComboBox


class DisplayParam():
    def __init__(self, pageSize = 20):
        self.pageSize = pageSize
        self.currentPage = 1
        #self.totalPage = 0
        self.totalCount = 0

    @property
    def totalPage(self):
        return math.ceil(self.totalCount / self.pageSize)

    @property
    def offset(self):
        return (self.currentPage - 1) * self.pageSize

    # 获取当前页，开始条数
    @property
    def start(self):
        return (self.currentPage - 1) * self.pageSize + 1

    # 获取当前页结束条数
    @property
    def end(self):
        end = self.currentPage  * self.pageSize
        if end > self.totalCount:
            end = self.totalCount
        return end

    @property
    def prePage(self):
        if self.currentPage > 1:
            return self.currentPage - 1

    @property
    def nextPage(self):
        if self.currentPage < self.totalPage:
            return self.currentPage + 1

    @property
    def isFirstPage(self):
        return self.currentPage <= 1

    @property
    def isLastPage(self):
        return self.currentPage >= self.totalPage

class PageTool(QWidget):
    query = pyqtSignal(DisplayParam)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.displayParam = DisplayParam()

        pageSizeCombobox = ComboBox(self, datas= map(str,[10,20,50,100,200]), maximumWidth=60)  # maximumWidth=300, minimumWidth=200
        self.pageSizeCombobox = pageSizeCombobox

        preButton = QPushButton(toolTip="pre")
        #preButton.setToolTip("1111")
        preButton.setFixedSize(26, 26)
        preButton.setStyleSheet("QPushButton{border-image: url(icon/page_pre.png)}")
        self.preButton = preButton

        nextButton = QPushButton(toolTip="next")
        nextButton.setFixedSize(26, 26)
        nextButton.setStyleSheet("QPushButton{border-image: url(icon/page_next.png)}")
        self.nextButton = nextButton

        pageInput = QLineEdit(maximumWidth=35)
        self.pageInput = pageInput

        pageJumpBtn = QPushButton("确定")
        self.pageJumpBtn = pageJumpBtn

        descLabel = QLabel("")
        self.descLabel = descLabel

        pageButtons = []
        self.pageButtons = pageButtons
        for i in range(1, 10):
            pageButton = QPushButton(str(i))
            pageButton.setObjectName("page_{}".format(i))
            #可以通过ObjectName找到元素
            # print(self.findChild(QPushButton, "page_1").text())
            pageButton.setFixedSize(26, 26)
            pageButton.hide()
            pageButtons.append(pageButton)

        mainLayout = HBoxLayout(self, contentsMargins=(10, 5, 10, 5), spacing=10)
        mainLayout.addWidget(pageSizeCombobox)
        mainLayout.addWidget(preButton)
        mainLayout.addWidgets(pageButtons)
        mainLayout.addWidget(nextButton)
        mainLayout.addText("到")
        mainLayout.addWidget(pageInput)
        mainLayout.addText("页")
        mainLayout.addWidget(pageJumpBtn)
        mainLayout.addStretch(1)
        mainLayout.addWidget(descLabel)
        mainLayout.addSpacing(30)

        self.registerSignal()
        #通过下面的方式防止初始化Combobox参数时触发信号
        pageSizeCombobox.blockSignals(True)
        pageSizeCombobox.setCurrentText(str(self.displayParam.pageSize))
        pageSizeCombobox.blockSignals(False)

    def updateDisplay(self):
        self.updatePageButtons()

        displayParam = self.displayParam
        self.pageSizeCombobox.setCurrentText(str(displayParam.pageSize))
        # self.descLabel.setStyleSheet("color:blue")
        # self.descLabel.setText("共{0}条数据, 当前显示：{1} 到 {2} ".format(100, 1, 10))
        self.descLabel.setText("共<span style='color:blue'>{}</span>条数据, 当前第<span style='color:blue'>{}/{}</span>页 显示：<span style='color:blue'>{}</span> 到 <span style='color:blue'>{}</span> ".format(
            displayParam.totalCount,displayParam.currentPage , displayParam.totalPage,displayParam.start, displayParam.end))

    def updatePageButtons(self):
        pageButtons = self.pageButtons
        currentPage = self.displayParam.currentPage
        totalPage = self.displayParam.totalPage
        pageExtend = 2 #只需修改这个参数
        pageCount = pageExtend * 2 + 3 #显示数字的pageButton

        if pageCount + 2 >= totalPage:
            pages = list( range(1 , totalPage + 1) )
        else:
            pages = list( filter( lambda x: 1 <= x <= totalPage, range(currentPage - pageExtend - 1, currentPage + pageExtend + 1 + 1)) )
            if len(pages) < pageCount:
                if pages[0] == 1:
                    pages.extend( range(pages[-1]+1, pages[-1]+1 + pageCount - len(pages)) )
                else:
                    pages = list( range(pages[0] - pageCount + len(pages), pages[0]) ) + pages

            if pages[0] != 1:
                pages[0] = 1
                pages.insert(1, None)
            if pages[-1] != totalPage:
                pages[-1] = totalPage
                pages.insert(-1, None)

            #防止pageButton变化，导致nextButton位置变化，影响鼠标连点
            if pages[1] is not None:
                pages.insert(-2, pages[-3] + 1)
            if pages[-2] is not None:
                pages.insert(-1, totalPage -1)


        for page,pageButton in zip_longest(pages, pageButtons, fillvalue= -1):
            if page is None:
                pageButton.setText("...")
                pageButton.setToolTip(None)
                pageButton.show()
            elif page is -1:
                pageButton.hide()
            else:
                pageButton.setText(str(page))
                pageButton.setToolTip("第{}页".format(page))
                pageButton.show()

    def registerSignal(self):
        self.preButton.clicked.connect(self.preButtonClicked)
        self.nextButton.clicked.connect(self.nextButtonClicked)
        self.pageSizeCombobox.currentIndexChanged.connect(self.pageSizeComboboxIndexChanged)

    def pageSizeComboboxIndexChanged(self, index):
        self.displayParam.pageSize = int(self.pageSizeCombobox.currentText())
        self.displayParam.currentPage = 1#修改pageSize后，currentPage置为1
        if self.displayParam.totalCount > 0:
            self.query.emit(self.displayParam)

    def preButtonClicked(self):
        displayParam = self.displayParam
        if not displayParam.isFirstPage:
            displayParam.currentPage = displayParam.prePage
            self.query.emit(displayParam)

    def nextButtonClicked(self):
        displayParam = self.displayParam
        if not displayParam.isLastPage:
            displayParam.currentPage = displayParam.nextPage
            self.query.emit(displayParam)