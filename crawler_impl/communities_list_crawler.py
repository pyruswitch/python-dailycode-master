# -*- coding: utf-8 -*-
__author__ = 'Sean Lei'

from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time


class CommunitiesListCrawler(BaseCrawler):
    global Dao
    Dao = Dao()

    def craw(self):
        self._generate_seed_url()

    def __init__(self):
        # TODO 用参数化和多线程来执行抓取

        super().__init__()
        self.detail_info_urls = []
        self.source_id = 18
        self._base_url = "http://bj.5i5j.com"
        self._community_detail = {
            'url': '',
            'name': '',
            'location': '',
            'area_name': '',
            'description': '',
            'latitude': '',
            'longitude': '',
            'city': ''

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
        #     html = self.get_page_content_str(single_url[0])
        #     try:
        #         self._extract_data(html)
        #     except Exception as e:
        #         print(e)
        #         update_sql = "   UPDATE  fetch_list SET  status  = 1 WHERE url = '{}'and source_id =17".format(
        #             single_url[0])
        #         Dao.execute_dmls(update_sql)

        # 单个url
        html = self.get_page_content_str(seed_url)
        self.findEachArea(html)
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

        # from page 1 to anypage which < 200

        # # 从数据库添加
        # self._seed_url = Dao._get_url_by_id(self.source_id)

        # 直接加，测试
        self._visit_pages("http://www.llzg.cn/nhd/neig44000000.html")


    def findEachArea(self, HTML):
        doc = Pq(HTML)
        citys = doc("body > div > div.container > div > div > div.branchNavWrap")
        for city in citys:
            self._community_detail['city'] = doc(city).find("div.title3>h4").text()
            areas = doc(city).find("div.branchNav>a")
            for area in areas:
                self._community_detail['area_name'] = doc(area).text()
                url = doc(area).attr('href') + '/plot/plotlist'
                self._extract_data(url)

    def _extract_data(self, url):
        doc_str = self.get_page_content_str(url)

        doc = Pq(doc_str)
        communities = doc(
            "body > div.container.marginTop10px > div > div.span9 > div.areasWrap > div.areas > dl.clearfix > dd > a")
        for community in communities:
            self._community_detail['name'] = doc(community).text()
            self._save_community()

    def _insert_community(self):
        result = "INSERT INTO  ehdc.communities_llzg (ORIGINAL_URL,NAME,AREA_NAME,LATITUDE,LONGITUDE,city_name )" \
                 " VALUES ('{}','{}','{}','{}','{}' ,'{}' )".format(self._community_detail["url"],
                                                                    self._community_detail["name"],
                                                                    self._community_detail["area_name"],
                                                                    '',
                                                                    '',
                                                                    self._community_detail['city'])
        return result

    def _save_community(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM ehdc.communities_llzg WHERE NAME = '{}' and AREA_NAME='{}' ".format(
            self._community_detail["name"],
            self._community_detail["area_name"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self._community_detail["name"]))
            return
        # 数据插入操作
        Dao.execute_dmls(self._insert_community())


if __name__ == '__main__':
    craw = CommunitiesListCrawler()
    craw.craw()