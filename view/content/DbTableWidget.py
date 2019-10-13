import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor

from PyQt5.QtWidgets import QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QToolBar, QToolButton, QMenu, QAction, \
    QDialog
from quamash import QApplication

from util.MysqlCursor import MysqlCursor
from view.base.BoxLayout import VBoxLayout
from view.base.PageTool import PageTool
from view.pop.SqlTableExportDialog import SqlTableExportDialog

class DbTableWidgetDialog(QDialog):
    def __init__(self, parent=None, width=600, hight=500,host=None, port=0, user='=', passwd=None, db=None, charset='utf8',tableName= ""):
        super().__init__(parent)
        self.setWindowTitle("table")
        self.resize(width, hight)

        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.tableName = tableName

        mainLayout = VBoxLayout(self)
        self.tableWidget = DbTableWidget(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db,
                      charset=self.charset, tableName=self.tableName)
        mainLayout.addWidget(self.tableWidget)

class DbTableWidget(QWidget):
    def __init__(self, parent=None,host=None, port=0, user='=', passwd=None, db=None, charset='utf8',tableName = "", **kwargs):
        super().__init__(parent, **kwargs)
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.tableName = tableName

        mainLayout = VBoxLayout(self)

        self.toolBar = QToolBar()
        self.initToolBar()
        self.table = QTableWidget()
        self.pageTool = PageTool()

        mainLayout.addWidget(self.toolBar)
        mainLayout.addWidget(self.table)
        mainLayout.addWidget(self.pageTool)

        self.table.horizontalHeader().setStyleSheet("QHeaderView::section{background:#F3F3F3;}")
        self.table.setStyleSheet("QTableWidget{border:0 none;//最外层边框}")
        self.table.verticalHeader().setVisible(False)  # 隐藏行号
        self.table.setAlternatingRowColors(True)  # 隔行换色
        # 设置可以自适应宽度
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.registerSignalConnect()

    def loadData(self):
        self.loadTable()

    def initToolBar(self):
        exportButton = QToolButton()
        exportButton.setText("导出")
        exportButton.setObjectName("exportButton")
        exportButton.setIcon(QIcon('icon/export.png'))
        exportButton.setIconSize(QSize(24, 24))
        exportButton.setAutoRaise(True)
        exportButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)#文字显示在图标旁边

        self.toolBar.addWidget(exportButton)

    def registerSignalConnect(self):
        self.pageTool.query.connect(self.loadTable)
        #通过name查找元素
        self.toolBar.findChild(QToolButton,"exportButton").clicked.connect(self.tableExport)
        #Qt.CustomContextMenu:用户自定义菜单，需绑定事件 customContextMenuRequested，并实现 槽函数
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.tableContextMenuEvent)

    def contextMenuEvent(self, event):
        """
        Qt.DefaultContextMenu	默认菜单，重写 contextMenuEvent() 实现自定义
        """
        pass

    def tableContextMenuEvent(self, event):
        #当前行的行号
        currentRow = self.table.currentRow()
        # 所有选中item的行号
        itemSelectedRows = [r.row() for r in self.table.selectedIndexes()]
        selections = self.table.selectionModel()
        # 所有选中行的行号
        selectedRows = [r.row() for r in selections.selectedRows()]

        pmenu = QMenu(self)
        downloadAct = QAction("删除", pmenu)
        pmenu.addAction(downloadAct)
        downloadAct.triggered.connect(lambda: print(selectedRows))
        # pmenu.popup(self.table.mapToGlobal(pos))
        pmenu.popup(QCursor.pos())

    def tableExport(self):
        exportDialog = SqlTableExportDialog()
        result = exportDialog.exec_()
        if result > 0:
            fileType, filePath = exportDialog.exportParams
            if fileType == 1:
                self.tableExportCsv(filePath)
            elif fileType == 2:
                self.tableExportExcel(filePath)


    def tableExportCsv(self, filePath):
        header, datas = [], []
        with MysqlCursor() as cursor:
            cursor.execute("select * from {tableName}".format(**{"tableName":self.tableName}))
            header = [item[0] for item in cursor.description]
            #datas = cursor.fetchall()

            import csv
            with open(filePath, "w", encoding="utf-8", newline="") as fp:
                # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
                csvwriter = csv.writer(fp, dialect=("excel"), delimiter=",")
                csvwriter.writerow(header)
                #这个应该是迭代器吧，内存应该不会很多
                for row in cursor:
                    csvwriter.writerow(row)

    def tableExportExcel(self, filePath):
        # with MysqlCursor() as cursor:
        #     cursor.execute("select * from {tableName}".format(**{"tableName":self.tableName}))
        #     header = [item[0] for item in cursor.description]
        #     # datas = cursor.fetchall()
        #
        #     import pandas as pd
        #     df = pd.DataFrame(cursor, columns=header)
        #     # engine='openpyxl'或者engine='xlsxwriter'
        #     with pd.ExcelWriter('table.xlsx', engine='xlsxwriter') as writer:
        #         df.to_excel(writer, sheet_name='Sheet1', columns=None, header=True, index=False)

        import xlsxwriter
        from  datetime import datetime

        with MysqlCursor() as cursor:
            cursor.execute("select * from {tableName}".format(**{"tableName":self.tableName}))
            header = [item[0] for item in cursor.description]
            # datas = cursor.fetchall()

        workbook = xlsxwriter.Workbook(filePath)  # 新建excel表
        worksheet = workbook.add_worksheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
        worksheet.write_row('A1',header)  # 写入表头
        for row,data in enumerate(cursor,start=1):
            for col,item in enumerate(data,start=0):
                if isinstance(item, datetime):
                    worksheet.write(row,col,item.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    worksheet.write(row, col, item)
        workbook.close()  # 将excel文件保存关闭，如果没有这一行运行代码会报错

    def loadTable(self):
        table = self.table
        displayParam = self.pageTool.displayParam

        table.clearContents()
        header,datas = [], []

        with MysqlCursor(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset=self.charset) as cursor:
            queryParam = {"tableName":self.tableName,"offset":displayParam.offset,"pageSize":displayParam.pageSize}
            rows = cursor.execute("select count(*) from {tableName}".format(**queryParam))

            displayParam.totalCount = cursor.fetchone()[0]
            self.pageTool.updateDisplay()

            #需要获取列名
            #if displayParam.totalCount > 0:
            rows = cursor.execute("select * from {tableName} limit {offset},{pageSize}".format(**queryParam))
            header = [item[0] for item in cursor.description]
            datas = cursor.fetchall()

        table.setColumnCount(len(header))
        # 注意必须在初始化行列之后进行，否则，没有效果
        table.setHorizontalHeaderLabels(header)

        table.setRowCount(len(datas))
        for i,row in enumerate(datas):
            for j,data in enumerate(row, start=0):

                item = QTableWidgetItem(str(data))
                table.setItem(i, j, item)

if __name__ == '__main__':
    import os

    os.chdir("../..")
    print(os.getcwd())
    app = QApplication(sys.argv)
    # 创建窗口
    example = DbTableWidget()
    example.resize(1000,800)
    # 显示窗口
    example.show()
    example.loadTable()
    sys.exit(app.exec_())



