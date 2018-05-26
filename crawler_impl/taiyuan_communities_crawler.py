# coding=utf-8
# -*- coding: utf-8 -*-
__author__ = 'wuhan'

import urllib
from pyquery import PyQuery as Pq
from DAO import Dao
from base_crawler import BaseCrawler
from video_detail_crawler import VideoDetailCrawler as DetailCrawler
import time
import threading


class CommunitiesListCrawler(BaseCrawler, threading.Thread):
    global Dao
    Dao = Dao()

    def __init__(self):

        super().__init__()
        self.detail_info_urls = []
        self.source_id = 31
        self._base_url = "http://www.tywsfdc.com/"
        self._root_url = "http://www.tywsfdc.com/Firsthand/tyfc/publish/p/ProNBList.do?pid"
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

        # 单个url
        # html = self.get_page_content_str(self._seed_url[0]) #用数据库的时候
        self._pid = seed_url[seed_url.rindex("-"):]
        seed_url = self._root_url + "=" + self._pid
        # print("_visit_pages " + seed_url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                   'Referer': seed_url}
        values = {
            'pid': self._pid,
            'pageNo': '1',
            'pageSize': '50'}
        data = urllib.parse.urlencode(values).encode(encoding='UTF8')
        request = urllib.request.Request(url="http://www.tywsfdc.com/Firsthand/tyfc/publish/ProNBList.do",
                                         headers=headers, data=data)

        m_fp = urllib.request.urlopen(request, timeout=500)
        html_str = m_fp.read().decode("utf8")
        self.findEachBuilding(html_str)
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

        querysql = "SELECT COMMUNITY_ID,ORIGINAL_URL FROM communities WHERE   source_id ='{}' and status<2 ; ".format(
            self.source_id)
        result = Dao.execute_query(querysql)
        for COMMUNITY_ID, ORIGINAL_URL in result:
            try:
                self._apartment_detail["COMMUNITY_ID"] = int(COMMUNITY_ID)
                self._apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                # print("_generate_seed_url func : "+ORIGINAL_URL)
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
        tr_list = doc("table>tr")
        # print("tr size ")
        for tr in tr_list:
            try:
                # 进入每一栋的url
                objid = doc(tr).attr("objid")
                if objid == None:
                    continue
                self._apartment_detail["BUILDING_NUM"] = Pq(tr)("td:eq(2)").text()
                url = "http://www.tywsfdc.com/Firsthand/tyfc/publish/p/ProNBView.do?proPID={}&nbid={}".format(
                    self._pid, objid)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
                           'Referer': url}
                RequestURL = "http://www.tywsfdc.com/Firsthand/tyfc/publish/probld/NBView.do?nid={}&projectid={}".format(
                    objid,
                    self._pid)
                values = {
                    'nid': objid,
                    'projectid': self._pid}
                data = urllib.parse.urlencode(values).encode(encoding='UTF8')
                request = urllib.request.Request(
                    url=RequestURL,
                    headers=headers, data=data)

                m_fp = urllib.request.urlopen(request, timeout=500)
                html_str = m_fp.read().decode("utf8")
                self._extract_data(html_str)
            except Exception as e:
                print(e)
                pass


    def _extract_data(self, doc_str):
        try:
            doc = Pq(doc_str)
            # 每一单元
            building_list = doc("ul#bldlist>span")
            for building in building_list:
                bld = doc(building).attr("id")
                bld = bld[3:]
                self._apartment_detail["BUILDING_NUM"] = doc(building).text()
                # 每一层：
                xpath = "div.flrlist>table#{}>tr".format(bld)
                tr_list = doc(xpath)
                # total_item =int( doc("").text().strip())
                # count_num = int(total_item) / 12
                for tr in tr_list:
                    self._apartment_detail["FLOOR_NUM"] = Pq(tr)("td:eq(0)").text()
                    a_list = Pq(tr)("td:eq(1)>span>a")
                    for a in a_list:
                        self._apartment_detail["APARTMENT_NUM"] = doc(a).text()
                        if self._apartment_detail["APARTMENT_NUM"].strip() != '':
                            self._apartment_detail["create_time"] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                  time.localtime(time.time()))
                            self._save_apartments()
        except Exception  as err:
            print(err)
            time.sleep(100)
            self._extract_data(doc_str)


    def _insert_community(self):
        result = "INSERT INTO  apartments (COMMUNITY_ID , BUILDING_NUM ,FLOOR_NUM , APARTMENT_NUM ,STATUS ,create_time  )" \
                 " VALUES ('{}','{}','{}','{}','{}','{}'  )".format(self._apartment_detail["COMMUNITY_ID"],
                                                                    self._apartment_detail["BUILDING_NUM"],
                                                                    self._apartment_detail["FLOOR_NUM"],
                                                                    self._apartment_detail["APARTMENT_NUM"],
                                                                    self._apartment_detail["STATUS"],
                                                                    self._apartment_detail["create_time"])
        return result


    def _save_apartments(self):
        # 表中是否已有记录
        query_sql = "SELECT * FROM apartments WHERE COMMUNITY_ID  = {}  and BUILDING_NUM ='{}'  and APARTMENT_NUM ='{}'and FLOOR_NUM='{}' ; ".format(
            int(self._apartment_detail["COMMUNITY_ID"]), self._apartment_detail["BUILDING_NUM"],
            self._apartment_detail["APARTMENT_NUM"], self._apartment_detail["FLOOR_NUM"])
        if Dao.execute_query(query_sql) is not None:
            print(" {} is already exists ,so next".format(str(self._apartment_detail["COMMUNITY_ID"]) +
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


if __name__ == '__main__':
    c = CommunitiesListCrawler()
    c.craw()

