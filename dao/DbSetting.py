import sqlite3
import os

curPath = os.path.abspath(os.path.dirname(__file__))
dbPath = os.path.abspath( os.path.join(curPath, "../db") )
dbBasePath = os.path.abspath( os.path.join(dbPath, "db_base.db") )

def initTable():
    connection = sqlite3.connect(dbBasePath)
    with connection:
        connection.execute("""create table db_setting
               (id integer primary key autoincrement,
               type int not null unique,
               host text not null,
               port int not null,
               db text,
               user text,
               passwd text,
               charset text);""")

        connection.execute("""replace into db_setting(type, host, port, db, user, passwd, charset) values ( 1,'localhost',3306,'test','root','123456','utf8') """)

def getDbSetting(type):
    connection = sqlite3.connect(dbBasePath)
    with connection:
        rst = connection.execute("""select host, port, db, user, passwd, charset from db_setting where type={}""".format(type))
        host, port, db, user, passwd, charset = rst.fetchone()
        return host, port, db, user, passwd, charset

def setDbSetting(*params):
    connection = sqlite3.connect(dbBasePath)
    with connection:
        rst = connection.execute("""replace into db_setting(type, host, port, db, user, passwd, charset) values ( ?,?,?,?,?,?,?) """,params)

if __name__ == '__main__':
    #initTable()
    getDbSetting()