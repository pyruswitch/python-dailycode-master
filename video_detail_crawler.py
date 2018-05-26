# -*- coding: utf-8 -*-
__author__ = 'Sean Lei&wuhan'

from base_crawler import BaseCrawler
from pyquery import PyQuery as Pq
from DAO import Dao


class VideoDetailCrawler(BaseCrawler):
    def __init__(self, seed_url,phone):
        self._seed_url = seed_url


    def _visit_pages(self):
        """
        @override
        in this class ,only one page
        """
        html = self.get_page_content_str(self._seed_url)
        self._extract_data(html)

    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        #name
        self.__ne_detail["name"] = doc('.mainTitle >h1').text()
        #area
        for li in doc('.newinfo >ul> li'):
            if(doc(li).find(".z").text()=="详细地址："):
                str = doc(li).text()
                str = str.replace("详细地址： ","").replace("&nbsp","").replace("-","").replace("  "," ").replace(" ",",")
                self.__ne_detail["location"] = str
            if(doc(li).find(".z").text()=="服务区域："):
                str = doc(li).text()
                str = str.replace("服务区域： ","").replace("&nbsp","").replace("-","").replace("  "," ").replace(" ",",")
                self.__ne_detail["area_name"] = str
        self.__ne_detail["description"] = doc('.description_con >span').text()
        print(self.__ne_detail)
        self._video_dao()

    def _insert_merchant(self):
        return "INSERT INTO merchant (city_id,name,phone,area_name,location,description,url )" \
               " VALUES ('{}','{}','{}','{}','{}','{}','{}' )".format(self.__ne_detail["city_id"],self.__ne_detail["name"],self.__ne_detail["phone"],self.__ne_detail["area_name"],
                                                                      self.__ne_detail["location"],self.__ne_detail["description"],self.__ne_detail["url"])

    def _video_dao(self):
        dao = Dao()
        #表中是否已有记录
        query_sql = "SELECT * FROM merchant WHERE url = '{}'".format(self.__ne_detail["url"])
        if dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self.__ne_detail["name"]))
            return
        #数据插入操作
        dao.execute_dmls(self._insert_merchant())


if __name__ == '__main__':
    v1 = VideoDetailCrawler("http://sz.58.com/songshui/19085255448200x.shtml",'13425149535')
    v1.craw()