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
        self._base_url = "http://newhouse.cnnbfdc.com/lpxx.aspx"
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
        self._extract_data(html)


    # def get_page_content_str(self, url):
    # time.sleep(1)
    #
    # try:
    # print("现在开始抓取" + url)
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    #         request = urllib.request.Request(url=url, headers=headers)
    #         m_fp = urllib.request.urlopen(request, timeout=5500)
    #         html_str_uncode = m_fp.read()
    #         m_fp.close()
    #         return html_str_uncode
    #     except urllib.error.URLError as err:
    #         # logfile = open('test.log', 'a')
    #         # logfile.write("Error: {} \n in  url : {}".format(err, url))
    #         # logfile.close()
    #         # print("error in {}.get_page_content_str".format(__name__))
    #         # if url[-3:] == "htm":
    #         # time.sleep(120)
    #         # return self.get_page_content_str(url)
    #         return None
    #     except Exception  as err:
    #         print(err)
    #         return None

    def _generate_seed_url(self):
        """
        generate all url to visit
        """

        # from page 1 to anypage which < 200

        # # 从数据库添加
        # self._seed_url = Dao._get_url_by_id(self.source_id)

        # 直接加，测试
        # self._visit_pages(self._base_url)
        # 实际操作，循环每一页
        for i in range(1, 70):
            visiturl = self._base_url + '?p=' + str(i)
            self._visit_pages(visiturl)


    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        tr_list = doc("td.sp_sck>table>tr")
        # total_item =int( doc("").text().strip())
        # count_num = int(total_item) / 12
        for tr in tr_list:
            try:
                doc = Pq(tr)
                # test =  doc(doc("tr")[1]).find("td")[1].text()
                self._community_detail['location'] = doc("td:eq(3)").text()
                self._community_detail['name'] = doc("a.sp_zi12c").text()
                self._community_detail['url'] = doc("a.sp_zi12c").attr("href")
                self._community_detail['area_name'] = doc("span.sp_f12").text()
                if (self._community_detail['name'] != ''):
                    self._save_community()
            except Exception  as err:
                print(tr)
                print(err)
                continue

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

    def _save_community(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM communities WHERE ORIGINAL_URL = '{}' and source_id ={} ".format(
            self._community_detail["url"], self.source_id)
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(self._community_detail["name"]))
            return
        # 数据插入操作
        Dao.execute_dmls(self._insert_community())

    def craw(self):
        self._generate_seed_url()