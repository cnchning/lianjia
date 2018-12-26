#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymysql, os, configparser
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB


class Config(object):
    """
    # Config().get_content("user_information")
    配置文件里面的参数
    [dbMysql]
    host = 192.168.1.80
    port = 3306
    user = root
    password = 123456
    """

    def __init__(self, config_filename="dbMysqlConfig.cnf"):
        file_path = os.path.join(os.path.dirname(__file__), config_filename)
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)

    def get_content(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.cf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return result


class BasePymysqlPool(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None


class MyPymysqlPool(BasePymysqlPool):
    """
    MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现
     获取连接对象：conn = Mysql.getConn()
     释放连接对象;conn.close()或del conn
    """
    # 连接池对象
    __pool = None

    def __init__(self, conf_name=None):
        self.conf = Config().get_content(conf_name)
        super(MyPymysqlPool, self).__init__(**self.conf)
        if MyPymysqlPool.__pool is None:
            self.__pool = PooledDB(creator=pymysql,
                              mincached=10,
                              maxcached=20,
                              maxconnections=20,
                              maxusage=0,
                              ping=4,
                              host=self.db_host,
                              port=self.db_port,
                              user=self.user,
                              passwd=self.password,
                              db=self.db,
                              use_unicode=True,
                              charset="utf8",
                              cursorclass=DictCursor)

        # 数据库构造函数，从连接池中取出连接，并生成操作游标
        # self._conn = self.__getConn()
        # self._cursor = self._conn.cursor()

    # 多线程必须每次从连接池获取新的数据库连接，多个线程公用一个连接会有问题
    def getConn(self):
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """
        return self.__pool.connection()

    def getAll(self, sql, param, conn):
        """
        @summary: 执行查询，并取出所有结果集
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list(字典对象)/boolean 查询到的结果集
        """
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchall()
        else:
            result = False
        cursor.close()
        return result

    def getOne(self, sql, param, conn):
        """
        @summary: 执行查询，并取出第一条
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchone()
        else:
            result = False
        cursor.close()
        return result

    def checkExist(self, sql, param, conn):
        if param is None:
            count = conn.cursor().execute(sql)
        else:
            count = conn.cursor().execute(sql, param)
        if count > 0:
            result = True
        else:
            result = False
        cursor.close()
        return result

    def getMany(self, sql, num, param, conn):
        """
        @summary: 执行查询，并取出num条结果
        @param sql:查询ＳＱＬ，如果有查询条件，请只指定条件列表，并将条件值使用参数[param]传递进来
        @param num:取得的结果条数
        @param param: 可选参数，条件列表值（元组/列表）
        @return: result list/boolean 查询到的结果集
        """
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        if count > 0:
            result = cursor.fetchmany(num)
        else:
            result = False
        return result

    def insertMany(self, sql, values, conn):
        """
        @summary: 向数据表插入多条记录
        @param sql:要插入的ＳＱＬ格式
        @param values:要插入的记录数据tuple(tuple)/list[list]
        @return: count 受影响的行数
        """
        count = conn.cursor().executemany(sql, values)
        return count

    def __query(self, sql, param, conn):
        cursor = conn.cursor()
        if param is None:
            count = cursor.execute(sql)
        else:
            count = cursor.execute(sql, param)
        cursor.close()
        return count

    def execute(self, sql, conn):
        return self.__query(sql, None, conn)

    def insert(self, sql, param, conn):
        """
        @summary: 更新数据表记录
        @param sql: ＳＱＬ格式及条件，使用(%s,%s)
        @param param: 要更新的  值 tuple/list
        @return: count 受影响的行数
        """
        return self.__query(sql, param, conn)

    def begin(self, conn):
        """
        @summary: 开启事务
        """
        conn.autocommit(0)

    def end(self, option, conn):
        """
        @summary: 结束事务
        """
        if option == 'commit':
            conn.commit()
        else:
            conn.rollback()

    def dispose(self):
        """
        @summary: 释放连接池资源
        """
        __pool = None

mysql = MyPymysqlPool("dbMysql")

if __name__ == '__main__':
    print('xxxxxxxxx')
    # 释放资源
    mysql.dispose()

