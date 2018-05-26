__author__ = 'wuhan'
# coding=utf-8
from pyquery import PyQuery as Pq
from DAO import Dao
import mysql.connector
from base_crawler import BaseCrawler
import time
import DAO
import urllib
import json
from dianping_shop_update_latlong import GoogleLatALng2Baidu
import threading


def save_apartments(COMMUNITY_ID, BUILDING_NUM, URL):
    # URL = 'http://www.szfcweb.com/szfcweb/(S(knmrwg452ea0mu55p2f5zi45))/DataSerach/SaleInfoHouseShow.aspx?PBTAB_ID=YFW003120_MD003&SPJ_ID=a5121bf5-f3af-451d-9e6c-01b1e33b2f7b'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
               'Referer': 'http://www.szfcweb.com/szfcweb/(S(knmrwg452ea0mu55p2f5zi45))/DataSerach/SaleInfoProListIndex.aspx'}
    dao = Dao()
    request = urllib.request.Request(url=URL)
    m_fp = urllib.request.urlopen(request, timeout=500)
    html_str = m_fp.read().decode("utf8")
    doc = Pq(html_str)
    try:
        table = doc("table.table_xkb")
        td_list = doc(table).find("div.lfzt>a")
        for td in td_list:
            APARTMENT_NUM = doc(td).text()
            insertSQL = "INSERT INTO  apartments (COMMUNITY_ID , BUILDING_NUM , APARTMENT_NUM ,STATUS ,create_time  )" \
                        " VALUES ('{}','{}','{}','{}','{}'  )".format(COMMUNITY_ID, BUILDING_NUM, APARTMENT_NUM, 2,
                                                                      time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                    time.localtime(time.time())))

            dao.execute_dmls(insertSQL)
    except Exception :
            print(Exception)
    update_sql = "update ehdc.buildings set status=2 where url = {} ;".format(URL)


def get_communities():
    dao = Dao()
    sql = '''SELECT DISTINCT
 COMMUNITY_ID,
  BUILDING_NUM,
  URL
FROM ehdc.buildings  WHERE STATUS = 0 LIMIT 1,100; '''
    result = dao.execute_query(sql)
    return result


if __name__ == '__main__':
    communities = get_communities()
    for COMMUNITY_ID, BUILDING_NUM, URL in communities:
        save_apartments(COMMUNITY_ID, BUILDING_NUM, URL)
