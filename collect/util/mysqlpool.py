#coding=utf-8
#!/usr/bin/python

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


class Base(object):
    def __init__(self, host, port, user, password, db_name):
        self.db_host = host
        self.db_port = int(port)
        self.user = user
        self.password = str(password)
        self.db = db_name
        self.conn = None
        self.cursor = None


class MysqlPool(Base):
    __pool = None
    def __init__(self, conf_name=None):
        self.conf = Config().get_content(conf_name)
        super(MysqlPool, self).__init__(**self.conf)
        if self.__pool is None:
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
    def getconn(self):
        return self.__pool.connection()

mysqlpool = MysqlPool('dbMysql')

