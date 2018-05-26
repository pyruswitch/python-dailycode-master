# -*- coding: utf-8 -*-
__author__ = 'wuhan'

from pyquery import PyQuery as Pq
from DAO import Dao
import mysql.connector
from base_crawler import BaseCrawler
import time
import DAO
import urllib
import json
from dianping_shop_update_latlong import GoogleLatALng2Baidu
import threading
import time


class DianpingMerchantCrawler(threading.Thread):
    def __init__(self, LT1, LG1, LT2, LG2, cityname, cityid, cityenname, name, shopId=0, categoryId=0):
        threading.Thread.__init__(self, name=name)
        self.cityid = cityid
        self.shopId = shopId
        self.categoryId = categoryId
        self.Lat1 = LT1
        self.Lat2 = LT2
        self.Long1 = LG1
        self.Long2 = LG2
        self.city_name = cityname
        self.values = {
            'promoId': '0',
            'shopType': '',
            'categoryId': '',
            'sortMode': '2',
            'shopSortItem': '1',
            'keyword': '',
            'searchType': '1',
            'branchGroupId': '0',
            'shippingTypeFilterValue': '0',
            'page': '1'}
        self.values["cityId"] = cityid
        self.values["cityEnName"] = cityenname
        self.url = "http://www.dianping.com/search/map/ajax/json"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                        'Referer': 'http://www.dianping.com/search/map/category/{}/0'.format(cityid)}
        self.dao = Dao()
        self.query_sql = "SELECT shopType ,categoryId,NAME FROM category  WHERE categoryId <> shopType AND categoryId <>'None'  "
        self.result = self.dao.execute_query(self.query_sql)
        self.query_sql2 = "SELECT shopId FROM shop_bean where  city_name ='{}'".format(cityname)
        self.result2 = self.dao.execute_query(self.query_sql2)
        self.shopIds = []
        if self.result2 is not None:
            for shopid in self.result2:
                self.shopIds.append(shopid[0])

    def save_shop(self, shopRecordBean, categoryId):
        zuobiao = GoogleLatALng2Baidu(
            shopRecordBean["geoLng"],
            shopRecordBean["geoLat"])
        insert_sql = "insert into shop_bean (address ,poi ,phoneNo ,shopId ,defaultPic,expand ,shopName,geoLat ,shopDealId,geoLng ,addDate ,shopPower ,shopPowerTitle ,avgPrice,memberCardId ," \
                     "bookingSetting ,dishTag ,branchUrl ,promoId ,hasSceneryOrder ,shopRecordBean ,regionList ,categoryId ,LATITUDE , LONGITUDE,city_name ) " \
                     "values( '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\"{}\",'{}','{}',{},{},'{}')".format(
            shopRecordBean["address"],
            shopRecordBean["poi"],
            shopRecordBean["phoneNo"],
            shopRecordBean["shopId"],
            shopRecordBean["defaultPic"],
            shopRecordBean["expand"],
            shopRecordBean["shopName"],
            shopRecordBean["geoLat"],
            shopRecordBean["shopDealId"],
            shopRecordBean["geoLng"],
            shopRecordBean["addDate"],
            shopRecordBean["shopPower"],
            shopRecordBean["shopPowerTitle"],
            shopRecordBean["avgPrice"],
            shopRecordBean["memberCardId"],
            shopRecordBean["bookingSetting"],
            shopRecordBean["dishTag"],
            shopRecordBean["branchUrl"],
            shopRecordBean["promoId"],
            shopRecordBean["hasSceneryOrder"],
            str(shopRecordBean["shopRecordBean"]).replace('\'', '\\\'').replace('\"', '\\\"'),
            shopRecordBean["regionList"],
            categoryId,
            zuobiao["LATITUDE"],
            zuobiao["LONGITUDE"], self.city_name)
        self.dao.execute_dmls(insert_sql)

    def savePageJson(self, page=1):
        try:
            self.values["page"] = page
            print(self.values, "begin")
            self.data = urllib.parse.urlencode(self.values).encode(encoding='UTF8')
            request = urllib.request.Request(url=self.url, headers=self.headers, data=self.data)
            m_fp = urllib.request.urlopen(request, timeout=500)
            html_str = m_fp.read().decode('utf-8')
            m_fp.close()
            # print(self.url,self.headers,self.data,html_str)
            s = json.loads(html_str)

            shopRecordBeanList = s["shopRecordBeanList"]
            # 去除重复的商家
            for shopRecordBean in shopRecordBeanList:
                if str(shopRecordBean["shopId"]) not in self.shopIds:
                    self.save_shop(shopRecordBean, self.values["categoryId"])
                    self.shopIds.append(str(shopRecordBean["shopId"]))
            # print("商家之一")
            # for key in shopRecordBean:
            # print("  {} = {}".format(key, shopRecordBean[key]))
            # for key in shopRecordBeanList[0]:
            # print("  {} = {}".format(key, shopRecordBeanList[0][key]))
            return s
        except Exception as e:
            print(e)
            return self.savePageJson(page)
            # except mysql.connector.Error as e :
            # print(e)

    def crawler_each_category(self, result):
        for shopType, categoryId, NAME in result:
            # print("shoptype = {} , categoryid = {} ,name = {}  begin ".format(shopType, categoryId, NAME))
            self.values["shopType"] = shopType
            self.values["categoryId"] = categoryId
            s = self.savePageJson(1)
            pageCount = s["pageCount"]
            for page in range(2, pageCount + 1):
                try:
                    self.savePageJson(page)
                except Exception as e:
                    print(e)
                    time.sleep(0.5)
                    self.savePageJson(page)

    def crawler_each_category_withzuobiao(self, result, Lat, Long):
        self.values["glat1"] = Lat
        self.values["glong1"] = Long
        self.values["glat2"] = Lat - 0.1
        self.values["glong2"] = Long + 0.2
        self.crawler_each_category(result)

    def run(self):
        if self.Lat1 == 0:
            if self.shopId == 0:
                self.crawler_each_category(self.result)
            elif self.categoryId == 0:
                result = [self.shopId, self.shopId,
                          ""]
                results = []
                results.append(result)
                self.crawler_each_category(results)
            else:
                result = [self.shopId, self.categoryId,
                          ""]
                results = []
                results.append(result)
                self.crawler_each_category(results)
        else:
            Lat = self.Lat1
            while (Lat >= self.Lat2):
                Long = self.Long1
                while (Long <= self.Long2):
                    self.crawler_each_category_withzuobiao(self.result, Lat, Long)
                    Long += 0.19
                Lat = Lat - 0.09
                # crawler_each_category(result)
        update_sql = "update dianping_cities set status = 0 where cityId = {} ".format(self.cityid)

    def stop(self):
        self.thread_stop = True


if __name__ == '__main__':
    thread1 = DianpingMerchantCrawler(0, 0, 0, 0, '苏州 ', '6', 'suzhou', '苏州线程')
    # thread1 = DianpingMerchantCrawler(39.15128409557495, 116.99860100341789, 39.019905173955294, 117.49676231933586, '天津', '10', 'tianjin','线程天津')
    querysql = " SELECT cityId ,cityenname ,cityname FROM dianping_cities WHERE cityname IS NOT NULL  and status = 2   "
    dao = DAO.Dao()
    results = dao.execute_query(querysql)
    threads = []
    files = range(len(results))
    for cityId, cityenname, cityname in results:
        thread = DianpingMerchantCrawler(0, 0, 0, 0, cityname, cityId, cityenname, cityname)
        threads.append(thread)
    for i in files:
        threads[i].start()

    for i in files:
        threads[i].join()

    print("end in ", time.ctime())