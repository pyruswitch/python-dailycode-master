# coding=utf-8
__author__ = 'wuhan'

import urllib
from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time
import threading


class CommunitiesListCrawler(BaseCrawler, threading.Thread):
    global Dao
    Dao = Dao()

    def __init__(self, page_num):
        # TO
        threading.Thread.__init__(self, name=page_num)
        super().__init__(self)
        self.detail_info_urls = []
        self.source_id = 30
        self.min_page = page_num * 30 + 1
        self.max_page = page_num * 30 + 31
        self._base_url = "http://newhouse.hfhome.cn/"
        self._community_detail = {
            'url': '',
            'name': '',
            'location': '',
            'area_name': '',
            'description': '',
            'latitude': '',
            'longitude': ''
        }

    def _visit_pages(self, seed_url):
        """
        visit one url,get page content
        """
        # 单个url
        html = self.get_page_content_str(seed_url)
        self.findEachBuilding(html)


    def findEachBuilding(self, html):
        doc = Pq(html)
        tr_list = doc("table#GVFwxkz>tr")
        for tr in tr_list:
            name = Pq(tr)("td:eq(1)").text()
            self._community_detail["name"] = name
            href = doc(tr).find("td>a").attr("href")
            if href == None:
                continue
            href = href[href.index("?"):]
            url = "http://newhouse.hfhome.cn/Modal/RoomList.aspx" + href
            if self._check_community(url):
                print(url + "     ---    已经爬取过了")
                continue
            self._community_detail["url"] = url
            self._extract_data(url)

    def _extract_data(self, url):
        community_id = self._save_community()
        doc_str = self.get_page_content_str(url)
        doc = Pq(doc_str)
        tr_list = doc("table>tr")
        try:
            for tr in tr_list:
                Floor_num = Pq(tr)("td:eq(0)").text()
                a_list = doc(tr).find("td.preview>a")
                for a in a_list:
                    apartment_detail = {
                        'COMMUNITY_ID': community_id,
                        'FLOOR_NUM': Floor_num,
                        'APARTMENT_NUM': doc(a).text(),
                        'STATUS': '2',
                        'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    }
                    self._save_apartment(apartment_detail)
            sql = "update communities set status = '2' where ORIGINAL_URL = '{}' ; ".format(url)
            Dao.execute_dmls(sql)
        except Exception as  e:
            print(e)
            sql = "update communities set status = -1 where ORIGINAL_URL = '{}' ; ".format(url)
            Dao.execute_dmls(sql)

    def _insert_community(self):
        result = "INSERT INTO  communities (ORIGINAL_URL,NAME,AREA_NAME,LATITUDE,LONGITUDE,address,source_id )" \
                 " VALUES ('{}','{}','{}','{}','{}' ,'{}','{}' )".format(self._community_detail["url"],
                                                                         self._community_detail["name"],
                                                                         self._community_detail["area_name"],
                                                                         self._community_detail["latitude"],
                                                                         self._community_detail["longitude"],
                                                                         self._community_detail["location"],
                                                                         self.source_id)
        return result


    def _insert_apartment(self, apartment_detail):
        result = "INSERT INTO  apartments (COMMUNITY_ID  , APARTMENT_NUM ,STATUS ,FLOOR_NUM,create_time  )" \
                 " VALUES ('{}','{}','{}','{}','{}'  )".format(apartment_detail["COMMUNITY_ID"],
                                                               apartment_detail["APARTMENT_NUM"],
                                                               apartment_detail["STATUS"],
                                                               apartment_detail["FLOOR_NUM"],
                                                               apartment_detail["create_time"])
        return result


    def _save_apartment(self, apartment_detail):
        # 表中是否已有记录
        query_sql = "SELECT * FROM apartments WHERE COMMUNITY_ID  = {}  and FLOOR_NUM ='{}'  and APARTMENT_NUM ='{}' ".format(
            int(apartment_detail["COMMUNITY_ID"]), apartment_detail["FLOOR_NUM"],
            apartment_detail["APARTMENT_NUM"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(str(apartment_detail["COMMUNITY_ID"]) +
                                                          apartment_detail["FLOOR_NUM"] +
                                                          apartment_detail["APARTMENT_NUM"]))
            return
        # 数据插入操作
        try:
            Dao.execute_dmls(self._insert_apartment(apartment_detail))
        except Exception as e:
            print(e)


    def _save_community(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM communities WHERE ORIGINAL_URL = '{}' and source_id ={} ".format(
            self._community_detail["url"], self.source_id)
        communityid_sql = "SELECT COMMUNITY_ID FROM communities WHERE ORIGINAL_URL = '{}' and source_id ={} ".format(
            self._community_detail["url"], self.source_id)
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self._community_detail["name"]))
            return Dao.execute_query(communityid_sql)[0][0]
        # 数据插入操作
        Dao.execute_dmls(self._insert_community())
        return Dao.execute_query(communityid_sql)[0][0]

    def _check_community(self, url):
        # 表中是否已有记录 完成的
        communityid_sql = "SELECT COMMUNITY_ID FROM communities WHERE ORIGINAL_URL = '{}' and source_id ={} and status = 2 ".format(
            url, self.source_id)
        result = Dao.execute_query(communityid_sql)
        if result == None:
            return False
        return True


    def run(self):
        # for i in range(self.min_page, self.max_page):
        for i in range(363, 397):
            url = "http://newhouse.hfhome.cn/hffd_xkz.aspx?page={}".format(i)
            self._visit_pages(url)
