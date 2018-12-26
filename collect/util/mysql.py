#coding=utf-8
#!/usr/bin/python

import threading
import pymysql
from util.mysqlpool import mysqlpool

class mysql():
    _conn = None
    def __init__(self):
        self._conn = mysqlpool.getconn()
        print('{1} - {0}'.format(mysqlpool, threading.current_thread().name))

    def execute(self, sql, param = None):
        if self._conn is None:
            self._conn = mysqlpool.getconn()
        cursor = self._conn.cursor()
        if not param:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        cursor.close()
        return count

    def executeMany(self, sql, values):
        count = self._conn.cursor().executemany(sql, values)
        return count

    def getOne(self, sql, param = None):
        cursor = self._conn.cursor()
        if not param:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = False
        cursor.close()
        return result

    def getMany(self, sql, num, param = None):
        cursor = self._conn.cursor()
        if not param:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchmany(num)
        else:
            result = False
        cursor.close()
        return result
    def getAll(self, sql, param = None):
        cursor = self._conn.cursor()
        if not param:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchall()
        else:
            result = False
        cursor.close()
        return result

    def begin(self):
        self._conn.autocommit(0)

    def end(self, option):
        if option == 'commit':
            self._conn.commit()
        else:
            self._conn.rollback()

    def dispose(self):
        self._conn.close()

    def close(self):
        self._conn.close()




