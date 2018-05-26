# -*- coding: utf-8 -*-
__author__ = 'wuhan'

from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
import urllib
import copy
import time


class CategoryListCrawler(BaseCrawler):
    global Dao
    Dao = Dao()

    def __init__(self):
        super().__init__()
        self.detail_info_urls = []
        self.source_id = 17
        self._base_url = "http://www.dianping.com/wuhan"
        self._category_detail = {
            'shopType': '',
            'categoryId': '',
            'name': ''
        }
        self._category_list = []

    def get_page_content_str(self, url):
        print("现在开始抓取" + url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        request = urllib.request.Request(url=url, headers=headers)
        m_fp = urllib.request.urlopen(request, timeout=500)
        html_str = m_fp.read().decode('utf-8')
        m_fp.close()
        return html_str

    def _visit_pages(self, seed_url):
        """
        visit one url,get page content
        """
        # 单个url
        html = self.get_page_content_str(self._seed_url[0])
        self._extract_data(html)


    def _generate_seed_url(self):
        """
        generate all url to visit
        """
        # 直接加，测试
        self._seed_url.append(self._base_url)


    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        li_list = doc('.aside.aside-left>.category-nav.J-category-nav>li')
        for li in li_list:
            self._category_detail["shopType"] = doc(li).attr("data-key")
            self._category_detail["categoryId"] = self._category_detail["shopType"]
            self._category_detail["name"] = doc(li).find(".name>span").text()
            self._category_list.append(copy.copy(self._category_detail))
            # doc2   = Pq(doc_str)
            # div_list = doc2(".aside.aside-left>.category-nav.J-category-nav>li>.secondary-category.J-secondary-category>div>div")
            a_list = doc(li).find("div>a")
            for a in a_list:
                self._category_detail["categoryId"] = doc(a).attr("data-key")
                self._category_detail["name"] = doc(a).text()
                self._category_list.append(copy.copy(self._category_detail))

        self.save_category()


    def craw(self):
        self._generate_seed_url()
        self._visit_pages(self._seed_url)
        print(self._seed_url)


    def save_category(self):
        for category in self._category_list:
            sql = "INSERT INTO category (shopType,categoryId,name )  VALUES ('{}','{}','{}' )".format(category["shopType"],
                                                                                                      category[
                                                                                                          "categoryId"],
                                                                                                      category["name"])
            Dao.execute_dmls(sql)
