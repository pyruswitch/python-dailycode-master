# -*- coding: utf-8 -*-
__author__ = 'Sean Lei'

import urllib
from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time


class CommunitiesListCrawler(BaseCrawler):
    global Dao
    Dao = Dao()

    def __init__(self):
        # TODO 用参数化和多线程来执行抓取

        super().__init__()
        self.detail_info_urls = []
        self.source_id = 28
        self._base_url = "http://newhouse.cnnbfdc.com/GetHouseTable.aspx"
        self._apartment_detail = {
            'COMMUNITY_ID': 0,
            'BUILDING_NUM': '',
            'APARTMENT_NUM': '',
            'STATUS': '2',
            'create_time': ''
        }

    def _visit_pages(self, seed_url, apartment_detail):
        """
        visit one url,get page content
        """

        # 单个url
        # html = self.get_page_content_str(self._seed_url[0]) #用数据库的时候
        endurl = seed_url[seed_url.index("?"):seed_url.index("&projectid")]
        seed_url = self._base_url + endurl
        html = self.get_page_content_str(seed_url)  # 单个URL
        self._extract_data(html, apartment_detail)
        # b = set(self._resualt)
        # self._resualt=[i for  i in b]
        # # dao=Dao()
        # insert_sql=""
        # for res1 in b :
        # insert_sql = "INSERT INTO merchant_tmp (description,url )VALUES ( '{}', 'http://www.youlin.me/category/407')".format(res1)
        # print( insert_sql  )
        # dao = Dao()
        # dao.execute_dmls(insert_sql)

    def _generate_seed_url(self):
        """
        generate all url to visit
        """
        # self._seed_url = "http://www.njhouse.com.cn/spf/inf/index.php?prjid=108510"
        # self._visit_pages(self._seed_url)
        # from page 1 to anypage which < 200

        # # 从数据库添加
        # self._seed_url = Dao._get_url_by_id(self.source_id)

        querysql = "SELECT  COMMUNITY_ID, BUILDING_NUM, URL  FROM ehdc.buildings WHERE STATUS = 0  ; "
        result = Dao.execute_query(querysql)
        for COMMUNITY_ID, BUILDING_NUM, URL in result:
            self.execute(COMMUNITY_ID, BUILDING_NUM, URL)

    def execute(self, COMMUNITY_ID, BUILDING_NUM, URL):
        try:
            apartment_detail = {
                'COMMUNITY_ID': 0,
                'BUILDING_NUM': '',
                'APARTMENT_NUM': '',
                'STATUS': '2',
                'create_time': ''
            }
            apartment_detail["COMMUNITY_ID"] = int(COMMUNITY_ID)
            apartment_detail["BUILDING_NUM"] = BUILDING_NUM
            apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self._visit_pages(URL, apartment_detail)
            sql = "update BUILDINGS set status = '2' where URL = '{}' ; ".format(URL)
            Dao.execute_dmls(sql)
        except Exception as  e:
            print(e)
            sql = "update BUILDINGS set status = -1 where URL = '{}' ; ".format(URL)
            Dao.execute_dmls(sql)

    def findEachBuilding(self, html):
        doc = Pq(html)
        a_list = doc("a.e_huangse")
        for a in a_list:
            self._apartment_detail["BUILDING_NUM"] = doc(a).text()
            href = doc(a).attr("onclick")
            href = href[href.index("'") + 1:]
            href = href[:href.index("'")]
            url = self._base_url + href
            # doc_str = self.get_page_content_str(url)
            # elf._extract_data(doc_str)
            # time.sleep(1)
            self.save_building(url)


    def _extract_data(self, doc_str, apartment_detail):
        try:
            doc = Pq(doc_str)
            a_list = doc("table>tr>td>table>tr>td")
            # total_item =int( doc("").text().strip())
            # count_num = int(total_item) / 12
            for a in a_list:
                apartment_detail["APARTMENT_NUM"] = doc(a).text()
                if apartment_detail["APARTMENT_NUM"].strip() != '':
                    apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                    time.localtime(time.time()))
                    self._save_community(apartment_detail)
        except Exception  as err:
            print(err)
            time.sleep(1)
            self._extract_data(doc_str)

    def _insert_apartment(self, apartment_detail):
        result = "INSERT INTO  apartments (COMMUNITY_ID , BUILDING_NUM , APARTMENT_NUM ,STATUS ,create_time  )" \
                 " VALUES ('{}','{}','{}','{}','{}'  )".format(apartment_detail["COMMUNITY_ID"],
                                                               apartment_detail["BUILDING_NUM"],
                                                               apartment_detail["APARTMENT_NUM"],
                                                               apartment_detail["STATUS"],
                                                               apartment_detail["create_time"])
        return result

    def _save_community(self, apartment_detail):
        # 表中是否已有记录
        query_sql = "SELECT * FROM apartments WHERE COMMUNITY_ID  = {}  and BUILDING_NUM ='{}'  and APARTMENT_NUM ='{}' ".format(
            int(apartment_detail["COMMUNITY_ID"]), apartment_detail["BUILDING_NUM"],
            apartment_detail["APARTMENT_NUM"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(str(apartment_detail["COMMUNITY_ID"]) +
                                                          apartment_detail["BUILDING_NUM"] +
                                                          apartment_detail["APARTMENT_NUM"]))
            return
        # 数据插入操作
        try:
            Dao.execute_dmls(self._insert_apartment(apartment_detail))
        except Exception as e:
            print(e)

    def craw(self):
        self._generate_seed_url()

    def save_building(self, url):
        SQL = " INSERT INTO ehdc.buildings (COMMUNITY_ID,BUILDING_NUM,URL,STATUS) VALUES ('{}','{}','{}','{}') ;".format(
            str(self._apartment_detail["COMMUNITY_ID"]), self._apartment_detail["BUILDING_NUM"], url,
            self._apartment_detail["STATUS"])
        Dao.execute_dmls(SQL)

