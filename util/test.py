import re

class Field:
    def __init__(self, name='', type='', comment=''):
        self.name = name
        self.type = type
        self.comment = comment
        self.is_not_null = False
        self.is_key = False
        self.is_auto_increase = False

    def __repr__(self):
        return "Field(name=%s, type=%s, comment=%s)" % (self.name, self.type, self.comment)

class Table:
    def __init__(self):
        self.name = ''
        self.comment = ''
        self.fields = []

    def __repr__(self):
        return "Table(name=%s, comment=%s, field=%s)" % (self.name, self.comment, repr(self.fields))

def get_tables(sql_text):
    """
    sql文本转Table对象列表
    :param sql_text: sql文本
    :return: list of Table
    """
    tables = []
    ret = re.findall(r"create\s+(?:external\s+|)table\s+`{0,1}(.+?)`{0,1}\s*\(([^;]+?)\)[\w\d=\s]+;", sql_text, re.I)
    for per_table_ret in ret:
        table_name = per_table_ret[0].replace('\r', '').replace('\n', '')
        table_body = per_table_ret[1]
        table_body_lines = list(map(lambda x: x.strip(), table_body.strip().splitlines()))
        new_table = Table()
        # 遍历( ... )里面的每一行
        key_names = []
        for line in table_body_lines:
            if 'primary key' in line.lower():
                key_names.append(line[line.find('(') + 1:line.find(')')])
            if 'key ' not in line.lower():
                ret_line = re.search(r'`{0,1}([\w\d_]+)`{0,1}\s+([^\s,]+)\s?(.*)', line)
                field_name = ret_line.group(1)
                field_type = ret_line.group(2)
                field_tail = ret_line.group(3)
                field_comment = '--'
                if 'comment ' in field_tail:
                    field_comment = re.search(r'[\w\s\d`_]+\'(.+)\'', line).group(1)
                new_field = Field(field_name, field_type, field_comment)
                if 'not null' in line:
                    new_field.is_not_null = True
                if 'auto_increment' in line:
                    new_field.is_auto_increase = True
                new_table.fields.append(new_field)
        # 处理primary key
        for per_field in new_table.fields:
            if per_field.name in key_names:
                per_field.is_key = True
        table_comment = 'null'
        ret_comment = re.search(
            r'alter\stable\s%s.+\'(.+)\'' % table_name.strip(), sql_text)
        if ret_comment is not None:
            table_comment = ret_comment.group(1)
        new_table.comment = table_comment
        new_table.name = table_name
        tables.append(new_table)
    return tables

if __name__ == '__main__':
    print(get_tables("""create table `test_rerm` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` int(10) unsigned NOT NULL comment '1111',
  `termType` varchar(32) NOT NULL DEFAULT '',
  `vendor` varchar(32) NOT NULL,
  `date` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3001 DEFAULT CHARSET=utf8;"""))