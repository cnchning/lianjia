#coding=utf-8
#!/usr/bin/python

import os
import time
import sys
import threading
import datetime
import threadpool
from util.logutil import log
from util.mysql import mysql
from collectold import collectOld

class Aaa():
    __obj = None
    def __init__(self, obj):
        self.__obj = obj
    def new(self, obj):
        self.__obj = obj
    def get(self):
        return self.__obj

aaa = Aaa(0)

def change(num):
    aaa.new(num)
    conn = mysql()
    conn.execute('select now()')
    time.sleep(num)
    log.debug(threading.current_thread().getName() + ' ' + str(aaa.get()) + '   ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#测试多线程共享一个对象，进程之间会共享数据
def main():

    abc = [{'a':x,'b':y} for x in range(5) for y in range(100, 105)]
    log.debug(abc)


    threads = []
    for l in range(1, 11):
        thread = threading.Thread(target=change, args=(l,))
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)

    log.info('JOIN: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for thrd in threads:
        thrd.join()
    log.info('完成： ' + '   ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    pool = threadpool.ThreadPool(4)
    nums = range(1, 11)
    works = threadpool.makeRequests(change, nums)
    log.info('pool start: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for work in works:
        pool.putRequest(work)
    pool.wait()
    log.info('pool end： ' + '   ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':
    main()