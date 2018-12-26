#coding=utf-8
#!/usr/bin/python

import os
import bs4
import sys
import threading
import time
import datetime
import threadpool
from collectold import collectOld
from util.logutil import log

def collect(params):
    ershoufang = collectOld()
    ershoufang.collect(params)
    ershoufang.dispose()

def collectErshoufang():
    #districtsInCd = ['jinjiang', 'longquanyi', 'qingyang', 'wuhou', 'gaoxin7', 'chenghua', 'jinniu', 'tianfuxinqu', 'gaoxinxi1',
    #                  'wenjiang','xindou','tianfuxinqunanqu', 'qingbaijiang', 'doujiangyan', 'pidou', 'shuangliu']
    districtsInCd = ['jinjiang', 'longquanyi']
    log.info('采集开始: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    startTime = time.time()
    # for district in districtsInCd:
    #     threads = []
    #     for l in range(1, 6):  # 爬图地址  一室l1,据此类推。。四室以上 l5,五个线程同时运行
    #         thread = threading.Thread(target=collect, args=(district, str(l)))
    #         thread.setDaemon(True)
    #         thread.start()
    #         threads.append(thread)
    #         #collect(district, str(l))
    #     log.info('线程JOIN: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #     for thrd in threads:
    #         thrd.join()
    #     log.info('采集完成一个区： ' + district + '   ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    params = []
    for district in districtsInCd:
        for l in range(1, 6):
            params.append({'district': district, 'l': str(l)})

    pool = threadpool.ThreadPool(8)
    works = threadpool.makeRequests(collect, params)
    log.info('pool start: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    for work in works:
        pool.putRequest(work)
    pool.wait()

    log.info('采集完成: ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '，用时：' + str(time.time() - startTime))

    after = collectOld()
    after.analyze()
    after.dispose()

def collectDeal():
    pass

def main():
    collectErshoufang()

if __name__ == '__main__':
    main()

