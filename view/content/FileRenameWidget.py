import re
import sys
import os
import traceback

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QApplication, QCheckBox, QPushButton, QMessageBox, QListWidget

from view.base.BoxLayout import HBoxLayout, LayStretch
from view.base.DragLineTextEdit import DragLineTextEdit
from view.base.FileLineEdit import FileOpenDirLineEdit
from view.base.GridLayout import GLItem, GridLayout

class FileRenameWidget(QWidget):
    """
    给文件加后缀例子：(^[^\.]+) 替换成\1_26
    """
    class ReplaceTemplateWidget(QWidget):
        def __init__(self, parent=None, **kwargs):
            super().__init__(parent, **kwargs)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.fileDir = ""
        self.fileDragList = []
        self.fileList = []
        self.filterRe = ""
        self.dirDeepSearch = False
        self.filterUseRe = False
        self.replaceUseRe = False

        self.fileDirLineEdit = FileOpenDirLineEdit()
        self.dirDeepSearchCheckBox = QCheckBox("递归搜素目录")
        self.filterReLineEdit = QLineEdit(minimumWidth=240)
        self.filterUseReCheckBox = QCheckBox("使用re")
        self.replaceTmpBtn = QPushButton("模板")#"<span style='color:blue'>模板</span>"
        self.replaceOldLineEdit = QLineEdit(minimumWidth=240)
        self.replaceNewLineEdit = QLineEdit(minimumWidth=240)
        self.replaceUseReCheckBox = QCheckBox("使用re")
        self.execButton = QPushButton("execute(执行)", maximumWidth=100)
        self.replacePromptLabel = QLabel()
        self.fileListText = DragLineTextEdit()

        gridLayout = GridLayout(self, contentsMargins=(10, 10, 10, 10), spacing=10)
        replaceLayout = HBoxLayout(contentsMargins=(0, 10, 10, 10), spacing=10,
                            widgets=[self.replaceOldLineEdit, QLabel("替换成"), self.replaceNewLineEdit,
                                     self.replaceUseReCheckBox, self.replaceTmpBtn,LayStretch(1)])
        glWidgets = [
            [GLItem(QLabel("目录："), 1, 2), GLItem(self.fileDirLineEdit, 1, 4), GLItem(self.dirDeepSearchCheckBox, 1, 2),GLItem(QWidget(), 1, -1)],
            [GLItem(QLabel("过滤字符串："), 1, 2), GLItem(self.filterReLineEdit, 1, 3), GLItem(self.filterUseReCheckBox, 1, 2),GLItem(QWidget(), 1, 3)],
            [GLItem(QLabel("替换："), 1, 2),GLItem(replaceLayout, 1, -1)],
            [GLItem(self.execButton, 1, 2), GLItem(self.replacePromptLabel, 1, -1)],
            [GLItem(self.fileListText, 1, -1)]
        ]
        gridLayout.addWidgets(glWidgets)

        self.replaceTmpWidget = QListWidget(self)
        self.replaceTmpList = [{"text":"添加后缀","name":"add_suffix"}]
        self.replaceTmpWidget.addItems(replaceTmp['text'] for replaceTmp in self.replaceTmpList)
        self.replaceTmpWidget.resize(100, 300)
        self.replaceTmpWidget.hide()

        # 注册事件
        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.fileDirLineEdit.textChanged.connect(self.fileDirChanged)
        # self.filterReLineEdit.textChanged.connect(self.filterReChanged)
        # 回车触发事件（只输入\,re.compile会报错）
        self.filterReLineEdit.returnPressed.connect(self.filterReConfirm)
        self.replaceNewLineEdit.returnPressed.connect(lambda : self._setAllFileList())
        self.fileListText.dragSignal.connect(self.fileDrag)
        """
        复选框的三种状态:
        Qt.Checked:2, 组件没有被选中（默认）
        Qt.PartiallyChecked1:, 组件被半选中
        Qt.Unchecked:0, 组件被选中
        """
        #当一个信号与多个槽函数关联时，槽函数按照建立连接时的顺序依次执行。（我测试过确实是，网上有些人说的不对）
        #self.filterUseReCheckBox.stateChanged.connect(lambda state: print("111111111"))
        #self.filterUseReCheckBox.stateChanged.connect(lambda state: print("222222222"))
        self.dirDeepSearchCheckBox.stateChanged.connect(lambda state: setattr(self, "dirDeepSearch", state > 0))
        self.dirDeepSearchCheckBox.stateChanged.connect(lambda state: self._setFileList())
        self.filterUseReCheckBox.stateChanged.connect(lambda state: setattr(self, "filterUseRe", state>0) )
        self.filterUseReCheckBox.stateChanged.connect(lambda state: self._setFileList())
        self.replaceUseReCheckBox.stateChanged.connect(lambda state: setattr(self, "replaceUseRe", state>0) )
        self.replaceUseReCheckBox.stateChanged.connect(lambda state: self._setFileList())
        self.execButton.clicked.connect(self.execButtonClicked)

        self.replaceTmpBtn.clicked.connect(self.replaceTmpBtnClicked)
        self.replaceTmpWidget.itemClicked.connect(self.replaceTmpClicked)

    def replaceTmpBtnClicked(self,*param):
        if self.replaceTmpWidget.isVisible():
            self.replaceTmpWidget.hide()
        else:
            #获取纵坐标，obj.y()，包括框架。如果没有父控件是相对于桌面坐标。
            self.replaceTmpWidget.move(self.width()-100, self.replaceTmpBtn.y()+ self.replaceTmpBtn.height())
            self.replaceTmpWidget.show()
            self.replaceTmpWidget.raise_()

    def replaceTmpClicked(self,item):
        replaceTmp = self.replaceTmpList[self.replaceTmpWidget.currentRow()]
        if replaceTmp["name"] == "add_suffix":
            self.replaceOldLineEdit.setText(r"(^[^\.]+)")
            self.replaceNewLineEdit.setText(r"\1_26")
            self.replaceUseReCheckBox.setChecked(True)

        self.replaceTmpWidget.hide()

    def fileDrag(self, links):
        for link in links:
            #python集合的+=要求右边是是可迭代对象
            #self.fileDragList += link
            self.fileDragList.append(link)

        self._setAllFileList()

    def _getReplacePrompt(self, fileList):
        if len(fileList) == 0:
            self.replacePromptLabel.setText("")
        else:
            _,fileName = os.path.split(fileList[0])
            fmt = "<span style='color:#02AC03;font-size:18px;'>{}</span> 修改成：<span style='color:#02AC03;font-size:18px;'>{}</span>"
            if not self.replaceUseRe:
                self.replacePromptLabel.setText(fmt.format(fileName, fileName.replace(self.replaceOldLineEdit.text(),  self.replaceNewLineEdit.text())))
            else:
                self.replacePromptLabel.setText(fmt.format(fileName,
                                                                   re.sub(self.replaceOldLineEdit.text(), self.replaceNewLineEdit.text(), fileName) ))
    def _getAllFileList(self):
        if len(self.fileDragList) == 0:
            return self.fileList

        fileSet = set(self.fileList)
        fileList = [file for file in self.fileList]
        for file in self.fileDragList:
            if file in fileSet:
                continue
            fileList.append(file)
            fileSet.add(file)

        return fileList

    def _setAllFileList(self):
        fileList = self._getAllFileList()

        self._getReplacePrompt(fileList)
        self.fileListText.setPlainText("\n".join(fileList))

    def execButtonClicked(self, *params):
        reply = QMessageBox.information(self, '提示', '确定要修改文件名吗？', QMessageBox.Ok | QMessageBox.No,
                                        QMessageBox.No)
        if reply != QMessageBox.Ok:
            return

        old = self.replaceOldLineEdit.text()
        new = self.replaceNewLineEdit.text()

        for dirname, filename in (os.path.split(path) for path in self._getAllFileList()):
            if not self.replaceUseRe:
                newname = filename.replace(old, new)
            else:
                newname = re.sub(old, new, filename)
            if filename != newname:
                os.rename(os.path.join(dirname, filename), os.path.join(dirname, newname))

        self.fileDragList.clear()
        self._setFileList()


    def fileDirChanged(self, fileDir):
        self.fileDir = fileDir
        self._setFileList()

    def filterReChanged(self, filterRe):
        self.filterRe = filterRe
        self._setFileList()

    def filterReConfirm(self):
        self.filterRe = self.filterReLineEdit.text()
        self._setFileList()

    def _setFileList(self):
        self.fileList.clear()
        if not os.path.isdir(self.fileDir):
            return

        try:
            if self.filterUseRe:
                filterRe = re.compile(self.filterRe)
        except Exception as e:
            """如果输入\,re.compile会报错"""
            #打印堆栈信息
            #traceback.print_exc()
            # 或者得到堆栈字符串信息
            info = traceback.format_exc()
            print(info)
            return

        first = True
        for parent, dirnames, filenames in os.walk(self.fileDir):
            #只搜索一层
            if not self.dirDeepSearch and not first:
                break
            first = False
            for filename in filenames:
                if self.filterUseRe:
                    if filterRe.search(filename) is None:
                        continue
                else:
                    if self.filterRe not in filename:
                        continue
                self.fileList.append(os.path.join(parent, filename))  # 路径和文件名连接构成完整路径

        self._setAllFileList()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fennbk = FileRenameWidget()
    fennbk.resize(500, 400)
    fennbk.show()
    sys.exit(app.exec_())