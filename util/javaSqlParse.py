import re

import Levenshtein

tablename = "tablename"
class JavaParse():
    pass

def getJavaSqlField(javaCode, sqlCode):
    from util import sqlParse
    javaFields = getJavaField(javaCode)
    sqlFields = []
    sqlTables = sqlParse.parse_sql_table(sqlCode)
    if sqlTables:
        sqlFields = sqlTables[0].fields
    if len(javaFields) is 0 and len(sqlFields) is 0:
        return []

    if len(sqlFields) is 0:
        return [(fieldType, fieldName, fieldName) for fieldType, fieldName in javaFields]
    if len(javaFields) is 0:
        from util import util
        type_map = {"varchar": "String", "datetime": "Date", "bigint": "long", "smallint": "int",
                    "tinyint": "int", "int": "int", "float": "float", "double": "double"}
        return [(type_map.get(field.dtype, "String"), util.fieldname_under2camel(field.name), field.name) for field in sqlFields]

    fields = []
    for sqlField in sqlFields:
        sqlFieldName = sqlField.name
        javaField = max(javaFields, key=lambda javaField: Levenshtein.jaro(sqlFieldName.lower(), javaField[1].lower()))
        fields.append((javaField[0], javaField[1], sqlFieldName))
    return fields

def getJavaField(codeStr):
    """获得class的属性"""
    lines = codeStr.split("\n")
    fields = list()
    re_field = re.compile(r"(int|Integer|short|long|Long|double|Double|boolean|Boolean|String|Date)\s+(\w+)\s{0,2}(=|;)")
    for line in lines:
        mactch = re.search(re_field, line)
        if mactch:
            fields.append((mactch.group(1), mactch.group(2)))
    return fields

def getJavaGetMethodByField(field):
    """获得class的get方法"""
    fieldType, fieldName, sqlField = field
    if fieldType in ["boolean", "Boolean"]:
        getMethod = "is" + fieldName[0].upper() + fieldName[1:] + "()"
    else:
        getMethod = "get" + fieldName[0].upper() + fieldName[1:] + "()"
    return getMethod

def getJavaSetMethodByField(field):
    """获得class的set方法"""
    fieldType, fieldName, sqlField = field
    getMethod = "set" + fieldName[0].upper() + fieldName[1:] + "()"
    return getMethod

def getJavaSqlGetMethodByField(field, dataname="data"):
    fieldType, fieldName, sqlField = field
    if fieldType == "String":
        return "'\"+" + dataname + "." + getJavaGetMethodByField(field) + "+\"'"
    return "\"+" + dataname + "." + getJavaGetMethodByField(field) + "+\""


def getJavXmlGetMethodByField(field, dataname="data"):
    fieldType, fieldName, sqlField = field
    if fieldType == "String":
        return "'${}.{}'".format(dataname, fieldName)
    return "${}.{}".format(dataname, fieldName)


def getJdbcGetMethodByField(field, dataname="data", rstname="rst"):
    fieldType, fieldName, sqlField = field
    if fieldType in ["boolean", "Boolean"]:
        temp = """{}.{}(rst.getBoolean("{}"));"""
    elif fieldType in ["String"]:
        temp = """{}.{}(rst.getString("{}"));"""
    elif fieldType in ["long", "Long"]:
        temp = """{}.{}(rst.getLong("{}"));"""
    elif fieldType in "double|Double":
        temp = """{}.{}(rst.getDouble("{}"));"""
    else:
        temp = """{}.{}(rst.getInt("{}"));"""
    return temp.format(dataname, getJavaSetMethodByField(field)[:-2], sqlField)


def getSelectSql(fields, tablename=tablename):
    temp = "select {fields} from {tablename}"
    return temp.format(**{"fields": ",".join(sqlField for fieldType, fieldName, sqlField in fields), "tablename": tablename})


def getInsertSql(fields,tablename=tablename, dataname="data", filterNames=None):
    filterNames = filterNames if filterNames else ["id"]
    fields = [field for field in fields if field[2] not in filterNames]
    temp = "insert into {tablename}({fields}) values ({fieldValues})"
    fieldValues = (getJavaSqlGetMethodByField(field, dataname) for field in fields)
    tempdict = {"tablename": tablename, "fields": ",".join(sqlField for fieldType,fieldName,sqlField in fields),
                "fieldValues": ",".join(fieldValues)}
    return temp.format(**tempdict)


def getUpdateSql(fields, tablename=tablename, dataname="data", filterNames=None):
    filterNames = filterNames if filterNames else ["id"]
    fields = [field for field in fields if field[1] not in filterNames]
    fieldValues = (field[2] + "=" + getJavaSqlGetMethodByField(field, dataname) for field in fields)
    temp = "update {tablename} set {fieldValues} where id =\"+{whereValue}"
    tempdict = {"tablename": tablename, "fieldValues": ",".join(fieldValues), "whereValue": dataname + ".getId()"}
    return temp.format(**tempdict)


def getUpdateSqlXml(fields, tablename=tablename, dataname="addParam", filterNames=None):
    filterNames = filterNames if filterNames else ["id"]
    fields = [field for field in fields if field[1] not in filterNames]
    fieldValues = (field[2] + " = " + getJavXmlGetMethodByField(field, dataname) for field in fields)
    temp = "update {tablename}\nset {fieldValues}\nwhere id ={whereValue}"
    tempdict = {"tablename": tablename, "fieldValues": ",\n".join(fieldValues), "whereValue": "$"+dataname+".id"}
    return temp.format(**tempdict)


def getDeleteSql(tablename=tablename, dataname="data"):
    temp = "delete from {tablename} where id =\"+{whereValue}"
    return temp.format(**{"tablename": tablename, "whereValue": dataname + ".getId()"})


def getJdbcGetMethodsByFields(fields, dataname="data", rstname="rst"):
    return (getJdbcGetMethodByField(field, dataname, rstname) for field in fields)


def getSqlAddColumByFields(fields, tablename=tablename):
    return ("alter table {} add {} tinyint(2) unsigned NOT NULL DEFAULT '1' after {};".format(
        tablename, field[1], (fields[i - 1][1] if i > 0 else "aaa")
    ) for i, field in enumerate(fields))

def test():
    with open("DacHikDtServerConfParam.java", "r", encoding="gbk") as fp:
        fields = getJavaSqlField(fp.read())
        print(getSelectSql(fields, "dac_dynamicperceive_config"))
        print("#"*30)
        print(getInsertSql(fields, "dac_dynamicperceive_config"))
        print("#" * 30)
        print(getUpdateSql(fields, "dac_dynamicperceive_config"))
        print("#" * 30)
        print(getUpdateSqlXml(fields, "dac_dynamicperceive_config"))
        print("#" * 30)
        print("\n".join(getSqlAddColumByFields(fields, "dac_dynamicperceive_config")))
        print("#" * 30)
        print(getDeleteSql("dac_dynamicperceive_config"))
        print("#" * 30)
        print("\n".join(getJdbcGetMethodsByFields(fields, "data")))

def getJavaClassField(javaText):
    re_class = re.compile(r"class[\w\d\s]+\{(.+)\}", re.DOTALL)
    classContent = re_class.search(javaText).group(1)
    for line in classContent.split("\n"):
        line = line.strip()
        if line == "":
            continue
        if line.startswith("/*") or line.startswith("*") or line.startswith("*/"):
            continue
        if line.startswith("//"):
            continue
        if line.startswith("@"):
            continue

if __name__ == '__main__':

    test()