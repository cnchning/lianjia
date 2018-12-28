#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import logging.handlers
import os
import time
import threading
import traceback

class logutil(object):
    def __init__(self, name =''):
        self.logname = name
        self.logger = logging.getLogger(name)
        # 设置输出的等级
        LEVELS = {'NOSET': logging.NOTSET,
                  'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL}
        self.loglevel = LEVELS['NOSET']
        # 创建文件目录
        logs_dir = "logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 修改log保存位置
        timestamp = time.strftime("%Y-%m-%d", time.localtime())
        logfilename = '%s.txt' % timestamp
        logfilepath = os.path.join(logs_dir, logfilename)
        rotatingFileHandler = logging.handlers.RotatingFileHandler(filename=logfilepath,
                                                                   maxBytes=1024 * 1024 * 50,
                                                                   backupCount=5)
        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        # 文件句柄
        rotatingFileHandler.setFormatter(formatter)
        # 控制台句柄
        console = logging.StreamHandler()
        console.setLevel(self.loglevel)
        console.setFormatter(formatter)
        # 添加内容到日志句柄中
        self.logger.addHandler(rotatingFileHandler)
        self.logger.addHandler(console)
        self.logger.setLevel(self.loglevel)

    def info(self, message):
        message = '[{0}] {1}'.format(threading.current_thread().name, message)
        self.logger.info(message)

    def debug(self, message):
        message = '[{0}] {1}'.format(threading.current_thread().name, message)
        self.logger.debug(message)

    def warning(self, message):
        message = '[{0}] {1}'.format(threading.current_thread().name, message)
        self.logger.warning(message)

    def error(self, err):
        if isinstance(err, Exception):
            message = '[{0}] {1}'.format(threading.current_thread().name, traceback.format_exc())
        else:
            message = '[{0}] {1}'.format(threading.current_thread().name, err)
        self.logger.error(message)

log = logutil()