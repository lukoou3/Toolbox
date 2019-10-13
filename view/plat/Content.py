from PyQt5.QtWidgets import QTabWidget

from view.content.DbTablesWidget import DbTablesWidget
from view.content.FileRenameWidget import FileRenameWidget
from view.content.JsonParseWidget import JsonParseWidget
from view.content.MarkdownWidget import MarkdownWidget
from view.content.SqlParseWidget import SqlParseWidget
from view.content.DbTableWidget import DbTableWidget
from view.content.StrMapReduceWidget import StrMapReduceWidget
from view.content.TransformWidget import TransformWidget


class Content(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menuMap = {}
        self.initUI()

    def initUI(self):
        """http://www.jsons.cn/unicode/"""
        self.setContentsMargins(0, 0, 0, 0)
        self.tabBar().hide()

        str_mapreduce_widget = StrMapReduceWidget()
        self.menuMap["str_mapreduce_widget"] = str_mapreduce_widget
        self.addTab(str_mapreduce_widget, "")

        str_json_widget = JsonParseWidget()
        self.menuMap["str_json_widget"] = str_json_widget
        self.addTab(str_json_widget, "")

        str_sql_widget = SqlParseWidget()
        self.menuMap["str_sql_widget"] = str_sql_widget
        self.addTab(str_sql_widget, "")

        str_transform_widget = TransformWidget()
        self.menuMap["str_transform_widget"] = str_transform_widget
        self.addTab(str_transform_widget, "")

        str_markdown_widget = MarkdownWidget()
        self.menuMap["str_markdown_widget"] = str_markdown_widget
        self.addTab(str_markdown_widget, "")

        file_rename_widget = FileRenameWidget()
        self.menuMap["file_rename_widget"] = file_rename_widget
        self.addTab(file_rename_widget, "")

        db_tables_widget = DbTablesWidget()
        self.menuMap["db_tables_widget"] = db_tables_widget
        self.addTab(db_tables_widget, "")

        # db_table_widget = DbTableWidget()
        # self.menuMap["db_table_widget"] = db_table_widget
        # self.addTab(db_table_widget, "")

        self.setCurrentIndex(0)

    def setCurrentWidgetByMenu(self, menu):
        widget = self.menuMap.get(menu.get("contentWidget", "str_mapreduce_widget"))
        self.setCurrentWidget(widget)
        loadData = getattr(widget, "loadData", None)
        if callable(loadData):
            loadData()