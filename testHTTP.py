# coding=utf-8
__author__ = 'wuhan'
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
from DAO import Dao

# def findQh(queryValue):
# values = {'query': queryValue}
#
# URL = 'http://www.123cha.com/postal/index.php'
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0','Referer':'http://www.szfcweb.com/szfcweb/(S(0fjocn55tmmm5h55pemtpsuk))/DataSerach/SaleInfoProListIndex.aspx'}
# data = urllib.parse.urlencode(values).encode(encoding='UTF8')
# # city = urllib.parse.urlencode("长沙").encode(encoding='UTF8')
# print(data)
#     request = urllib.request.Request(url=URL, headers=headers, data=data)
#     m_fp = urllib.request.urlopen(request, timeout=500)
#     html_str = m_fp.read().decode('UTF-8')
#     # print(html_str)
#     doc = Pq(html_str)
#     qh = doc("table[width='100%']>tr>td[align='left']").text()
#     return qh
#
# dao = Dao()
# querySql = "SELECT  CITY_ID ,NAME  FROM src_cities WHERE districtNo =''     "
# result = dao.execute_query(querySql)
# for CITY_ID, NAME in result:
#     districtData = findQh(NAME)
#     updateSql = "update src_cities set districtData = '{}' where city_id = '{}' ".format(districtData, CITY_ID)
#     dao.execute_dmls(updateSql)
#
URL = 'http://www.szfcweb.com/szfcweb/(S(0rtucweehhc0ql45brfcmi55))/DataSerach/SaleInfoHouseShow.aspx?PBTAB_ID=YFW003120_MD003&SPJ_ID=a5121bf5-f3af-451d-9e6c-01b1e33b2f7b'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',
           'Referer': 'http://www.szfcweb.com/szfcweb/(S(0fjocn55tmmm5h55pemtpsuk))/DataSerach/SaleInfoProListIndex.aspx'}
values = {"CorpName":"海马汽车集团股份有限公司",
          "itemname":""
    }
data = urllib.parse.urlencode(values).encode(encoding='UTF8')
request = urllib.request.Request(url=URL, headers=headers   )
m_fp = urllib.request.urlopen(request, timeout=500)
html_str = m_fp.read().decode("utf8")
print(html_str)