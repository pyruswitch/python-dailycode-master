# -*- coding: utf-8 -*-
__author__ = 'Sean Lei'

import urllib
import time

from DAO import Dao


class BaseCrawler(object):
    def __init__(self, seed_url=[]):
        self._doc_str = ''
        self._now_url = ''
        self._resualt = []
        self._seed_url = seed_url
        self._base_url = "http://www.xzqy.net/"


    def _generate_seed_url(self):
        """
        generate all url to visit
        """
        pass

    def _visit_pages(self, seed_url):
        """
        visit one url,get page content
        """

        for single_url in seed_url:
            # # 获取html源代码
            # html = self.get_page_content_str(single_url)
            #
            # #使用哪个方法进行分析
            # self._extract_data(html)

            # dao=Dao()
            # insert_sql =" INSERT INTO fetch_list (source_id, url,times,page,STATUS) VALUE(99,'{}',0,0,0)".format(single_url)
            # dao.execute_dmls(insert_sql)

            dao = Dao()
            update_sql = "   UPDATE  fetch_list2 SET  times = times+1 WHERE url = '{}'and source_id = 98 ".format(
                single_url[0])
            dao.execute_dmls(update_sql)
            self._now_url = single_url[0]
            html = self.get_page_content_str(single_url[0])
            self._extract_data2(html)

            # b = set(self._resualt)
            # self._resualt=[i for  i in b]
            # # dao=Dao()
            # insert_sql=""
            # for res1 in b :
            # insert_sql = "INSERT INTO merchant_tmp (description,url )VALUES ( '{}', 'http://www.youlin.me/category/407')".format(res1)
            # print( insert_sql  )
            # dao = Dao()
            # dao.execute_dmls(insert_sql)

    def _extract_data(self, doc_str):
        pass

    def _extract_data2(self, doc_str):
        pass

    def get_page_content_str(self, url):
        time.sleep(1)

        try:
            print("现在开始抓取" + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            request = urllib.request.Request(url=url, headers=headers)
            m_fp = urllib.request.urlopen(request, timeout=500)
            html_str = m_fp.read().decode('utf-8')
            m_fp.close()
            return html_str
        except urllib.error.URLError as err:
            # logfile = open('test.log', 'a')
            # logfile.write("Error: {} \n in  url : {}".format(err, url))
            # logfile.close()
            # print("error in {}.get_page_content_str".format(__name__))
            sql = "   UPDATE  fetch_list SET  times = 0  WHERE url = '{}'".format(self._now_url)
            dao = Dao()
            dao.execute_dmls(sql)
            # if url[-3:] == "htm":
            # time.sleep(120)
            #     return self.get_page_content_str(url)
            return None
        except Exception  as err:
            print(err)
            sql = "   UPDATE  fetch_list SET  times = 0  WHERE url = '{}'".format(self._now_url)
            dao = Dao()
            dao.execute_dmls(sql)
            return None

    def craw(self):
        self._generate_seed_url()
        self._visit_pages(self._seed_url)
        print(self._seed_url)