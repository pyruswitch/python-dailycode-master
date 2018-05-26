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
        self.source_id = 21
        self._base_url = "http://www.njhouse.com.cn/spf/inf/"
        self._root_url = "http://www.njhouse.com.cn/spf/inf/index.php"
        self._apartment_detail = {
            'COMMUNITY_ID': 0,
            'BUILDING_NUM': '',
            'APARTMENT_NUM': '',
            'STATUS': '2',
            'create_time': ''
        }

    def _visit_pages(self, seed_url):
        """
        visit one url,get page content
        """

        # for single_url in seed_url:
        # update_sql = "   UPDATE  fetch_list SET  times = times+1 WHERE url = '{}'and source_id =17".format(
        # single_url[0])
        # Dao.execute_dmls(update_sql)
        # self._base_url = single_url[0]
        # self._now_url = single_url[0]
        # html = self.get_page_content_str(single_url[0])
        #     try:
        #         self._extract_data(html)
        #     except Exception as e:
        #         print(e)
        #         update_sql = "   UPDATE  fetch_list SET  status  = 1 WHERE url = '{}'and source_id =17".format(
        #             single_url[0])
        #         Dao.execute_dmls(update_sql)

        # 单个url
        # html = self.get_page_content_str(self._seed_url[0]) #用数据库的时候
        seed_url = self._root_url + seed_url[seed_url.rindex("?"):]
        html = self.get_page_content_str(seed_url)  #单个URL
        self.findEachBuilding(html)
        # b = set(self._resualt)
        # self._resualt=[i for  i in b]
        # # dao=Dao()
        # insert_sql=""
        # for res1 in b :
        # insert_sql = "INSERT INTO merchant_tmp (description,url )VALUES ( '{}', 'http://www.youlin.me/category/407')".format(res1)
        # print( insert_sql  )
        # dao = Dao()
        # dao.execute_dmls(insert_sql)


    def get_page_content_str(self, url):


        try:
            print("现在开始抓取" + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            request = urllib.request.Request(url=url, headers=headers)
            m_fp = urllib.request.urlopen(request, timeout=1500)
            html_str_uncode = m_fp.read()
            if html_str_uncode == '':
                print("出问题了，没出来数据")
                return self.get_page_content_str(url)
            m_fp.close()
            return html_str_uncode
        except urllib.error.URLError as err:
            return None
        except Exception  as err:
            print(err)
            return None


    def _generate_seed_url(self):
        """
        generate all url to visit
        """
        # self._seed_url = "http://www.njhouse.com.cn/spf/inf/index.php?prjid=108510"
        # self._visit_pages(self._seed_url)
        # from page 1 to anypage which < 200

        # # 从数据库添加
        # self._seed_url = Dao._get_url_by_id(self.source_id)

        querysql = "SELECT COMMUNITY_ID,ORIGINAL_URL FROM communities WHERE   source_id ='{}' and status= -1 ; ".format(
            self.source_id)
        result = Dao.execute_query(querysql)
        for COMMUNITY_ID, ORIGINAL_URL in result:
            try:
                self._apartment_detail["COMMUNITY_ID"] = int(COMMUNITY_ID)
                self._apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                self._visit_pages(ORIGINAL_URL)
                sql = "update communities set status = '2' where COMMUNITY_ID = '{}' ".format(int(COMMUNITY_ID))
                Dao.execute_dmls(sql)
            except Exception as  e:
                print(e)
                sql = "update communities set status = '-1' where COMMUNITY_ID = '{}' ".format(int(COMMUNITY_ID))
                Dao.execute_dmls(sql)

                # 直接加，测试
                # self._seed_url.append(self._base_url)


    def findEachBuilding(self, html):
        doc = Pq(html)
        a_list = doc("table>tr>td.text>a")
        for a in a_list:
            self._apartment_detail["BUILDING_NUM"] = doc(a).text()
            url = self._base_url + doc(a).attr("href")
            doc_str = self.get_page_content_str(url)
            self._extract_data(doc_str)
            time.sleep(5)


    def _extract_data(self, doc_str):
        try:
            doc = Pq(doc_str)
            a_list = doc("tr.text>td>a")
            # total_item =int( doc("").text().strip())
            # count_num = int(total_item) / 12
            for a in a_list:
                self._apartment_detail["APARTMENT_NUM"] = doc(a).text()
                if self._apartment_detail["APARTMENT_NUM"].strip() != '':
                    self._apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                          time.localtime(time.time()))
                    self._save_community()
        except Exception  as err:
            print(err)
            time.sleep(100)
            self._extract_data(doc_str)

    def _insert_community(self):
        result = "INSERT INTO  apartments (COMMUNITY_ID , BUILDING_NUM , APARTMENT_NUM ,STATUS ,create_time  )" \
                 " VALUES ('{}','{}','{}','{}','{}'  )".format(self._apartment_detail["COMMUNITY_ID"],
                                                               self._apartment_detail["BUILDING_NUM"],
                                                               self._apartment_detail["APARTMENT_NUM"],
                                                               self._apartment_detail["STATUS"],
                                                               self._apartment_detail["create_time"])
        return result

    def _save_community(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM apartments WHERE COMMUNITY_ID  = {}  and BUILDING_NUM ='{}'  and APARTMENT_NUM ='{}' ".format(
            int(self._apartment_detail["COMMUNITY_ID"]), self._apartment_detail["BUILDING_NUM"],
            self._apartment_detail["APARTMENT_NUM"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(str(self._apartment_detail["COMMUNITY_ID"] )+
                                                          self._apartment_detail["BUILDING_NUM"] +
                                                          self._apartment_detail["APARTMENT_NUM"]))
            return
        # 数据插入操作
        try:
            Dao.execute_dmls(self._insert_community())
        except Exception as e:
            print(e)

    def craw(self):
        self._generate_seed_url()

