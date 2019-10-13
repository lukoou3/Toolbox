import traceback
import pymysql

class MysqlCursor():
    def __init__(self, host=None, port=0, user='=', passwd=None, db=None, charset='utf8'):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        print("db open......")
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is not None:
            #分别为：异常类别，异常值，追踪信息
            #print(exc_type, exc_val, exc_tb ,sep='\n')
            print(traceback.format_exc())
        print("db close.....")
        return True