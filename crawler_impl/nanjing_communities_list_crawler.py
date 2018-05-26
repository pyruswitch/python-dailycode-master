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
        self._base_url = "http://www.njhouse.com.cn/persalereg.php"
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

        # for single_url in seed_url:
        #     update_sql = "   UPDATE  fetch_list SET  times = times+1 WHERE url = '{}'and source_id =17".format(
        #         single_url[0])
        #     Dao.execute_dmls(update_sql)
        #     self._base_url = single_url[0]
        #     self._now_url = single_url[0]
        #     html = self.get_page_content_str(single_url[0])
        #     try:
        #         self._extract_data(html)
        #     except Exception as e:
        #         print(e)
        #         update_sql = "   UPDATE  fetch_list SET  status  = 1 WHERE url = '{}'and source_id =17".format(
        #             single_url[0])
        #         Dao.execute_dmls(update_sql)

        # 单个url
        html = self.get_page_content_str(self._seed_url[0])
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


    def get_page_content_str(self, url):
        time.sleep(1)

        try:
            print("现在开始抓取" + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            request = urllib.request.Request(url=url, headers=headers)
            m_fp = urllib.request.urlopen(request, timeout=5500)
            html_str_uncode=m_fp.read()
            m_fp.close()
            return html_str_uncode
        except urllib.error.URLError as err:
            # logfile = open('test.log', 'a')
            # logfile.write("Error: {} \n in  url : {}".format(err, url))
            # logfile.close()
            # print("error in {}.get_page_content_str".format(__name__))
            # if url[-3:] == "htm":
            # time.sleep(120)
            #     return self.get_page_content_str(url)
            return None
        except Exception  as err:
            print(err)
            return None

    def _generate_seed_url(self):
        """
        generate all url to visit
        """

        # from page 1 to anypage which < 200

        # # 从数据库添加
        # self._seed_url = Dao._get_url_by_id(self.source_id)

        # 直接加，测试
        self._seed_url.append(self._base_url)




    def _extract_data(self, doc_str):
        doc = Pq(doc_str)
        tables=doc("table>tr>td>table")
        # total_item =int( doc("").text().strip())
        # count_num = int(total_item) / 12
        for table in tables:
            try :
                doc = Pq(table)
                # test =  doc(doc("tr")[1]).find("td")[1].text()
                self._community_detail['location']  = Pq(doc("tr:eq(1)"))("td:eq(1)").text()
                self._community_detail['name']  =  Pq(doc("tr:eq(2)"))("a").text()
                self._community_detail['url']  =   Pq(doc("tr:eq(2)"))("a").attr("href")
                self._community_detail['area_name']  =  Pq(doc("tr:eq(8)"))("td:eq(1)").text()

                self._save_community()
            except Exception  as err:
                print(table)
                print(err)
                continue

    def _insert_community(self):
        result = "INSERT INTO  communities (ORIGINAL_URL,NAME,AREA_NAME,LATITUDE,LONGITUDE,location,source_id )" \
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
