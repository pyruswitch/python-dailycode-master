# -*- coding: utf-8 -*-
__author__ = 'Sean Lei'

from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time


class GanjiListCrawler(BaseCrawler):
    def __init__(self):
        # TODO 用参数化和多线程来执行抓取
        super().__init__()
        self.detail_info_urls = []
        self.source_id = 16
        self._base_url = "http://sz.ganji.com/"
        self._merchant_detail = {
            'city_id': '5636851',
            'name': '',
            'location': '',
            'area_name': '',
            'description': '',
            'phone': '',
            'source_id': self.source_id,
            'service': '',
            'url': ''

        }

    def _visit_pages(self, seed_url):
        """
        visit one url,get page content
        """

        for single_url in seed_url:
            update_sql = "   UPDATE  fetch_list SET  times = times+1 WHERE url = '{}'and source_id = 16".format(
                single_url[0])
            Dao.execute_dmls(update_sql)
            self._now_url = single_url[0]
            html = self.get_page_content_str(single_url[0])
            self._extract_data(html)


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
        global Dao
        Dao = Dao()
        self._seed_url = Dao._get_url_by_id(self.source_id)

        # 直接加，测试
        # self._seed_url.append("http://sz.ganji.com/jiadianweixiu/o1")


    def find_url_from_ul(self, ul):
        """
        对每一个ul 进行解析
        """
        doc = Pq(ul)
        li_list = doc("li")
        for li in li_list:
            url = self._base_url + doc(li).find("div>p>a").attr("href")
            if url in self.detail_info_urls:
                continue
            else:
                self._merchant_detail["url"] = url
                self.detail_info_urls.append(url)
                html = self.get_page_content_str(url)
                self._extract_data2(html)


    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        ul_list = doc('.leftBox>.list>ul')

        for ul in ul_list:
            self.find_url_from_ul(ul)


    def _extract_data2(self, doc_str):
        doc = Pq(doc_str)
        self._merchant_detail["name"] = doc(".d-top-head.clearfix>.txt>h1").text().replace("&nbsp", "").replace("-",
                                                                                                                "").replace(
            "  ", " ")
        doc = Pq(doc_str)
        self._merchant_detail["description"] = "".join(doc(".d-left-box>.service-about>.con>.txt").text())
        doc = Pq(doc_str)
        ul = doc(".d-top-info>ul")
        self._merchant_detail["phone"] = doc(ul).find(".tel-num.clearfix>.tcon.pos-r>.tel.phone").text().replace(
            "&nbsp",
            "").replace(
            "-", "").replace("  ", " ").replace(" ", ",")
        self._merchant_detail["location"] = doc(ul).find(".clearfix>.tcon>.fl").text().replace("&nbsp", "").replace("-",
                                                                                                                    "").replace(
            "  ", " ").replace(" ", ",")
        self._merchant_detail["service"] = doc(ul).find(".clearfix.service>.tcon>.mr10").text().replace("&nbsp",
                                                                                                        "").replace("-",
                                                                                                                    "").replace(
            "  ", " ").replace(" ", ",")
        # self._merchant_detail["location"]=",".join(doc(ul).find(".clearfix>.tcon>.fl").text().replace("&nbsp","").replace("-","").replace("  "," ").replace(" ",","))
        # self._merchant_detail["service"]=",".join(doc(ul).find(".clearfix.service>.tcon>.mr10").text().replace("&nbsp","").replace("-","").replace("  "," ").replace(" ",","))
        # print(self._merchant_detail)
        self._save_merchant()


    def _insert_merchant(self):
        return "INSERT INTO merchant (city_id,name,phone,area_name,location,description,url,source_id,service )" \
               " VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}' )".format(self._merchant_detail["city_id"],
                                                                                self._merchant_detail["name"],
                                                                                self._merchant_detail["phone"],
                                                                                self._merchant_detail["area_name"],
                                                                                self._merchant_detail["location"],
                                                                                self._merchant_detail["description"],
                                                                                self._merchant_detail["url"],
                                                                                self._merchant_detail["source_id"],
                                                                                self._merchant_detail["service"])


    def _save_merchant(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM merchant WHERE url = '{}'".format(self._merchant_detail["url"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self._merchant_detail["name"]))
            return
        # 数据插入操作
        Dao.execute_dmls(self._insert_merchant())
