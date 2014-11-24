#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
# if(sys.platform == 'win32'):
#     encoding = "gb2312"
# else:
#     encoding = "utf8"
    
sys.setdefaultencoding("utf8")

try:
    import MySQLdb
    from MySQLdb import Error
    from Global import DBInfo
except ImportError, e:
    print 'check module error:', e
    exit()


class DBConnection:
    
    _conn = None;
    _cur = None;
    
    def __init__(self):
        try:
            # 连接数据库
            self.connect()
            self.cursor()
        except Exception, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        
    def connect(self):
        self._conn = MySQLdb.connect(host=DBInfo.host, user=DBInfo.user, passwd=DBInfo.passwd, port=DBInfo.port, charset="utf8")
        
    def cursor(self):
        self._cur = self._conn.cursor()
        
    def get_cursor(self):
        return self._cur
    
    def get_conn(self):
        return self._conn
    
    def close(self):
        self._cur.close()
        self._conn.close()
    
def main():
    db = DBConnection()
    
    conn = db.get_conn()
    if(conn == None):
        print "connect failed"
        exit(0);
    conn.select_db(DBInfo.db)
    
    cur = db.get_cursor()
    
    cur.execute("show tables;")
    
    result = cur.fetchall();
    for r in result:
        print r
        
    conn.commit()
    db.close()

if __name__ == '__main__':
    main()






