
class Field:
    def __init__(self, name='', type='', comment=''):
        self.name = name
        self.type = type
        self.comment = comment
        self.is_not_null = False
        self.is_key = False
        self.is_auto_increase = False

    def __repr__(self):
        return "Field(name=%s, type=%s, comment=%s, is_not_null=%s, is_key=%s, is_auto_increase=%s)" % \
               (self.name, self.type, self.comment, self.is_not_null, self.is_key, self.is_auto_increase)

class Table:
    def __init__(self):
        self.name = ''
        self.comment = ''
        self.fields = []

    def __repr__(self):
        return "Table(name=%s, comment=%s, field=%s)" % (self.name, self.comment, repr(self.fields))

class SqlTableParse():
    def __init__(self):
        pass

    def parse_sql_text(self,sql_text):
        """
            sql文本转Table对象列表
            :param sql_text: sql文本
            :return: list of Table
        """
        pass