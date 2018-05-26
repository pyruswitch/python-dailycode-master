# -*- coding: utf-8 -*-
__author__ = 'Sean Lei'

from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time


class VideoListCrawler(BaseCrawler):
    def __init__(self):
        # TODO 用参数化和多线程来执行抓取
        super().__init__()
        self.detail_info_urls = []
        self.source_id = 98

    def _generate_seed_url(self):
        """
        generate all url to visit
        """
        # 从数据库添加
        # from page 1 to anypage which < 200
        global Dao
        Dao = Dao()
        self._seed_url = Dao._get_url_by_id(self.source_id)

        # 从网页添加
        # html = self.get_page_content_str(self._base_url)
        # doc = Pq(html)
        # alist = doc(".navi>ul>li>a")
        # for a in alist:
        #     self._seed_url.append(self._base_url + Pq(a).attr("href"))

        # 直接加，测试
        # self._seed_url.append("http://www.xzqy.net/./110000000000.htm")
        # 按照规则添加
        # for i in range(1,183):
        #     url = "http://www.youlin.me/home/explore/sort_type-new__category-407__day-0__page-" + str(i)
        #     self._seed_url.append(url)
        #     print(self._seed_url)

    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        self._comcode_detail["province"] = doc('.content>ul>li>h1').text()
        doc = Pq(doc_str)
        tr_list = doc('.content>table>tr')

        for tr in tr_list:
            try:
                # time.sleep(1)
                td_list = doc(tr).find("td")
                self._comcode_detail["city"] = doc(td_list[0]).find("a").text()
                a_list = doc(td_list[1]).find("a")
                for a in a_list:
                    self._comcode_detail["area"] = doc(a).text()
                    url = self._base_url + doc(a).attr("href")
                    # html = self.get_page_content_str(url)
                    # self._extract_data2(html)
                    insert_sql = " INSERT INTO fetch_list2 (source_id, url,times,page,STATUS) VALUE(98,'{}',0,0,0)".format(
                        url)
                    print("insert sql is [" + insert_sql)
                    Dao.execute_dmls(insert_sql)
            except IndexError as er:
                print("error in " + doc(tr).text())

                # self._comcode_detail["city"] = doc(tr).find(".parent").text()
                # # class ="tdiv" 的标签内的<a>标签的 href属性
                # herf = doc(tr).find(".tdiv > a").attr("href")
                # print(phone)
                # print(herf)
                # crawler = DetailCrawler(herf, phone)
                # crawler.craw()
                # print(self._resualt)

    def _extract_data2(self, doc_str):
        doc = Pq(doc_str)
        a_list = doc(".place>ul>li>a")
        try:
            self._comcode_detail["province"] = doc(a_list[1]).text()
            self._comcode_detail["city"] = doc(a_list[2]).text()
        except IndexError as er:
            sql =  "   UPDATE  fetch_list2 SET  times = 0  WHERE url = '{}'".format(self._now_url)
            Dao.execute_dmls(sql)
        doc = Pq(doc_str)
        self._comcode_detail["area"] = doc('.content>ul>li>h1').text()
        doc = Pq(doc_str)
        tr_list = doc('.content>table>tr')
        for tr in tr_list:
            try:
                # time.sleep(1)
                td_list = doc(tr).find("td")
                self._comcode_detail["street"] = doc(td_list[0]).find("a").text()
                a_list = doc(td_list[1]).find("a")
                for a in a_list:
                    self._comcode_detail["society_community"] = doc(a).text()
                    self._save_comcode()

            except IndexError as er:
                print("error in " + doc(tr).text())

    def _save_comcode(self):
        inser_sql = "INSERT INTO comcode (province ,city,area,street,society_community  )" \
                    " VALUES ('{}','{}','{}','{}','{}'  )".format(self._comcode_detail["province"],
                                                                  self._comcode_detail["city"],
                                                                  self._comcode_detail["area"],
                                                                  self._comcode_detail["street"],
                                                                  self._comcode_detail["society_community"])
        Dao.execute_dmls(inser_sql)