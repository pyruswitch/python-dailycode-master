# coding=utf-8
__author__ = 'wuhan'

import DAO
import urllib
from pyquery import PyQuery as Pq
import time
from baidumap import xBaiduMap


# def getCoordinate(url):
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
# request = urllib.request.Request(url=url, headers=headers)
# m_fp = urllib.request.urlopen(request, timeout=500)
# html_str = m_fp.read().decode('utf-8')
# m_fp.close()
# pyQuery = Pq(html_str)
#     coordinateUrl = pyQuery(".border-info.comm-detail>.comm-list.clearfix>.comm-l-detail.float-l>dd>.comm-icon").attr(
#         "href")
#     coordinate = {}
#     try:
#         coordinate['latitude'] = coordinateUrl[coordinateUrl.index("l1=") + 3:coordinateUrl.index("&l2")]
#         coordinate['longitude'] = coordinateUrl[coordinateUrl.index("l2=") + 3:coordinateUrl.index("&l3")]
#     except Exception as e :
#         coordinate['latitude'] =0
#         coordinate['longitude'] = 0
#         print("error url : " + url)
#         return  coordinate
#     return coordinate

def update_communities_location(source_id, city):
    dao = DAO.Dao()
    query_sql = "SELECT ORIGINAL_URL,IFNULL(IF(address = 'null',NAME,address),  NAME) FROM communities WHERE source_id = {} ".format(
        source_id)
    # query_sql = "SELECT ORIGINAL_URL,NAME  FROM communities_temp"
    result = dao.execute_query(query_sql)
    for ORIGINAL_URL, name in result:
        bm = xBaiduMap()
        zuobiao = bm.getLocation(name, city)
        if zuobiao is not None:
            update_sql = "update communities set BAIDU_LATI = {} , BAIDU_LONG = {} ,modify_time ='{}' where ORIGINAL_URL = '{}' AND source_id = '{}' ".format(
                zuobiao[1],
                zuobiao[0],
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ORIGINAL_URL, source_id)
            dao.execute_dmls(update_sql)
            # if zuobiao is not None:
            #     update_sql = "update communities_temp set BAIDU_LATI = {} , BAIDU_LONG = {} ,modify_time ='{}' where NAME = '{}'    ".format(
            #             zuobiao[1],
            #             zuobiao[0],
            #             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), name)


            # if zuobiao[1] == 0 :
            #     continue
            # if str(zuobiao['latitude']) == str(LATITUDE) and str(zuobiao['longitude']) == str(LONGITUDE):
            #     print("unmodified url : "+ ORIGINAL_URL)
            #     continue
            # else:
            #     update_sql = "update communities set LATITUDE = {} , LONGITUDE = {} ,modify_time ='{}' where ORIGINAL_URL = '{}' AND source_id = 17  ".format(
            #         zuobiao["latitude"],
            #         zuobiao["longitude"],
            #         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), ORIGINAL_URL)
            #     dao.execute_dmls(update_sql)


def update_communities_location():
    dao = DAO.Dao()
    query_sql = "SELECT  location,  LONGITUDE,  LATITUDE FROM  ehdc.shenzhen_jigou         "
    result = dao.execute_query(query_sql)
    for location, LONGITUDE, LATITUDE in result:
        bm = xBaiduMap()
        zuobiao = bm.getLocation(location, '深圳')
        if zuobiao is not None:
            update_sql = "update ehdc.shenzhen_jigou  set LATITUDE = {} , LONGITUDE = {}   where location = '{}' ".format(
                zuobiao['lat'],
                zuobiao['lng'],
                location)
            dao.execute_dmls(update_sql)


if __name__ == '__main__':
    update_communities_location()