import re

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit, QPushButton, QLabel, QLineEdit

from util import javaSqlParse
from view.base.BoxLayout import HBoxLayout, LayStretch
from view.base.LineTextEdit import LineTextEdit
from view.base.RadioButtonGroup import RadioButtonGroup


class SqlJavaCodeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.sqlInTextEdit = QPlainTextEdit()
        self.javaInTextEdit = QPlainTextEdit()
        self.tableNameLineEdit = QLineEdit(minimumWidth=240)
        self.tableNameLineEdit.setText("table_name")
        self.dataNameLineEdit = QLineEdit(minimumWidth=240)
        self.dataNameLineEdit.setText("data")
        self.paramNameLineEdit = QLineEdit(minimumWidth=240)
        self.paramNameLineEdit.setText("param")
        self.outSqlTypeRadioGroup = RadioButtonGroup(datas=[{"value": 1, "text": "jdbc"},
                                                            {"value": 2, "text": "mybatis"}], value=1, maximumWidth=200)
        self.execButton = QPushButton("execute(执行)", maximumWidth=100)
        self.resultTextEdit = LineTextEdit()

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(HBoxLayout(widgets=[QLabel("sql："), QLabel("java：")]))
        mainLayout.addLayout(HBoxLayout(widgets=[self.sqlInTextEdit, self.javaInTextEdit]), 2)
        mainLayout.addLayout(HBoxLayout(widgets=[QLabel("tableName："), self.tableNameLineEdit, LayStretch(1),
                                                 QLabel("dataName："), self.dataNameLineEdit, LayStretch(1),
                                                 QLabel("paramName："), self.paramNameLineEdit, LayStretch(1)]))
        mainLayout.addLayout(HBoxLayout(widgets=[QLabel("输出sql类型："), self.outSqlTypeRadioGroup, LayStretch(1)]))
        mainLayout.addWidget(self.execButton)
        mainLayout.addWidget(self.resultTextEdit, 7)

        self.registerSignalConnect()

    def registerSignalConnect(self):
        self.sqlInTextEdit.textChanged.connect(self.sqlInTextChanged)
        self.execButton.clicked.connect(self.execButtonClicked)

    def sqlInTextChanged(self):
        text = self.sqlInTextEdit.toPlainText().strip()
        match = re.search(r"create\s+(?:external\s+|)table\s+`{0,1}(.+?)`{0,1}\s*\(", text, re.IGNORECASE)
        if match is not None:
            self.tableNameLineEdit.setText(match.group(1))

    def execButtonClicked(self, *params):
        sqlInText = self.sqlInTextEdit.toPlainText().strip()
        javaInText = self.javaInTextEdit.toPlainText().strip()
        tableName = self.tableNameLineEdit.text()
        dataName = self.dataNameLineEdit.text()
        paramName = self.paramNameLineEdit.text()
        fields = javaSqlParse.getJavaSqlField(javaInText, sqlInText)
        outSqlType = self.outSqlTypeRadioGroup.value
        if not fields:
            return

        results = []
        if outSqlType == 1:
            selectSql = javaSqlParse.getSelectSql(fields, tableName)
            results.append(selectSql)
            insertSql = javaSqlParse.getInsertSql(fields, tableName)
            results.append(insertSql)
            updateSql = javaSqlParse.getUpdateSql(fields, tableName)
            results.append(updateSql)
            updateSqlXml = javaSqlParse.getUpdateSqlXml(fields, tableName)
            results.append(updateSqlXml)
            deleteSql = javaSqlParse.getDeleteSql(tableName)
            results.append(deleteSql)
            jdbcGetMethodsByFields = "\n".join(javaSqlParse.getJdbcGetMethodsByFields(fields, dataName))
            results.append(jdbcGetMethodsByFields)
            javaGetSetMethodsByFields = "\n".join(
                javaSqlParse.getJavaGetSetMethodsByFields(fields, dataName, paramName))
            results.append(javaGetSetMethodsByFields)
        elif outSqlType == 2:
            selectSql = javaSqlParse.getMybatisSelectListSql(fields, tableName)
            results.append(selectSql)
            selectSql = javaSqlParse.getMybatisSelectOneSql(fields, tableName)
            results.append(selectSql)
            selectSql = javaSqlParse.getMybatisSelectListSql2(tableName)
            results.append(selectSql)
            selectSql = javaSqlParse.getMybatisSelectOneSql2(tableName)
            results.append(selectSql)
            insertSql = javaSqlParse.getMybatisInsertSql(fields, tableName)
            results.append(insertSql)
            updateSql = javaSqlParse.getMybatisUpdateSql(fields, tableName)
            results.append(updateSql)
            deleteSql = javaSqlParse.getMybatisDeleteSql(tableName)
            results.append(deleteSql)

        self.resultTextEdit.clear()
        first = True
        for str in results:
            if not first:
                self.resultTextEdit.appendPlainText("\n" + "#" * 10 + "\n")
            else:
                first = False
            self.resultTextEdit.appendPlainText(str)
