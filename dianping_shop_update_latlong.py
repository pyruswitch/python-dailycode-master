# -*- coding:utf-8 -*-
__author__ = 'wuhan'
import DAO
import urllib
import json


def GoogleLatALng2Baidu(geoLng, geoLat):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    url = "http://api.map.baidu.com/geoconv/v1/?coords={},{}&from=3&to=5&ak=d39Enn0oZPO717h8GRyGMkvE&qq-pf-to=pcqq.temporaryc2c".format(
        geoLng, geoLat)
    request = urllib.request.Request(url=url, headers=headers)
    m_fp = urllib.request.urlopen(request, timeout=500)
    html_str = m_fp.read().decode('utf-8')
    m_fp.close()
    s = json.loads(html_str)
    try:
        result = {
            'LATITUDE': s["result"][0]["y"],
            'LONGITUDE': s["result"][0]["x"]}
    except Exception as e:
        print(e)
        result = {'LATITUDE': "",
                  'LONGITUDE': ""}
    return result


if __name__ == '__main__':
    dao = DAO.Dao()
    query_sql = "SELECT shopId,geoLat,geoLng FROM  shop_bean where LATITUDE is null "
    result = dao.execute_query(query_sql)

    for shopId, geoLat, geoLng in result:
        zuobiao = GoogleLatALng2Baidu(geoLng, geoLat)
        update_sql = "update shop_bean set LATITUDE = {} , LONGITUDE = {}  where shopId = '{}'  ".format(
            zuobiao["LATITUDE"],
            zuobiao["LONGITUDE"], shopId)
        dao.execute_dmls(update_sql)