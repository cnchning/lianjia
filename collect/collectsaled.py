#coding=utf-8
#!/usr/bin/python

import requests
import os
import re
import bs4
from bs4 import BeautifulSoup
import sys
import decimal
import time
import datetime
from util.mysql import mysql
from util.logutil import log


class collectOld():
    def __init__(self):
        self._conn = mysql()
    def write_house(self, param):
        try:
            sql = '''insert ignore into houseA (id,title,housing_estate,position,district,city,bedroom_num,livingroom_num,bathroom_num,build_area,inside_area,unit_price,total_price,follow,
            take_look,pub_date,build_year, lastdeal_date,yearlimit,use_type,use_year,ownership,fitment,elevator_num,house_num,structure,tag,build_structure,floor,direction,build_type) 
            VALUES(%(id)s,%(title)s,%(housing_estate)s, %(position)s,%(district)s,%(city)s,%(bedroom_num)s,%(livingroom_num)s,%(bathroom_num)s,%(build_area)s,%(inside_area)s,
            %(unit_price)s,%(total_price)s,%(follow)s,%(take_look)s,%(pub_date)s,%(build_year)s,%(lastdeal_date)s,%(yearlimit)s,%(use_type)s,%(use_year)s,%(ownership)s,
            %(fitment)s,%(elevator_num)s,%(house_num)s,%(structure)s,%(tag)s,%(build_structure)s,%(floor)s,%(direction)s,%(build_type)s)'''
            self._conn.execute(sql, param)
            self._conn.end("commit")
        except Exception as e:
            log.error('=========================insert house table error===================')
            # raise e
            log.error(e)

    def get_house(self, id):
        sql = 'select id,title,unit_price,total_price,updateTime,build_area,touchTime from houseA where id=%(id)s'
        param = {'id': id}
        return self._conn.getOne(sql, param)

    def write_room(self, param):
        try:
            sql = "insert ignore into room (id,title,area,window,direction) VALUES(%(id)s,%(title)s,%(area)s,%(window)s,%(direction)s)"
            self._conn.execute(sql, param)
            self._conn.end("commit")
        except Exception as e:
            log.error('-------------------------insert room table error-----------------------')
            # raise e
            log.error(e)

    def update_houseprice(self, houseparam, pricelogparam):
        try:
            sql = "insert ignore into pricelog (id,unit_price,total_price,unit_change,total_change,pricetrend,pricetype,thedate,createDate)  " \
                  "VALUES(%(id)s,%(unit_price)s,%(total_price)s,%(unit_change)s,%(total_change)s,%(pricetrend)s,%(pricetype)s,%(thedate)s,now())"
            self._conn.execute(sql, pricelogparam)

            sql = "update houseA set unit_price=%(unit_price)s,total_price=%(total_price)s,build_area=%(build_area)s,updateTime=now() where id=%(id)s"
            self._conn.execute(sql, houseparam)

            self._conn.end("commit")
        except Exception as e:
            log.error('-------------------------update house updatetime error-----------------------')
            # raise e
            log.error(e)

    def touch_house(self, param):
        try:
            sql = "update houseA set touchTime=now() where id=%(id)s"
            self._conn.execute(sql, param)
            self._conn.end("commit")
        except Exception as e:
            log.error('-------------------------update house touch_time error-----------------------')
            # raise e
            log.error(e)

    def analyze(self):
        try:
            districtSql = '''insert IGNORE into avgDistrict(ymd,district,bedroom_num,unit_price,total_price,build_area,inside_area,num_house,follow,take_look)
            select DATE_FORMAT(NOW(),'%Y%m%d') as dd,district,bedroom_num,
                cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as avgUnitPrice, 
                cast(sum(total_price)/count(0) as DECIMAL(10,2)) as avgTotalPrice,
                cast(sum(build_area)/count(0) as DECIMAL(10,2)) as avgBuildArea,    
                cast(sum(inside_area)/count(0) as DECIMAL(10,2)) as avgInsideArea,
                count(0) as numhouse,
                cast(sum(follow)/count(0) as DECIMAL(10,2)) as avgFollow,
                cast(sum(take_look)/count(0) as DECIMAL(10,2)) as avgTakeLook
             from houseA where DATEDIFF(touchTime, NOW())=0
                group by district,bedroom_num having count(0)>10 order by district,bedroom_num'''
            positionSql = '''insert IGNORE into avgPosition(ymd,position,bedroom_num,unit_price,total_price,build_area,inside_area,num_house,follow,take_look)
                    select DATE_FORMAT(NOW(),'%Y%m%d') as dd,position,bedroom_num,
                        cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as avgUnitPrice, 
                        cast(sum(total_price)/count(0) as DECIMAL(10,2)) as avgTotalPrice,
                        cast(sum(build_area)/count(0) as DECIMAL(10,2)) as avgBuildArea,    
                        cast(sum(inside_area)/count(0) as DECIMAL(10,2)) as avgInsideArea,
                        count(0) as numhouse,
                        cast(sum(follow)/count(0) as DECIMAL(10,2)) as avgFollow,
                        cast(sum(take_look)/count(0) as DECIMAL(10,2)) as avgTakeLook
                     from houseA where DATEDIFF(touchTime, NOW())=0
                        group by position,bedroom_num having count(0)>10 order by position,bedroom_num'''
            estateSql = '''insert IGNORE into avgEstate(ymd,housing_estate,bedroom_num,unit_price,total_price,build_area,inside_area,num_house,follow,take_look)
            select DATE_FORMAT(NOW(),'%Y%m%d') as dd,housing_estate,bedroom_num,
                cast(sum(unit_price)/count(0) as DECIMAL(10,2)) as avgUnitPrice, 
                cast(sum(total_price)/count(0) as DECIMAL(10,2)) as avgTotalPrice,
                cast(sum(build_area)/count(0) as DECIMAL(10,2)) as avgBuildArea,    
                cast(sum(inside_area)/count(0) as DECIMAL(10,2)) as avgInsideArea,
                count(0) as numhouse,
                cast(sum(follow)/count(0) as DECIMAL(10,2)) as avgFollow,
                cast(sum(take_look)/count(0) as DECIMAL(10,2)) as avgTakeLook
             from houseA where DATEDIFF(touchTime, NOW())=0
                group by housing_estate,bedroom_num having count(0)>10 order by housing_estate,bedroom_num'''
            # insert IGNORE into maininfo(ymd, num_house, avg_total_price, avg_unit_price, num_priceup, num_pricedown)
            mainSql = '''insert IGNORE into maininfo(ymd, num_house,avg_unit_price,avg_total_price,num_priceup,num_pricedown)
            select DATE_FORMAT(NOW(),'%Y%m%d') as ymd, numhouse,unit_price,total_price,numup,numdown from
                (select count(0) as numhouse,sum(unit_price)/count(0) as unit_price,sum(total_price)/count(0) as total_price, 1 as col from houseA where DATEDIFF(touchTime,NOW())=0) as h
                inner join (select count(0) as numup, 1 as col from pricelog where pricetrend='up' and DATEDIFF(createDate,NOW())=0) as up on h.col=up.col
                inner join (select count(0) as numdown,1 as col from pricelog where pricetrend='down' and DATEDIFF(createDate,NOW())=0) as down on h.col=down.col'''
            cnt = self._conn.execute(districtSql)
            log.debug('行政区生成统计数据条数：' + repr(cnt))
            cnt = self._conn.execute(positionSql)
            log.debug('区域生成统计数据条数：' + repr(cnt))
            cnt = self._conn.execute(estateSql)
            log.debug('小区生成统计数据条数：' + repr(cnt))
            cnt = self._conn.execute(mainSql)
            log.debug('mainInfo data generated successful')
            self._conn.end("commit")
        except Exception as e:
            log.error('===============analyze data error========')
            log.error(e)
            raise e

    def getNumber(self, chineseNumber):
        tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
               '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20,
               '二十一': 21, '二十二': 22, '二十三': 23, '二十四': 24, '二十五': 25, '二十六': 26, '二十七': 27, '二十八': 28, '二十九': 29,
               '三十': 30,
               '三十一': 31, '三十二': 32, '三十三': 33, '三十四': 34, '三十五': 35, '三十六': 36, '三十七': 37, '三十八': 38, '三十九': 39,
               '四十': 40,
               '四十一': 41, '四十二': 42, '四十三': 43, '四十四': 44, '四十五': 45, '四十六': 46, '四十七': 47, '四十八': 48, '四十九': 49,
               '五十': 50,
               '五十一': 51, '五十二': 52, '五十三': 53, '五十四': 54, '五十五': 55, '五十六': 56, '五十七': 57, '五十八': 58, '五十九': 59,
               '六十': 60,
               '六十一': 61, '六十二': 62, '六十三': 63, '六十四': 64, '六十五': 65, '六十六': 66, '六十七': 67, '六十八': 68, '六十九': 69,
               '七十': 70,
               '七十一': 71, '七十二': 72, '七十三': 73, '七十四': 74, '七十五': 75, '七十六': 76, '七十七': 77, '七十八': 78, '七十九': 79,
               '八十': 80,
               '八十一': 81, '八十二': 82, '八十三': 83, '八十四': 84, '八十五': 85, '八十六': 86, '八十七': 87, '八十八': 88, '八十九': 89,
               '九十': 90
               }
        return tmp[chineseNumber]

    def collect(self, param):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
        patternRoom = re.compile(r'\D*(\d+)室(\d+)厅(\d*)厨*(?P<bath>\d*)卫*\s*')
        page_max = 100
        cnt = 0
        district = param['district']
        l = param['l']
        for i in range(1, int(page_max) + 1):
            pageUrl = 'https://cd.lianjia.com/ershoufang/' + district + '/l' + l + '/pg' + str(i)
            if i == 1:
                pageUrl = 'https://cd.lianjia.com/ershoufang/' + district + '/l' + l + '/'
            startTime = time.time()
            log.info('开始采集： ' + pageUrl)
            res = requests.get(pageUrl, headers=headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            ul = soup.find('ul', class_='sellListContent')
            if ul is None:
                break
            li_max = ul.find_all('li')
            for li in li_max:
                try:
                    cnt += 1
                    house_param = {}
                    house_param['title'] = li.find('div', class_='title').text
                    houseUrl = li.find('div', class_='title').find('a').attrs['href']
                    houseId = re.sub("\D", "", houseUrl)
                    house_param['id'] = houseId
                    log.info(district + '-' + l + '-' + str(cnt) +': ' +
                             houseId + ':' + house_param['title'] + ' ' + houseUrl)
                    # --------------------------------------------------------#  价钱
                    totalprice = li.find('div', class_='totalPrice').text
                    totalprice = decimal.Decimal(re.sub(r"[^\d\.]", "", totalprice))
                    house_param['total_price'] = totalprice
                    unitprice = li.find('div', class_='unitPrice').text
                    unitprice = decimal.Decimal(re.sub(r"[^\d\.]", "", unitprice))
                    house_param['unit_price'] = unitprice

                    #  东洪广厦 | 3室1厅 | 87.82平米 | 东南 | 精装 | 有电梯
                    #  加国枫韵 | 车位 | 109平米 | 西南 | 无电梯    (车位）
                    #  浣花里100号  | 叠拼别墅 | 6室2厅 | 235.66平米 | 东 | 其他 | 有电梯 （别墅）
                    content = li.find('div', class_='houseInfo').text
                    content = content.split("|")
                    house_param['housing_estate'] = content[0]
                    buildArea = re.sub(r"[^\d\.]", "", content[2] if len(content) < 7 else content[3])
                    house_param['build_area'] = buildArea if re.match(r"\d+\.*\d*", buildArea) else 0
                    # --------------------------------------------------------#
                    # {'id': 106101546082, 'title': '华韵天府双卫套四，朝西南，对创意山', 'unit_price': Decimal('23521.00'), 'total_price': Decimal('207.00'), 'updateTime': datetime.datetime(2018, 12, 11, 16, 34, 9)}
                    house = self.get_house(houseId)
                    if house:
                        touchParam = {'id': houseId}
                        self.touch_house(touchParam)
                        if house['total_price'] != totalprice:
                            log.debug('price changed, ID: ' + houseId + ':' + house_param['title'])
                            param1 = {'id': houseId, 'unit_price': unitprice, 'total_price': totalprice,
                                      'build_area': house_param['build_area']}
                            priceTrend = 'up' if unitprice > house['unit_price'] else 'down'
                            param2 = {'id': houseId, 'unit_price': house['unit_price'],
                                      'total_price': house['total_price'],
                                      'unit_change': unitprice - house['unit_price'],
                                      'total_change': totalprice - house['total_price'], 'pricetrend': priceTrend,
                                      'thedate': house['updateTime'], 'pricetype': 'quote'}
                            self.update_houseprice(param1, param2)

                        continue

                    house_param['city'] = '成都'

                    # --------------------------------------------------------#
                    #  位置 水清沟
                    position = li.find('div', class_='positionInfo').find('a').text
                    house_param['position'] = position
                    # --------------------------------------------------------#
                    # 57人关注 / 共13次带看 / 6个月以前发布
                    follow = li.find('div', class_='followInfo').text
                    follow = follow.split("/")
                    house_param['follow'] = re.sub("\D", "", follow[0])
                    house_param['take_look'] = re.sub("\D", "", follow[1])

                    res = requests.get(houseUrl, headers=headers)
                    soup = BeautifulSoup(res.text, 'html.parser')

                    baseinfo = soup.find('div', class_='base')
                    baselis = baseinfo.find_all('li')
                    if len(baselis) > 3:
                        matchRoom = patternRoom.match(baselis[0].text)
                        bedroom_num = decimal.Decimal(matchRoom.group(1))
                        house_param['bedroom_num'] = bedroom_num if bedroom_num < 6 else 5
                        house_param['livingroom_num'] = matchRoom.group(2)
                        numBathroom = matchRoom.group('bath')
                        house_param['bathroom_num'] = 1 if numBathroom == '' else numBathroom
                    else:
                        house_param['bedroom_num'] = 0
                        house_param['livingroom_num'] = 0
                        house_param['bathroom_num'] = 0

                    if len(baselis) == 12:
                        insideArea = re.sub(r"[^\d\.]", "", baselis[4].text)
                        house_param['inside_area'] = insideArea if re.match(r"\d+\.*\d*", insideArea) else 0
                        house_param['fitment'] = baselis[8].text.replace('装修情况', '')
                        useyear = re.sub(r"\D", "", baselis[11].text)
                        house_param['use_year'] = useyear if re.match(r'\d+', useyear) else 0
                        house_param['structure'] = baselis[3].text.replace('户型结构', '')
                        house_param['build_structure'] = baselis[7].text.replace('建筑结构', '')
                        house_param['floor'] = baselis[1].text.replace('所在楼层', '')
                        house_param['elevator_num'] = 0 if baselis[10].text.replace('配备电梯', '') == '无' \
                            else self.getNumber(re.sub(r'梯.+', '', baselis[9].text.replace('梯户比例', '')))
                        house_param['house_num'] = self.getNumber(re.sub(r'.+梯', '', baselis[9].text.replace('户', '')))
                        house_param['direction'] = baselis[6].text.replace('房屋朝向', '')
                        house_param['build_type'] = baselis[5].text.replace('建筑类型', '')
                    elif len(baselis) == 3:  # 车位
                        insideArea = re.sub(r"[^\d\.]", "", baselis[1].text)
                        house_param['inside_area'] = insideArea if re.match(r"\d+\.*\d*", insideArea) else 0
                        house_param['fitment'] = '车位'
                        house_param['use_year'] = 0
                        house_param['structure'] = ''
                        house_param['build_structure'] = ''
                        house_param['floor'] = baselis[0].text.replace('所在楼层', '')
                        house_param['elevator_num'] = 0
                        house_param['house_num'] = 1
                        house_param['direction'] = baselis[2].text.replace('房屋朝向', '')
                        house_param['build_type'] = '车位'
                    else:  # 别墅
                        insideArea = re.sub(r"[^\d\.]", "", baselis[3].text)
                        house_param['inside_area'] = insideArea if re.match(r"\d+\.*\d*", insideArea) else 0
                        house_param['fitment'] = baselis[6].text.replace('装修情况', '')
                        useyear = re.sub(r"\D", "", baselis[8].text)
                        house_param['use_year'] = useyear if re.match(r'\d+', useyear) else 0
                        house_param['structure'] = baselis[7].text.replace('别墅类型', '')
                        house_param['build_structure'] = baselis[5].text.replace('建筑结构', '')
                        house_param['floor'] = baselis[1].text.replace('所在楼层', '')
                        house_param['elevator_num'] = 0
                        house_param['house_num'] = 1
                        house_param['direction'] = baselis[4].text.replace('房屋朝向', '')
                        house_param['build_type'] = '别墅'

                    transinfo = soup.find('div', class_='transaction')
                    translis = transinfo.find_all('div')[1].ul.find_all('li')
                    house_param['pub_date'] = translis[0].find_all('span')[1].text
                    house_param['ownership'] = translis[1].find_all('span')[1].text
                    lastdealtime = translis[2].find_all('span')[1].text
                    house_param['lastdeal_date'] = lastdealtime if re.match(r'\d{4}-\d{2}-\d{2}', lastdealtime) else '0000-00-00'
                    house_param['use_type'] = translis[3].find_all('span')[1].text
                    house_param['yearlimit'] = translis[4].find_all('span')[1].text

                    tagsinfo = soup.find('div', class_='tags')
                    house_param['tag'] = '' if tagsinfo is None else tagsinfo.find_all('div')[1].text

                    buildyear = soup.find('div', class_='houseInfo').find('div', class_='area').find('div',
                                                                                                     class_='subInfo').text
                    buildyear = re.sub(r"\D", "", buildyear)
                    house_param['build_year'] = buildyear if re.match(r'\d{4}', buildyear) else 0
                    house_param['district'] = soup.find('div', class_='areaName').find('a').text

                    roominfo = soup.find('div', attrs={'id': 'infoList'})
                    roomlis = [] if roominfo is None else roominfo.find_all('div', class_='row')

                    if house_param['inside_area'] == 0:  # 修正部分数据没有套内面积的情况
                        insideArea = 0
                        for roomli in roomlis:
                            rlist = roomli.find_all('div')
                            if rlist is None:
                                log.info('rlist is none,::: ' + houseUrl)
                                break
                            insideArea += decimal.Decimal(re.sub(r"[^\d\.]", "", rlist[1].text))
                        house_param['inside_area'] = insideArea

                    self.write_house(house_param)

                    for roomli in roomlis:
                        room_param = {}
                        room_param['id'] = house_param['id']
                        rlist = roomli.find_all('div')
                        if rlist is None:
                            log.info('rlist is none,' + houseUrl)
                            break
                        room_param['title'] = rlist[0].text
                        room_param['area'] = re.sub(r"[^\d\.]", "", rlist[1].text)
                        room_param['direction'] = rlist[2].text
                        room_param['window'] = rlist[3].text
                        self.write_room(room_param)
                except Exception as e:
                    log.error('###########{0}  {1}\n{2}'.format(house_param['title'], houseUrl, e))
                    # raise e

            endTime = time.time()
            shortestWaitTime = 12
            if endTime - startTime < shortestWaitTime:
                time.sleep(int(shortestWaitTime - (endTime - startTime)))

        log.info(pageUrl + "总条数：" + str(cnt))

    def dispose(self):
        self._conn.dispose()
