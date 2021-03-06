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

    def __init__(self):
        # TODO 用参数化和多线程来执行抓取

        super().__init__()
        self.detail_info_urls = []
        self.source_id = 17
        self._base_url = "http://sz.ganji.com/"
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

        for single_url in seed_url:
            update_sql = "   UPDATE  fetch_list SET  times = times+1 WHERE url = '{}'and source_id =17".format(
                single_url[0])
            Dao.execute_dmls(update_sql)
            self._base_url = single_url[0]
            self._now_url = single_url[0]
            html = self.get_page_content_str(single_url[0])
            try:
                self._extract_data(html)
            except Exception as e:
                print(e)
                update_sql = "   UPDATE  fetch_list SET  status  = 1 WHERE url = '{}'and source_id =17".format(
                    single_url[0])
                Dao.execute_dmls(update_sql)

                # 单个url
                # html = self.get_page_content_str(self._seed_url[0])
                # self._extract_data(html)
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

        # 从数据库添加
        self._seed_url = Dao._get_url_by_id(self.source_id)

        # 直接加，测试
        # self._seed_url.append("http://www.anjuke.com/index.html")




    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        total_item = doc(".PL_1.clearfix>span>em").text()
        count_num = int(total_item) / 10
        for page in range(1, int(count_num) + 1):
            url = self._base_url + "W0QQpZ" + str(page)
            html = self.get_page_content_str(url)
            self._extract_data2(html)

    def _extract_data2(self, doc_str):
        doc = Pq(doc_str)
        li_list = doc(".mainListing.clearfix>.pL>.list>li")
        for li in li_list:
            self._community_detail["url"] = doc(li).find(".details>div>a").attr("href")
            self._community_detail["name"] = doc(li).find(".details>div>a").text()
            p = doc(li).find(".details>p")
            self._community_detail["location"] = doc(p[0]).text()
            self._community_detail["area_name"] = self._community_detail["location"][
                                                  self._community_detail["location"].index("[") + 1:
                                                  self._community_detail["location"].index("]")]
            self._community_detail["location"] = self._community_detail["location"][
                                                 self._community_detail["location"].index("]") + 1:]

            url = doc(li).find(".details>.p_links>a").attr("href")
            self._community_detail['latitude'] = url[url.index("l1=") + 3:url.index("&l2")]
            self._community_detail['longitude'] = url[url.index("l2=") + 3:url.index("&l3")]
            self._save_community()


    def _insert_community(self):
        result = "INSERT INTO  communities (ORIGINAL_URL,NAME,address,AREA_NAME,LATITUDE,LONGITUDE,source_id )" \
                 " VALUES ('{}','{}','{}','{}','{}','{}' ,'{}' )".format(self._community_detail["url"],
                                                                         self._community_detail["name"],
                                                                         self._community_detail["location"],
                                                                         self._community_detail["area_name"],
                                                                         self._community_detail["latitude"],
                                                                         self._community_detail["longitude"],
                                                                         self.source_id)
        return result

    def _save_community(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM communities WHERE ORIGINAL_URL = '{}'".format(self._community_detail["url"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self._community_detail["name"]))
            return
        # 数据插入操作
        Dao.execute_dmls(self._insert_community())
